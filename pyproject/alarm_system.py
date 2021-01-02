from gpiozero import LED
from time import sleep
from datetime import datetime

led = LED(21)
led_a = LED(20)
led_s = LED(16)

def turnon():
    current_time = datetime.now()
    current_time = current_time.strftime("%d/%m/%Y %H:%M:%S")
    print('The door is open at: ', current_time)
    led.on()
    sleep(5)
    led.off()
    menu()

def alarm():
    timer = 0
    loop = True
    while loop:
        #print('led is on')
        led.on()
        timer = timer + 1
        sleep(0.5)
        #print('led is off')
        led.off()
        time = timer + 1
        sleep(0.5)
        print('counting...',timer)
        if timer > 5:
            print('ALERT INTRUDER!!!!')
            alert()

def alert():
    led_a.on()
    print('ALERT Jack and Kerstin')
    print('Enable Echo sound - Intruder call 911')
    for i in range(0,10):
        print('...Counting', i )
        sleep(1)
        i += 1
    print('Call security with the recorded voice from echo\n This a voice from security system from room 204, we have intruder')
    print('Inform Jack and Kerstin that system is about to call security')
    print('Type [N] for cancel, you have 2 minute')
    res = str(input('Your decision: '))
    if res == 'N':
        led_a.off()
        return menu()
    else:
        print('Calling security')
        led_s.on()
        sleep(100)
        return menu()
        

def menu():
    ans = int(input('Enter J&Ks passcode: '))
    passcode = 123456
    if ans == passcode:
        turnon()
        print('return to normal mode\n')
        sleep(2)
        print('...')
        return menu()
    if ans != passcode:
        alarm()

menu()
