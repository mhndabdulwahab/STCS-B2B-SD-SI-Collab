from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
@app.route('/')
def home():
    return render_template('form.html')

@app.route('/configuration')
def configuration():
    
    VoiceGatewayIP = request.form.get("VoiceGatewayIP")
    VoiceGatewayUsername =request.form.get("VoiceGatewayUsername")
    VoiceGatewayPassword=request.form.get("VoiceGatewayPassword")
    PrimaryCallManager=request.form.get("PrimaryCallManager")
    SecondaryCallManager=request.form.get("SecondaryCallManager")
    STCCustomerIP=request.form.get("STCCustomerIP")
    STCSIPProxyIP=request.form.get("STCSIPProxyIP")
    First=request.form.get("First")
    Last=request.form.get("Last")
    return render_template("configuration.html",VoiceGatewayIP=VoiceGatewayIP,VoiceGatewayUsername=VoiceGatewayUsername,VoiceGatewayPassword=VoiceGatewayPassword,PrimaryCallManager=PrimaryCallManager,SecondaryCallManager=SecondaryCallManager,STCCustomerIP=STCCustomerIP,STCSIPProxyIP=STCSIPProxyIP,First=First,Last=Last)

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)
