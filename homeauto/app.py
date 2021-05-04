from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
from gpiozero import LED, Button
from time import sleep
from datetime import datetime

#Declare Hardware
#INPUT
window = Button(37)
#OUTPUT
system_status = LED(12)
door = LED(21) #Door detection
warning = LED(20) #Warning System
red = LED(16) #Alarm system

secure_status = 'On'

current_time = datetime.now()
current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")

app = Flask(__name__)
#MAIL CONFIG
app.config.update(
        DEBUG = True,
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT=465,
        MAIL_USE_TLS=False,
        MAIL_USE_SSL=True,
        MAIL_USERNAME = '*********@gmail.com',
        MAIL_PASSWORD = '*********'
        )
mail = Mail(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        passcode = request.form.get('passcode')
        if passcode == '123456' :
            door.on()
            current_time = datetime.now()
            current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
            global secure_status
            secure_status = 'Logged in'
            return render_template('homebase.html', secure_status=secure_status, current_time=current_time)
        else:
            return alarm()
    return render_template('index.html')

def alarm():
    timer = 0
    while True:
        door.on()
        timer += 1
        sleep(0.5)
        door.off()
        timer += 1
        sleep(0.5)
        print('counting ...', timer)
        if timer > 20:
            print ('ALERT INTRUDER!!!!!')
            return alert()

def alert():
    warning.on()
    print('Inform Jack, Kerstin')
    for i in range(0,10):
        sleep(1)
        print('counting', i)    
    return send_mail()

def send_mail():
    red.on()
    msg = Message("There's an intruder!!! If you want to start the alarm and call security please go to our homebase",
    sender = "jaxhome7t@gmail.com",
    recipients = ["kerstin.burgstaller@hotmail.com", "jackjr.wk@gmail.com"])
    msg.body = "There's an intruder coming into the house. If you want to cancel the process to call security, please go to homebase and turn of the alarm."
    mail.send(msg)
    return 'Alert Sent!'

@app.route('/entry_points')
def entry_points():
    return render_template('entry_points.html')

@app.route('/logs/<name>')
def logs(name):
    return render_template('logs.html', name=name)

@app.route('/homebase/<secure_status>/<current_time>')
def homebase():
    return render_template('homebase.html', secure_status=secure_status,current_time=current_time)


#LED System
@app.route('/secure_on')
def secure_on():
    system_status.on()
    global secure_status
    secure_status = 'On'
    return render_template('homebase.html', secure_status=secure_status, current_time=current_time)

@app.route('/secure_off')
def secure_off():
    system_status.off()
    warning.off()
    red.off()
    global secure_status
    secure_status = 'Off'
    return render_template('homebase.html', secure_status=secure_status, current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
