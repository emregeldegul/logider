from mfrc522 import SimpleMFRC522
from time import sleep
from RPi import GPIO as GPIO
from datetime import datetime
from sqlite3 import connect

vt = connect("logider.db")
im = vt.cursor()

GPIO.setwarnings(False)
buzzer_pin = 11

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    sleep(1)
    GPIO.output(pin, GPIO.LOW)
    return

while True:
    print("[*] Waiting Card!")

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(buzzer_pin, GPIO.OUT)

    reader = SimpleMFRC522()
    id = str(reader.read()[0])
    try:
        im.execute("SELECT * FROM user WHERE cardid = '{}'".format(id))
        user = im.fetchall()
        if len(user):
            if user[0][5] == 0:
                print("[!] Login Failed! No Fee Paid")

                GPIO.output(buzzer_pin, 1)
                sleep(0.5)
                GPIO.output(buzzer_pin, 0)

            else:
                print("[+] Login Successful: "+str(user[0][3])+" ("+str(user[0][2])+")")
                data = user[0][1], datetime.now()
                im.execute("""INSERT INTO entry (cardid, date) VALUES (?, ?)""", data)
                vt.commit()

                GPIO.output(buzzer_pin, 1)
                sleep(0.2)
                GPIO.output(buzzer_pin, 0)

        else:
            print("[-] Login Failed! User Not Found!")
            GPIO.output(buzzer_pin, 1)
            sleep(0.5)
            GPIO.output(buzzer_pin, 0)
    finally:
        GPIO.cleanup()
        sleep(0.5)
        print("\n\n")
