
from netmiko import ConnectHandler
import getpass


def getipaddressrange(ipaddr1, ipaddr2):
    iplist = []
    startloop = int(ipaddr1.rpartition(".")[2])
    endloop = int(ipaddr2.rpartition(".")[2])
    for startloop in range(startloop, endloop + 1):
        ipaddr = ipaddr1.rpartition(".")[0] + ipaddr1.rpartition(".")[1] + str(startloop)
        iplist.append(ipaddr)
    return iplist


def getcommands():
    command = []
    userinput = ""
    print("please Enter your Commands # for termination ")
    while (userinput != "#"):
        userinput = input("")
        command.append(userinput)
    command.remove("#")
    return command


def applyConf(devlist, command,usrname, pwd):
    for dev in devlist:
        switch = {
            'device_type': 'cisco_ios',
            'ip': dev,
            'user': usrname,
            'pass': pwd
        }
        net_connect = ConnectHandler(ip=switch["ip"],
                                username=switch["user"],
                                password=switch["pass"],
                                device_type=switch["device_type"])
        out = net_connect.send_config_set(command)
        print(out)
        #print(f"Configuration has been applied to {dev} Successfully ")



start_ip = input("Plese Enter starting ip address : ")
end_ip = input("Plese Enter ending ip address (same range) : ")
#username = input("Plese Enter the username : ")
#passwd = getpass.getpass("Please Enter the Password : ")

devices = getipaddressrange(start_ip, end_ip)
cmd = getcommands()

# ************** Confirmation ********************

print("\t**** For Confrmation ***** \n***** below is the list of switches ******")
for d in devices:
    print(d)

print("***** list of Commands that will be applied *****")
for c in cmd:
    print(c)

confirm = input("please chose one of following actions : \n 1 - confirm \n 2 - Need to review \n ")

if confirm == "1":
    applyConf(devices, cmd, "ST.Cisco","ST.Cisco@132")
else:
    print("\t***** Script will be terminated ******")

