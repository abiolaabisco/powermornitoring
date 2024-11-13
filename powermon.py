import RPi.GPIO as GPIO
import time
import smtplib
from datetime import datetime as dt
from config import LOCATION, area_location_monitoring

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from_emil = "aedcmail.com"
to_email = "aedcemail"

msg = MIMEMultipart()
msg ['from'] = from_emil
msg ['To'] = to_email
msg ['subject'] = "power is availability for power monitoring"
body = "power monitoring for "
msg.attach(MIMEText(body, 'subject'))

server = smtplib.SMTP('smtp-mail.outlook.com ', 587,)
server.starttls()
server.login(from_emil, "*******password")
text = msg.as_string()
#server.sendmail(from_emil, to_email, text, LOCATION)
#server.quit()

GPIO.setmode(GPIO.BCM)

time.sleep(5)

GPIO.setmode(GPIO.BCM)
# GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
# GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def capture_event_callback(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH mains Event detected - value: %s' % value)
        send_mains_on_email()

    else:
        print('LOW mains event detected - value: %s' % value)
        send_mains_off_email()


def capture_inverter_event_callback(channel):
    print('event detected on channel: %s' % channel)
    value = GPIO.input(channel)

    if value:
        print('HIGH inverter Event detected - value: %s' % value)
        send_inverter_on_email()

    else:
        print('LOW inverter event detected - value: %s' % value)
        send_inverter_off_email()


def send_mains_on_email(body):
	msg['subject'] = "mains is on in garki area office"
	server.sendmail(from_emil, to_email, text, LOCATION, area_location_monitoring)
	server.quit()
    pass


def send_mains_off_email(body):
	msg['subject'] = "mains is off visit it fast"
	server.sendmail(from_emil, to_email, text, LOCATION, area_location_monitoring)
	server.quit()
    pass


def send_inverter_on_email(body):
	msg['subject'] = "inverter is on"
	server.sendmail(from_emil, to_email, text, LOCATION, area_locastion_monitoring)
	server.quit()
    pass


def send_inverter_off_email(body):
	msg ['subject'] = "inverter is down urgent attention needed"
	server.sendmail(from_emil, to_email, text, LOCATION, area_location_monitoring)
	server.quit()
    pass

def post_to_es():
    pass


def main():
    # GPIO.add_event_detect(5, GPIO.BOTH, callback=capture_event_callback, bouncetime=200)
    GPIO.add_event_detect(6, GPIO.BOTH, callback=capture_event_callback, bouncetime=200)
    # GPIO.add_event_detect(20, GPIO.BOTH, callback=capture_inverter_event_callback, bouncetime=200)
    GPIO.add_event_detect(21, GPIO.BOTH, callback=capture_inverter_event_callback, bouncetime=200)

    while True:
        #    print("Waiting to detect event")
        time.sleep(50000)


if __name__ == '__main__':
    main()
