# Red Team Threaded SSH Password Sprayer


Simple python3 script to spray a username and password over ssh against a subnet. It has threading included in order to speed up the wait time. With 1000 threads, it takes about 15 seconds to spray a /24 network. Unless you make changes to the system and up your ulimit cap, I recommend running this with 250 threads on Mac or 1000 threads on Kali or most other Linux flavors. It must be run with python3 and uses the paramiko library for ssh authentication. The script writes successful authentications to a file named "outfile.txt" in the current working directory.

first install the paramiko library:
pip3 install paramiko

usage:
python3 ssh-sprayer-threaded.py
