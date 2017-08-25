# email2username.py

This script is meant to be run after converting a Federated ID directory from email-based federation to username-based federation.  Immediately after the conversion, all of the users will have their email as their username, and will be unable to sign in.  To fix this, you supply a spreadsheet containing columns Username and Email, and the script finds everyone by their email and converts their username to be the one listed in the spreadsheet.

The script is run as:
```
python email2username.py -c config.yml -u users.csv
```
where the config file provides the UMAPI integration credentials and the users file is the spreadsheet.

The script can also be run in the opposite direction, in which case it converts the username for each user back into the user's email:
```
python email2username.py -r -c config.yml -u users.csv
```

The argument details are:
```
usage: email2username.py [-h] -c config.yml -u users.csv [-t] [-r]

Federated ID Convert from Email to Username Tool

optional arguments:
  -h, --help            show this help message and exit
  -c config.yml, --config config.yml
                        path to config file containing integration credentials
  -u users.csv, --users users.csv
                        path to csv spreadsheet with columns Username, Email
  -t, --test-mode       run updates in test mode (no changes made)
  -r, --reverse         reverse conversion (set username to email)
```

NOTE: Before running the script, install its dependencies with
```
pip -r requirements.txt
```
