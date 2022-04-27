from netmiko import ConnectHandler

def getipaddressrange(ipaddr1, ipaddr2):
    iplist = []
    startloop = int(ipaddr1.rpartition(".")[2])
    endloop = int(ipaddr2.rpartition(".")[2])
    for startloop in range(startloop, endloop + 1):
        ipaddr = ipaddr1.rpartition(".")[0] + ipaddr1.rpartition(".")[1] + str(startloop)
        iplist.append(ipaddr)
    return iplist

def saveconfig(ipaddr, sw_username, sw_passwd):

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
    #out = net_connect.send_command("archive download-sw /overwrite tftp://10.25.60.254/c2960c405-universalk9-tar.152-7.E2.tar")
    print("Sending Command to ",ipaddr," ...")
    #net_connect.send_command_timing("archive download-sw /overwrite ftp://admin1:admin1@10.25.60.254/c2960c405-universalk9-tar.152-7.E2.tar")
    net_connect.send_command_timing("reload")
    net_connect.send_command_timing("\r")

start_ip = input("Plese Enter starting ip address : ")
end_ip = input("Plese Enter ending ip address (same range) : ")

devices = getipaddressrange(start_ip, end_ip)

for y in range(len(devices)):
    saveconfig(devices[y],"ST.Cisco","ST.Cisco@132")