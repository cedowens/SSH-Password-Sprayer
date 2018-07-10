# Red Team SSH Password Sprayer

Simple script to spray a username and password over ssh against a subnet. It must be run with python3 and uses the paramiko library for ssh authentication.

*This script currently does not include threading so it is not optimized for speed.

first install the paramiko library: pip3 install paramiko

usage: python3 ssh-sprayer.py
