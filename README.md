CloudGenix Serial to Controller Description Utility.
------------------

This utility will verify the Element serial number exists as a hashtag in the First Controller interface description.

Each Element will have `#serial:<serial number>` appeneded to the first Controller interface when run. Script will also check and update/remove any other `#serial` hashtags in the description.

Example output (first run):
```bash
edwards-mbp-pro:serial-to-controller aaron$ ./check-create-serialtag.py
login: aaron@cloudgenix.com
Password: 

Checking all Elements for '#serial' hashtag on Controller with correct serial...
Checking 'CHC-ION-3K-1'... Added Serial Hashtag to controller 1.
Checking 'NYC-ION-3K-1'... Added Serial Hashtag to controller 1.
Checking 'SEA-ION-3K-1'... Added Serial Hashtag to controller 1.
Checking 'SFO-7K-1'... Added Serial Hashtag to controller 1.
Checking 'SFO-7K-2'... Added Serial Hashtag to controller 1.
Checking 'DC-7K-1'... Added Serial Hashtag to controller 1.
Checking 'DC-7K-2'... Added Serial Hashtag to controller 1.
Checking 'Azure US Central CGX'... Added Serial Hashtag to controller 1.
Checking 'AUTOMATION-BACKUP'... Not assigned to Site, skipping.
Checking 'AUTOMATION-BACKUP'... Added Serial Hashtag to controller 1.
Checking 'OCI-ION-7K'... Added Serial Hashtag to controller 1.
Checking 'Azure US Central CGX-2'... Added Serial Hashtag to controller 1.
Checking 'None'... Not assigned to Site, skipping.
edwards-mbp-pro:serial-to-controller aaron$
```

Example output(subsequent run):
```bash
edwards-mbp-pro:serial-to-controller aaron$ ./check-create-serialtag.py
login: aaron@cloudgenix.com
Password: 

Checking all Elements for '#serial' hashtag on Controller with correct serial...
Checking 'CHC-ION-3K-1'... Serial Hashtag Present.
Checking 'NYC-ION-3K-1'... Serial Hashtag Present.
Checking 'SEA-ION-3K-1'... Serial Hashtag Present.
Checking 'SFO-7K-1'... Serial Hashtag Present.
Checking 'SFO-7K-2'... Serial Hashtag Present.
Checking 'DC-7K-1'... Serial Hashtag Present.
Checking 'DC-7K-2'... Serial Hashtag Present.
Checking 'Azure US Central CGX'... Serial Hashtag Present.
Checking 'AUTOMATION-BACKUP'... Not assigned to Site, skipping.
Checking 'AUTOMATION-BACKUP'... Serial Hashtag Present.
Checking 'OCI-ION-7K'... Serial Hashtag Present.
Checking 'Azure US Central CGX-2'... Serial Hashtag Present.
Checking 'None'... Not assigned to Site, skipping.
edwards-mbp-pro:serial-to-controller aaron$
```

Example output (removal run)
```bash
edwards-mbp-pro:serial-to-controller aaron$ ./check-create-serialtag.py --remove
login: aaron@cloudgenix.com
Password: 

Removing all '#serial' hashtags on Controller ports.
Checking 'CHC-ION-3K-1'... Cleaned Serial Hashtags from controller 1.
Checking 'NYC-ION-3K-1'... Cleaned Serial Hashtags from controller 1.
Checking 'SEA-ION-3K-1'... Cleaned Serial Hashtags from controller 1.
Checking 'SFO-7K-1'... Cleaned Serial Hashtags from controller 1.
Checking 'SFO-7K-2'... Cleaned Serial Hashtags from controller 1.
Checking 'DC-7K-1'... Cleaned Serial Hashtags from controller 1.
Checking 'DC-7K-2'... Cleaned Serial Hashtags from controller 1.
Checking 'Azure US Central CGX'... Cleaned Serial Hashtags from controller 1.
Checking 'AUTOMATION-BACKUP'... Not assigned to Site, skipping.
Checking 'AUTOMATION-BACKUP'... Cleaned Serial Hashtags from controller 1.
Checking 'OCI-ION-7K'... Cleaned Serial Hashtags from controller 1.
Checking 'Azure US Central CGX-2'... Cleaned Serial Hashtags from controller 1.
Checking 'None'... Not assigned to Site, skipping.
edwards-mbp-pro:serial-to-controller aaron$
```

Usage Info:
```bash
edwards-mbp-pro:serial-to-controller aaron$ ./check-create-serialtag.py --help
usage: check-create-serialtag.py [-h] [--remove] [--controller CONTROLLER]
                                 [--email EMAIL] [--password PASSWORD]
                                 [--insecure] [--noregion]
                                 [--sdkdebug SDKDEBUG]

Check/Create Serial Number Tags (v1.0)

optional arguments:
  -h, --help            show this help message and exit

custom_args:
  Tag Options

  --remove              Remove all Serial Tags.

API:
  These options change how this program connects to the API.

  --controller CONTROLLER, -C CONTROLLER
                        Controller URI, ex.
                        https://api.elcapitan.cloudgenix.com

Login:
  These options allow skipping of interactive login

  --email EMAIL, -E EMAIL
                        Use this email as User Name instead of
                        cloudgenix_settings.py or prompting
  --password PASSWORD, -PW PASSWORD
                        Use this Password instead of cloudgenix_settings.py or
                        prompting
  --insecure, -I        Do not verify SSL certificate
  --noregion, -NR       Ignore Region-based redirection.

Debug:
  These options enable debugging output

  --sdkdebug SDKDEBUG, -D SDKDEBUG
                        Enable SDK Debug output, levels 0-2
edwards-mbp-pro:serial-to-controller aaron$
```

