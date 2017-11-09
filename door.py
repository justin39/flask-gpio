import sys
import time
import RPi.GPIO as GPIO
from flask import Flask, redirect, render_template, request

app = Flask(__name__, template_folder='/home/pi/Documents/apartment/templates')

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

#sys.stdout = open('door.log', 'w')
#sys.stderr = open('door.log', 'w')

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('/home/pi/Documents/apartment/door.log', maxBytes=1024*1024*100, backupCount=1)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Starting server...")

@app.route('/')
def index():
    return render_template('welcome.html')

@app.route('/open')
def open_door():
    app.logger.info("Received request for /open with query string %s", request.query_string)
    delay, duration = 0, 5
    try:
        delay = int(request.args.get('delay'))
    except:
        delay = 0
    try:
        duration = int(request.args.get('duration'))
    except:
        duration = 5
    app.logger.info("Opening door for delay %d and duration %d", delay, duration)
    time.sleep(delay)
    GPIO.output(11, GPIO.HIGH)
    time.sleep(duration)
    GPIO.output(11, GPIO.LOW)
    return render_template('open.html')

if __name__ == "__main__":
    app.run()
