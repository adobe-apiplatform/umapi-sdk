# email2username.py

This script is meant to be run after converting a Federated ID directory from email-based federation to username-based federation.  Immediately after the conversion, all of the users will have their email as their username, and will be unable to sign in.  To fix this, you supply a spreadsheet containing columns Username and Email, and the script finds everyone by their email and converts their username to be the one listed in the spreadsheet.

The script can also be run in the opposite direction, in which case it converts all the usernames back into their emails.  Supply the `--reverse` (or `-r`) to run it this way.

If you supply no arguments, the script will document its usage.
