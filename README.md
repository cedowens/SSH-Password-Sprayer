# Blue Team OSX/Linux Suspicious Process Checker

Simple python script to look for suspicious processes being used for reverse shell connections. This would be helpful when you have a Mac or Linux machine you suspect is infected and would be a quick way to check for the presence of common reverse shells. This script does not look at anything related to browser plugins or PUP/adware. Instead, this script searches at the process level.

first: install psutil library (pip3 install psutil)

Usage: python3 process-checker.py

Run on a machine you suspect is compromised to search for the presence of common reverse shells.

