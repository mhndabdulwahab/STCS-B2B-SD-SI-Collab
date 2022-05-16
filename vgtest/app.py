from flask import Flask ,render_template ,request
from netmiko import *


app = Flask(__name__)

@app.route('/')
def home():
   return render_template("form.html")

@app.route('/configuration', methods=["post"])

def configuration():

    VoiceGatewayIP =request.form.get("VoiceGatewayIP")

    VoiceGatewayUsername =request.form.get("VoiceGatewayUsername")

    VoiceGatewayPassword=request.form.get("VoiceGatewayPassword")

    CustomerIP=request.form.get("CustomerIP")

    ISP_IP=request.form.get("ISP_IP")

    ISP_SIP_Proxy_IP=request.form.get("ISP_SIP_Proxy_IP")

    PrimaryCallManager=request.form.get("PrimaryCallManager")

    SecondaryCallManager=request.form.get("SecondaryCallManager")

    FirstField=request.form.get("FirstField")

    SecondField=request.form.get("SecondField")

    ThirdField=request.form.get("ThirdField")

    FirstFieldR2=request.form.get("FirstFieldR2")

    SecondFieldR2=request.form.get("SecondFieldR2")

    ThirdFieldR2=request.form.get("ThirdFieldR2")

    
    if int(ThirdFieldR2) - int(ThirdField) >= 999:
        ThirdFieldRange = int(ThirdFieldR2)/1000
        Range=str(int(ThirdFieldRange))+"...$"
    elif  int(ThirdFieldR2) - int(ThirdField) >= 99:
        ThirdFieldRange = int(ThirdFieldR2)/100
        Range=str(int(ThirdFieldRange))+"..$"
    
    vgcommand( Range,ThirdFieldRange,VoiceGatewayUsername,VoiceGatewayPassword,VoiceGatewayIP,CustomerIP,ISP_IP,ISP_SIP_Proxy_IP,PrimaryCallManager,SecondaryCallManager,FirstField,SecondField,ThirdField,FirstFieldR2,SecondFieldR2,ThirdFieldR2)

    return  render_template("configuration.html",VoiceGatewayUsername=VoiceGatewayUsername,VoiceGatewayPassword=VoiceGatewayPassword,VoiceGatewayIP=VoiceGatewayIP,CustomerIP=CustomerIP,ISP_IP=ISP_IP,ISP_SIP_Proxy_IP=ISP_SIP_Proxy_IP,PrimaryCallManager=PrimaryCallManager,SecondaryCallManager=SecondaryCallManager,FirstField=FirstField,SecondField=SecondField,ThirdField=ThirdField,FirstFieldR2=FirstFieldR2,SecondFieldR2=SecondFieldR2,ThirdFieldR2=ThirdFieldR2)
    
def vgcommand( Range,ThirdFieldRange,VoiceGatewayUsername,VoiceGatewayPassword,VoiceGatewayIP,CustomerIP,ISP_IP,ISP_SIP_Proxy_IP,PrimaryCallManager,SecondaryCallManager,FirstField,SecondField,ThirdField,FirstFieldR2,SecondFieldR2,ThirdFieldR2):
    
    Basic = [ "clock timezone GMT 3 0",
	"no ip domain lookup",
	"voice-card 0",
	"dspfarm",
	"dsp services dspfarm"
	]
    
    CUBE =[ "voice service voip",
	"ip address trusted list",
	"ipv4"+PrimaryCallManager,
	"ipv4"+SecondaryCallManager,
	"ipv4"+ISP_SIP_Proxy_IP,
	"ipv4"+VoiceGatewayIP,
	"allow-connections h323 to h323",
	"allow-connections h323 to sip ",
	"allow-connections sip to h323 ",
	"allow-connections sip to sip",
	"no supplementary-service sip moved-temporarily",
	"no supplementary-service sip refer ",
	" no supplementary-service sip handle-replaces ",
	"redirect ip2ip",  
	"fax protocol t38 version 0 ls-redundancy 0 hs-redundancy 0 fallback none ",
    " h323 " ,
	" session transport udp",
	" h245 caps mode restricted",
	"sip ",
	" voice class codec 1 ",
	" codec preference 1 g711alaw ",
	" codec preference 2 g711ulaw"]



    Translation=["voice translation-rule 1 ",
    "rule 1 /^[234678]......$/ /9\0/",
     "rule 2 /^1[1-9].......$/ /90\0/ ",
     "  rule 3 /^01[1-9].......$/ /9\0/ ",
     " rule 4 /^5........$/ /90\0/  ",
     " rule 5 /^00.+/ /9\0/ ",
    " voice translation-rule 2",
    " rule 1 /^"+SecondField+"\("+Range+"\)/ /+966"+FirstField + SecondField+"\1/ ", 
    " rule 2 /^"+FirstField + SecondField+"\("+Range+"\)/ /+966"+FirstField + SecondField+"\1/ ",
    " rule 3 /^0"+FirstField + SecondField+"\("+Range+"\)/ /+966"+FirstField + SecondField+"\1/ ",
    "voice translation-rule 4 ",
    "rule 1 /9\(.*\)/ /\1/   ",
    " voice translation-profile PSTN_IN ",
    "translate calling 1 ",
    " translate called 2" ,
    " voice translation-profile PSTN_OUT ",
    " translate calling 3 ", 
    " translate called 4"]



    SCCP=[" sccp local GigabitEthernet0/0",
    "sccp ccm"+PrimaryCallManager+"  identifier 1 priority 1 version 7.0 ",
    "ccm"+SecondaryCallManager+" identifier 2 priority 2 version 7.0 sccp ",
    " sccp ccm group 1 ",
    " bind interface GigabitEthernet0/0 ",
    "associate ccm 1 priority 1",
    "associate ccm 2 priority 2 ",
    "associate profile 1 register XCODE ",
    " registration timeout 3 ",
    " keepalive timeout 3 ",
    " switchover method immediate ",
    "switchback ", 
    "method immediate ",
    "dspfarm profile 1 transcode ",
    "codec g729r8 ",
    "codec g711ulaw ",
    "codec g711alaw ",
    "codec g729ar8 ", 
    "codec g729abr8 ",
    "maximum sessions 25",
    " associate application SCCP "] 



    Dial_peer= [ "dial-peer voice 11001 voip ", 
    "description *** Incoming from CUCM *** ",
    "session protocol sipv2 ",
    "incoming called-number . ",
    " voice-class codec 1 ",
    "dtmf-relay rtp-nte ",
    " fax-relay ecm disable ",  
    "fax protocol t38 version 0 ls-redundancy 0 hs-redundancy 0 fallback pass-through g711alaw ",
    "no vad ",
    "dial-peer voice 21001 voip " ,
    "description *** Outgoing dial-peer to CUCM SUB *** ",
    "destination-pattern "+Range,
    "session protocol sipv2 ",
    "session target ipv4:"+SecondaryCallManager,
    "voice-class codec 1",
    "voice-class sip bind control source-interface GigabitEthernet0/0/0 ",
    "voice-class sip bind media source-interface GigabitEthernet0/0/0 ",
    "dtmf-relay rtp-nte ", 
    "fax-relay ecm disable ",  
    "fax protocol t38 version 0 ls-redundancy 0 hs-redundancy 0 fallback pass-through g711alaw ",
    "no vad"] 
    Dial_peer2 = ["dial-peer voice 21002 voip" ,
    "description *** Outgoing dial-peer to CUCM PUB ***",
    "preference 2 \n  destination-pattern " +Range, 
    "session protocol sipv2 ",
    "session target ipv4:"+PrimaryCallManager,
    "voice-class codec 1 ",
    "voice-class sip bind control source-interface GigabitEthernet0/0/0 ", 
    "voice-class sip bind media source-interface GigabitEthernet0/0/0",
    "dtmf-relay rtp-nte ",
    "fax-relay ecm disable ", 
    "fax protocol t38 version 0 ls-redundancy 0 hs-redundancy 0 fallback pass-through g711alaw ",
    "no vad "]
    
    Dial_peer3=["dial-peer voice 31001 voip ",
    "description *** Incoming from PSTN ****** ",  
    "translation-profile incoming PSTN_IN ",
    "session protocol sipv2 ", 
    "incoming called-number 0"+FirstField + SecondField+ Range+
    "voice-class codec 1 ",
    "dtmf-relay rtp-nte ",
    "fax-relay ecm disable ", 
    " no vad ",
    " dial-peer voice 31002 voip ",
    " description *** Incoming from PSTN ****** ",
    " translation-profile incoming PSTN_IN ",
    " session protocol sipv2 ",
    "incoming called-number"+FirstField + SecondField+ Range,
    " voice-class codec 1 ",
    " dtmf-relay rtp-nte ", 
    " fax-relay ecm disable ",
    " no vad ",  
    " dial-peer voice 31003 voip ",
    " description *** Incoming from PSTN ****** ",
    "translation-profile incoming PSTN_IN ",
    " session protocol sipv2 ",
    "  incoming called-number"+FirstField + SecondField+ Range,
    " voice-class codec 1 ", 
    "dtmf-relay rtp-nte ",
    " fax-relay ecm disable ", 
    " no vad ",
    "dial-peer voice 41001 voip ", 
    "description *** Outgoing to PSTN ******* ", 
    "translation-profile outgoing PSTN_OUT ",
    " destination-pattern 9T ",
    "  session protocol sipv2 ",
    " session target ipv4:"+ISP_SIP_Proxy_IP,
    " session transport udp ",
    "voice-class codec 1 ",
    " voice-class sip dtmf-relay force rtp-nte ",
    " voice-class sip bind control source-interface GigabitEthernet0/0/1 ",
    "voice-class sip bind media source-interface GigabitEthernet0/0/1 ",
    " dtmf-relay rtp-nte \n  no vad "]

    applyConf(VoiceGatewayIP,Basic,VoiceGatewayUsername,VoiceGatewayPassword)



def applyConf(VoiceGatewayIP,CUBE,VoiceGatewayUsername,VoiceGatewayPassword):
    
        switch = {
            'device_type': 'cisco_ios',
            'ip': VoiceGatewayIP,
            'user': VoiceGatewayUsername,
            'pass': VoiceGatewayPassword,
            'port':'23'
        }
        net_connect = ConnectHandler(ip=switch["ip"],
                                username=switch["user"],
                                password=switch["pass"],
                                device_type=switch["device_type"],
                                port=switch["port"]
                                )
        out = net_connect.send_confg_set(CUBE)
        print(out)    


app.run()
if __name__ == '__main__':
    app.run(debug=True)