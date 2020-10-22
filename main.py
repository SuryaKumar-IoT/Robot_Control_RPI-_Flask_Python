import time
import RPi.GPIO as GPIO
import sound as play
from flask import Flask, render_template, request
app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

#l293d motor
IN1 = 12
IN2 = 16
IN3 = 20
IN4 = 21
#cam motor
IN11 = 26
IN12 = 19

mine =5
minests=1
GPIO.setup(IN11,GPIO.OUT)
GPIO.setup(IN12,GPIO.OUT)
GPIO.setup(IN1,GPIO.OUT)
GPIO.setup(IN2,GPIO.OUT)
GPIO.setup(IN3,GPIO.OUT)
GPIO.setup(IN4,GPIO.OUT)
GPIO.setup(mine,GPIO.IN,pull_up_down=GPIO.PUD_UP)
# Create a dictionary called pins to store the pin number, name, and pin state:
pins = {
   24  : {'name' : 'FORWARD',  'state' : GPIO.LOW},
   25  : {'name' : 'BACKWARD', 'state' : GPIO.LOW},
   20  : {'name' : 'LEFT',     'state' : GPIO.LOW},
   21  : {'name' : 'RIGHT',    'state' : GPIO.LOW},
   26  : {'name' : 'STOP',     'state' : GPIO.LOW},
   16  : {'name' : 'CAMR',  'state' : GPIO.LOW},
   12  : {'name' : 'CAML', 'state' : GPIO.LOW},
   13  : {'name' : 'MON', 'state' : GPIO.LOW}
  }

# Set each pin as an output and make it low:
for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.LOW)


@app.route("/")
def main():
   minests=GPIO.input(mine)
   if(minests==0):
	minests="DETECTED"
   else:
	minests= "NOT DETECTED"
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins,
      'mine' : minests,
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/readPin/<pin>")
def readPin(pin):
   try:
    if GPIO.input(int(pin)) == 0:
         message = "Pin number " + pin + " is high!"
    else:
         message = "Pin number " + pin + " is low!"
   except:
      message = "There was an error reading pin " + pin + "."

   templateData = {
      'pins' : 'Status of Pin' + pin,
      'message' : message
      }

   return render_template('main.html', **templateData)
# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = pins[changePin]['name']
   # If the action part of the URL is "on," execute the code indented below:
   if action == "forward":
      GPIO.output(IN2,GPIO.HIGH)
      GPIO.output(IN1,GPIO.LOW)
      GPIO.output(IN3,GPIO.HIGH)
      GPIO.output(IN4,GPIO.LOW)
      message = "ROBOT MOVING FORWARD"
   if action == "backward":
      GPIO.output(IN2,GPIO.LOW)
      GPIO.output(IN1,GPIO.HIGH)
      GPIO.output(IN3,GPIO.LOW)
      GPIO.output(IN4,GPIO.HIGH)
      message = "ROBOT MOVING BACKWARD"
   if action == "left":
      GPIO.output(IN1,GPIO.LOW)
      GPIO.output(IN2,GPIO.LOW)
      GPIO.output(IN3,GPIO.HIGH)
      GPIO.output(IN4,GPIO.LOW)
      message = "ROBOT MOVING LEFT"
   if action == "right":
      GPIO.output(IN2,GPIO.HIGH)
      GPIO.output(IN1,GPIO.LOW)
      GPIO.output(IN3,GPIO.LOW)
      GPIO.output(IN4,GPIO.LOW)
      message = "ROBOT MOVING RIGHT"
   if action == "stop":
      GPIO.output(IN1,GPIO.LOW)
      GPIO.output(IN2,GPIO.LOW)
      GPIO.output(IN3,GPIO.LOW)
      GPIO.output(IN4,GPIO.LOW)
      message = "ROBOT STOPPED"
   if action =="con":
      GPIO.output(IN11,GPIO.HIGH)
      GPIO.output(IN12,GPIO.LOW)
      time.sleep(0.05)
      GPIO.output(IN11,GPIO.LOW)
      GPIO.output(IN12,GPIO.LOW)
      message = "CAMERA TURNING RIGHT "
   if action =="coff":
      GPIO.output(IN11,GPIO.LOW)
      GPIO.output(IN12,GPIO.HIGH)
      time.sleep(0.05)
      GPIO.output(IN11,GPIO.LOW)
      GPIO.output(IN12,GPIO.LOW)
      message = "CAMERA TURNING LEFT"
   if action =="mon":
      play.playsound()
      message = "PLAYING ALERT SOUND "
   if action == "toggle":
      # Read the pin and set it to whatever it isn't (that is, toggle it):
      GPIO.output(changePin, not GPIO.input(changePin))
      message = "Toggled " + deviceName + "."
   minests=GPIO.input(mine)
   if(minests==0):
	minests="DETECTED"
   else:
	minests="NOT DETECTED"
   # For each pin, read the pin state and store it in the pins dictionary:
   for pin in pins:
      pins[pin]['state'] = GPIO.input(pin)

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'message' : message,
      'pins' : pins,
      'mine' : minests,
   }

   return render_template('main.html', **templateData)


if __name__ == "__main__":
   app.run(host='192.168.43.159', port=80, debug=True)
