#!/usr/bin/env python
import sys
import os
import argparse
import re

serial_match = re.compile("#serial:[a-zA-Z0-9-]*")

####
#
# Enter other desired optional system modules here.
#
####

import json

####
#
# End other desired system modules.
#
####

# Import CloudGenix Python SDK
try:
    import cloudgenix
    jdout = cloudgenix.jdout
    jd = cloudgenix.jd
except ImportError as e:
    cloudgenix = None
    sys.stderr.write("ERROR: 'cloudgenix' python module required. (try 'pip install cloudgenix').\n {0}\n".format(e))
    sys.exit(1)

# Check for cloudgenix_settings.py config file in cwd.
sys.path.append(os.getcwd())
try:
    from cloudgenix_settings import CLOUDGENIX_AUTH_TOKEN

except ImportError:
    # if cloudgenix_settings.py file does not exist,
    # Get AUTH_TOKEN/X_AUTH_TOKEN from env variable, if it exists. X_AUTH_TOKEN takes priority.
    if "X_AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('X_AUTH_TOKEN')
    elif "AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    else:
        # not set
        CLOUDGENIX_AUTH_TOKEN = None

try:
    # Also, seperately try and import USERNAME/PASSWORD from the config file.
    from cloudgenix_settings import CLOUDGENIX_USER, CLOUDGENIX_PASSWORD

except ImportError:
    # will get caught below
    CLOUDGENIX_USER = None
    CLOUDGENIX_PASSWORD = None


# Handle differences between python 2 and 3. Code can use text_type and binary_type instead of str/bytes/unicode etc.
if sys.version_info < (3,):
    text_type = unicode
    binary_type = str
else:
    text_type = str
    binary_type = bytes


####
#
# Start custom modifiable code
#
####

GLOBAL_MY_SCRIPT_NAME = "Check/Create Serial Number Tags"
GLOBAL_MY_SCRIPT_VERSION = "v1.0"


def extract_tags(cgx_dict):
    """
    This function looks at a CloudGenix config object, and gets hashtags.
    :param cgx_dict: CloudGenix config dict, expects "description" keys supported in root.
    :return: list of tags present.
    """

    # need to check hashtags in description.
    description = cgx_dict.get("description", "")
    # check for None.
    if description is None:
        description = ""
    # select all hashtags in description text, space or \n separated, strip hash,
    # and no empty tags (ensure string not "" after lstrip).
    hashtags = [tag.lstrip('#') for tag in description.split() if tag.startswith("#") and tag.lstrip("#")]

    # return unique tags from both sources.
    return list(set(hashtags))


def put_tags(new_tag_list, cgx_dict):
    """
    This function looks at a CloudGenix config object, looks in description for hashtags, and appends new ones.
    :param new_tag_list: List of tags to add if not already present.
    :param cgx_dict: CloudGenix config dict, expects "description" keys supported in root.
    :return: list of tags present.
    """

    # need to use hashtags in description.
    description = cgx_dict.get("description", "")
    # check for None.
    if description is None:
        description = ""
    # select all hashtags in description text, space or \n seperated, strip hash,
    # and no empty tags (ensure string not "" after lstrip).
    # use regex to strip any existing serial tags.
    description = serial_match.sub('', description)
    tags = [tag.lstrip('#') for tag in description.split() if tag.startswith("#") and tag.lstrip("#")]
    # figure out tags not in description, and append them.
    needed_tags = [tag for tag in new_tag_list if tag not in tags]
    for tag in needed_tags:
        description += " #{0}".format(tag)
    # update dict
    cgx_dict["description"] = description

    return cgx_dict


def remove_tags(cgx_dict):
    """
    This function looks at a CloudGenix config object, looks in description for hashtags, removes all serial tags.
    :param cgx_dict: CloudGenix config dict, expects "description" keys supported in root.
    :return: list of tags present.
    """

    # need to use hashtags in description.
    description = cgx_dict.get("description", "")
    # check for None.
    if description is None:
        description = ""
    # select all hashtags in description text, space or \n seperated, strip hash,
    # and no empty tags (ensure string not "" after lstrip).
    # use regex to strip any existing serial tags.
    description = serial_match.sub('', description)
    cgx_dict["description"] = description

    return cgx_dict

####
#
# End custom modifiable code
#
####


# Start the script.
def go():
    """
    Stub script entry point. Authenticates CloudGenix SDK, and gathers options from command line to run do_site()
    :return: No return
    """

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0} ({1})".format(GLOBAL_MY_SCRIPT_NAME, GLOBAL_MY_SCRIPT_VERSION))

    ####
    #
    # Add custom cmdline argparse arguments here
    #
    ####
    custom_group = parser.add_argument_group('custom_args', 'Tag Options')
    custom_group.add_argument("--remove", help="Remove all Serial Tags.",
                              default=False, action="store_true")
    ####
    #
    # End custom cmdline arguments
    #
    ####

    # Standard CloudGenix script switches.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. https://api.elcapitan.cloudgenix.com",
                                  default=None)

    login_group = parser.add_argument_group('Login', 'These options allow skipping of interactive login')
    login_group.add_argument("--email", "-E", help="Use this email as User Name instead of cloudgenix_settings.py "
                                                   "or prompting",
                             default=None)
    login_group.add_argument("--password", "-PW", help="Use this Password instead of cloudgenix_settings.py "
                                                       "or prompting",
                             default=None)
    login_group.add_argument("--insecure", "-I", help="Do not verify SSL certificate",
                             action='store_true',
                             default=False)
    login_group.add_argument("--noregion", "-NR", help="Ignore Region-based redirection.",
                             dest='ignore_region', action='store_true', default=False)

    debug_group = parser.add_argument_group('Debug', 'These options enable debugging output')
    debug_group.add_argument("--sdkdebug", "-D", help="Enable SDK Debug output, levels 0-2", type=int,
                             default=0)

    args = vars(parser.parse_args())

    sdk_debuglevel = args["sdkdebug"]

    # Build SDK Constructor
    if args['controller'] and args['insecure']:
        sdk = cloudgenix.API(controller=args['controller'], ssl_verify=False)
    elif args['controller']:
        sdk = cloudgenix.API(controller=args['controller'])
    elif args['insecure']:
        sdk = cloudgenix.API(ssl_verify=False)
    else:
        sdk = cloudgenix.API()

    # check for region ignore
    if args['ignore_region']:
        sdk.ignore_region = True

    # SDK debug, default = 0
    # 0 = logger handlers removed, critical only
    # 1 = logger info messages
    # 2 = logger debug messages.

    if sdk_debuglevel == 1:
        # CG SDK info
        sdk.set_debug(1)
    elif sdk_debuglevel >= 2:
        # CG SDK debug
        sdk.set_debug(2)

    # login logic. Use cmdline if set, use AUTH_TOKEN next, finally user/pass from config file, then prompt.
    # figure out user
    if args["email"]:
        user_email = args["email"]
    elif CLOUDGENIX_USER:
        user_email = CLOUDGENIX_USER
    else:
        user_email = None

    # figure out password
    if args["password"]:
        user_password = args["password"]
    elif CLOUDGENIX_PASSWORD:
        user_password = CLOUDGENIX_PASSWORD
    else:
        user_password = None

    # check for token
    if CLOUDGENIX_AUTH_TOKEN and not args["email"] and not args["password"]:
        sdk.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)
        if sdk.tenant_id is None:
            print("AUTH_TOKEN login failure, please check token.")
            sys.exit(1)

    else:
        while sdk.tenant_id is None:
            sdk.interactive.login(user_email, user_password)
            # clear after one failed login, force relogin.
            if not sdk.tenant_id:
                user_email = None
                user_password = None

    ####
    #
    # Do your custom work here, or call custom functions.
    #
    ####

    remove = args['remove']

    if not remove:
        print("Checking all Elements for '#serial' hashtag on Controller with correct serial...")
    else:
        print("Removing all '#serial' hashtags on Controller ports.")

    elements_resp = sdk.get.elements()

    if elements_resp.cgx_status:
        elements_cache = elements_resp.cgx_content.get('items', [])
    else:
        print("ERROR: Unable to read 'elements': {0}".format(cloudgenix.jdout_detailed(elements_resp)))
        sys.exit()

    for element in elements_cache:
        element_id = element.get('id')
        element_displayname = element.get('name', element_id)
        print("Checking '{0}'... ".format(element_displayname), end="")

        element_id = element.get('id')
        site = element.get("site_id")
        serial_no = element.get("serial_number")

        if not serial_no:
            print("Error getting Serial Number.")
            continue
        if not site or site == "1":
            print("Not assigned to Site, skipping.")
            continue

        interfaces_resp = sdk.get.interfaces(site, element_id)

        if interfaces_resp.cgx_status:
            interfaces_cache = interfaces_resp.cgx_content.get('items', [])
        else:
            print("Unable to read 'interfaces'. Skipping.")
            continue

        selected_interface = {}
        for interface in interfaces_cache:
            if interface.get('name') in ['controller', 'controller 1']:
                selected_interface = interface
                continue

        if not selected_interface:
            print("Could not find Controller/Controller 1 interface. Skipping.")
            continue

        selected_interface_id = selected_interface.get('id')
        selected_interface_name = selected_interface.get('name')
        serial_hashtag = "serial:{0}".format(serial_no)
        interface_hashtags = extract_tags(selected_interface)

        if remove:
            candidtate_interface_config = remove_tags(selected_interface)

            interface_edit_resp = sdk.put.interfaces(site, element_id, selected_interface_id,
                                                     candidtate_interface_config)

            if interface_edit_resp.cgx_status:
                print("Cleaned Serial Hashtags from {0}.".format(selected_interface_name))
            else:
                print("Failed Clean Serial Hashtags: {0}".format(cloudgenix.jdout_detailed(interface_edit_resp)))

        else:  # add/check
            if serial_hashtag in interface_hashtags:
                print("Serial Hashtag Present.")
                continue

            # tag not present, add.
            candidtate_interface_config = put_tags([serial_hashtag], selected_interface)

            interface_edit_resp = sdk.put.interfaces(site, element_id, selected_interface_id, candidtate_interface_config)

            if interface_edit_resp.cgx_status:
                print("Added Serial Hashtag to {0}.".format(selected_interface_name))
            else:
                print("Failed to add Serial Hashtag: {0}".format(cloudgenix.jdout_detailed(interface_edit_resp)))

    ####
    #
    # End custom work.
    #
    ####


if __name__ == "__main__":
    go()
