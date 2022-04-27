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

def saveconfig(ipaddr, sw_username, sw_passwd,path):

    switch = {
                    'device_type': 'cisco_ios',
                    'ip': ipaddr,
                    'user': sw_username,
                    'pass': sw_passwd
                }
    net_connect = ConnectHandler(ip=switch["ip"],
                                    username=switch["user"],
                                    password=switch["pass"],
                                    device_type=switch["device_type"])
    net_connect.save_config()
    out = net_connect.send_command("sh run")


    conf = ""
    for i in range(len(out)):
        conf += out[i]

    filename = ""
    hoststart = conf.find("hostname") + 9

    while conf[hoststart] != "!":
        filename += conf[hoststart]
        hoststart += 1

    filename = filename.strip("\n") + ".txt"

    file = open(f"{path}/{filename}", "w+")
    file.write(conf)
    print("Backup Completed Successfully for ",ipaddr," Node ...")


start_ip = input("Plese Enter starting ip address : ")
end_ip = input("Plese Enter ending ip address (same range) : ")
username = input("Plese Enter the username : ")
passwd = getpass.getpass('Please Enter the password : ')
filepath = input("Please Enter the path : ")

devices = getipaddressrange(start_ip, end_ip)

for y in range(len(devices)):
    saveconfig(devices[y],username,passwd,filepath.replace("\\","/"))

