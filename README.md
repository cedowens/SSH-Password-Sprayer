# Red Team SSH Password Sprayer

Simple script to spray a username and password over ssh against a subnet. It must be run with python3 and uses the paramiko library for ssh authentication. The script writes successful authentications to a file named "outfile.txt" in the current working directory.

first install the paramiko library:
pip3 install paramiko

usage:
python3 ssh-sprayer.py

___________________________________
DISCLAIMER

Use at your own risk. Do not use without the appropriate authorizations.
