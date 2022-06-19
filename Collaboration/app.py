from flask import Flask ,render_template ,request
from netmiko import *
from numpy import append

from test import ThirdField
port_no=""
device_t=""
logging = ""
HcsShareDilledNumber = ""



app = Flask(__name__)

@app.route('/')
def home():
   return render_template("form.html")

@app.route('/configuration', methods=["post"])

def configuration():
    global hosted

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
    
    connection=request.form.get("connection")

    hosted=request.form.get("hosted")

    cluster=request.form.get("cluster")


    
    global port_no
    global device_t

    if connection == "Telnet":
        port_no="23"
        device_t="cisco_ios_telnet"
    else:
        port_no="22"
        device_t="cisco_ios_ssh"


    if int(ThirdFieldR2) - int(ThirdField) >= 999:
        ThirdFieldRange = int(ThirdFieldR2)/1000
        Range=str(int(float(ThirdFieldRange)))+"...$"
    elif  int(ThirdFieldR2) - int(ThirdField) >= 99:
        ThirdFieldRange = int((ThirdFieldR2))/100
        Range=str(int(ThirdFieldRange))+"..$"

   
        

   

    global HcsShareDilledNumber
    if hosted =="Hosted collab solution":
        if cluster =="shared_cluster":
            HcsShareDilledNumber = "\+966" + FirstField + SecondField
        else:
            HcsShareDilledNumber = ""


    else:
        HcsShareDilledNumber=""

    
    vgcommand( HcsShareDilledNumber,Range,VoiceGatewayUsername,VoiceGatewayPassword,VoiceGatewayIP,ISP_SIP_Proxy_IP,PrimaryCallManager,SecondaryCallManager,FirstField,SecondField)

    # return  render_template("configuration.html",VoiceGatewayUsername=VoiceGatewayUsername,VoiceGatewayPassword=VoiceGatewayPassword,VoiceGatewayIP=VoiceGatewayIP,CustomerIP=CustomerIP,ISP_IP=ISP_IP,ISP_SIP_Proxy_IP=ISP_SIP_Proxy_IP,PrimaryCallManager=PrimaryCallManager,SecondaryCallManager=SecondaryCallManager,FirstField=FirstField,SecondField=SecondField,ThirdField=ThirdField,FirstFieldR2=FirstFieldR2,SecondFieldR2=SecondFieldR2,ThirdFieldR2=ThirdFieldR2)
    return  render_template("configuration.html",logging=logging)

def vgcommand(HcsShareDilledNumber, Range,VoiceGatewayUsername,VoiceGatewayPassword,VoiceGatewayIP,ISP_SIP_Proxy_IP,PrimaryCallManager,SecondaryCallManager,FirstField,SecondField):
    
    Basic = [ "clock timezone GMT 3 0",
	"no ip domain lookup",
	"voice-card 0/4",
	"dsp services dspfarm"
	]
    
    CUBE =[ "voice service voip",
	"ip address trusted list",
	"ipv4 "+PrimaryCallManager,
	"ipv4 "+SecondaryCallManager,
	"ipv4 "+ISP_SIP_Proxy_IP,
	"ipv4 "+VoiceGatewayIP,
	"allow-connections h323 to h323",
	"allow-connections h323 to sip ",
	"allow-connections sip to h323 ",
	"allow-connections sip to sip",
	"no supplementary-service sip moved-temporarily",
	"no supplementary-service sip refer ",
	"no supplementary-service sip handle-replaces ",
	"redirect ip2ip",  
	"fax protocol t38 version 0 ls-redundancy 0 hs-redundancy 0 fallback none ",
    "h323 " ,
	"session transport udp",
	"h245 caps mode restricted",
	"sip ",
	"voice class codec 1 ",
	"codec preference 1 g711alaw ",
	"codec preference 2 g711ulaw"]


    Translation=["voice translation-rule 1 ",
    "rule 1 /^[234678]......$/ /9"+"\\"+"0/",
    "rule 2 /^1[1-9].......$/ /90"+"\\"+"0/ ",
    "rule 3 /^01[1-9].......$/ /9"+"\\"+"0/ ",
    "rule 4 /^5........$/ /90"+"\\"+"0/  ",
    "rule 5 /^00.+/ /9"+"\\"+"0/ ",
    "voice translation-rule 2",
    "rule 1 /^"+SecondField+""+"\\"+"("+Range+""+"\\"+")/ /"+HcsShareDilledNumber+"\\"+"1/ ", 
    "rule 2 /^"+FirstField + SecondField+""+"\\"+"("+Range+""+"\\"+")/ /"+HcsShareDilledNumber+"\\"+"1/",
    "rule 3 /^0"+FirstField + SecondField+""+"\\"+"("+Range+""+"\\"+")/ /"+"\\"+HcsShareDilledNumber+"1/",
    "voice translation-rule 3",
    "rule 1 /^.+966"+FirstField + SecondField+""+"\\"+"("+Range+""+"\\"+")/ /" + SecondField+""+"\\"+"1/ ",
    "voice translation-rule 4 ",
    "rule 1 /9\(.*\)/ /"+"\\"+"1/   ",
    "voice translation-profile PSTN_IN ",
    "translate calling 1 ",
    "translate called 2" ,
    "voice translation-profile PSTN_OUT ",
    "translate calling 3 ", 
    "translate called 4"]

    SCCP=[" sccp local GigabitEthernet0/0/0",
    "sccp ccm "+PrimaryCallManager+"  identifier 1 priority 1 version 7.0 ",
    "sccp ccm "+SecondaryCallManager+" identifier 2 priority 2 version 7.0",
    "sccp",
    "sccp ccm group 1 ",
    "bind interface GigabitEthernet0/0/0 ",
    "associate ccm 1 priority 1",
    "associate ccm 2 priority 2 ",
    "associate profile 1 register VG_XCODE",
    "associate profile 2 register VG_MTP",
    "registration timeout 3 ",
    "keepalive timeout 3 ",
    "switchover method immediate ",
    "dspfarm profile 1 transcode ",
    "maximum sessions 8",
    "associate application SCCP ",
    "no shutdown",
    "dspfarm profile 2 mtp",
    "maximum sessions software 30",
    "associate application sccp",
    "no shutdown"] 

    Dial_peer= [ "dial-peer voice 11001 voip ", 
    "description *** Incoming from CUCM *** ",
    "session protocol sipv2 ",
    "incoming called-number . ",
    "voice-class codec 1 ",
    "dtmf-relay rtp-nte ",
    "fax-relay ecm disable ",  
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
    "preference 2",
    "destination-pattern " +Range, 
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
    "session protocol sipv2 "
    "dial-peer voice 31002 voip ",
    "description *** Incoming from PSTN ****** ",
    "translation-profile incoming PSTN_IN ",
    "session protocol sipv2 ",
    "incoming called-number "+FirstField + SecondField+ Range,
    "voice-class codec 1 ",
    "dtmf-relay rtp-nte ", 
    "dial-peer voice 31003 voip ",
    "description *** Incoming from PSTN ****** ",
    "translation-profile incoming PSTN_IN ",
    "session protocol sipv2 ",
    "incoming called-number "+FirstField + SecondField+ Range,
    "voice-class codec 1 ", 
    "dtmf-relay rtp-nte ",
    "fax-relay ecm disable ", 
    "no vad ",
    "dial-peer voice 41001 voip ", 
    "description *** Outgoing to PSTN ******* ", 
    "translation-profile outgoing PSTN_OUT ",
    "destination-pattern 9T ",
    "session protocol sipv2 ",
    "session target ipv4:"+ISP_SIP_Proxy_IP,
    "session transport udp ",
    "voice-class codec 1 ",
    "voice-class sip dtmf-relay force rtp-nte ",
    "voice-class sip bind control source-interface GigabitEthernet0/0/1 ",
    "voice-class sip bind media source-interface GigabitEthernet0/0/1 ",
    "dtmf-relay rtp-nte",   
    "no vad"
    "do wr"]

    applyConf(VoiceGatewayIP,Basic,CUBE,Translation,SCCP,Dial_peer,Dial_peer2,Dial_peer3,VoiceGatewayUsername,VoiceGatewayPassword)
    

def applyConf(VoiceGatewayIP,Basic,CUBE,Translation,SCCP,Dial_peer,Dial_peer2,Dial_peer3,VoiceGatewayUsername,VoiceGatewayPassword):  
         global logging 
        
         net_connect = ConnectHandler(ip=VoiceGatewayIP,
                                username=VoiceGatewayUsername,
                                password=VoiceGatewayPassword,
                               device_type=device_t,
                               port=port_no)
         out =net_connect.send_config_set(Basic)
         logging +=out
         out =net_connect.send_config_set(CUBE)
         #logging +=out
         out =net_connect.send_config_set(Translation)
         logging +=out
         out =net_connect.send_config_set(SCCP)
         logging += out
         out =net_connect.send_config_set(Dial_peer)
         logging +=out
         out =net_connect.send_config_set(Dial_peer2)
         logging +=out
         out =net_connect.send_config_set(Dial_peer3)
         logging = logging.split('\n')
         print(logging)  
       
       
        #  logging=(Basic)
        #  logging+=(CUBE)
        #  logging+=(Translation)
        #  logging+=(SCCP)
        #  logging+=(Dial_peer)
        #  logging+=(Dial_peer2)
        #  logging+=(Dial_peer3)


        #  print(logging)
        

   

app.run()
if __name__ == '__main__':
    app.run(debug=True)