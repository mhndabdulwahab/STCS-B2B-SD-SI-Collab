from netmiko import *

CUBE =[ "voice service voip",
        "allow-connections h323 to h323",
        "allow-connections h323 to sip ",
        "allow-connections sip to h323 ",
        "allow-connections sip to sip",
        ]

net_connect = ConnectHandler(ip="192.168.10.1",
                                username="admin",
                                password="cisco",
                                device_type="cisco_ios_telnet",
                                port="23")

out = net_connect.send_config_set(CUBE)
print(out)                                  
