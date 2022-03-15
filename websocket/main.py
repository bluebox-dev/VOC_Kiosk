# Websocket
import asyncio
import websockets
import json

# GPIO
import time
import RPi.GPIO as GPIO

# Camera
import cv2
import pygame

# Take Image
def camera(point):
    datetime = time.strftime("%d%m%Y_%H:%M%H:%M")
    camera = cv2.VideoCapture(0)
    for i in range(1):
        ret,image = camera.read()
        cv2.imwrite('user'+str(datetime)+"_point_"+str(point)+'.png', image)
    camera.release()
    cv2.destroyAllWindows()

# Take Music Thx
def music():
  pygame.mixer.init()
  pygame.mixer.music.load("myFile.wav")
  pygame.mixer.music.play()

# Initial the input pin
def initialInductive(sensor1,sensor2,sensor3,sensor4,sensor5):
  global GPIOsensor1,GPIOsensor2,GPIOsensor3,GPIOsensor4,GPIOsensor5
  GPIOsensor1 = sensor1
  GPIOsensor2 = sensor2
  GPIOsensor3 = sensor3
  GPIOsensor4 = sensor4
  GPIOsensor5 = sensor5
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOsensor1,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOsensor2,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOsensor3,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOsensor4,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(GPIOsensor5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  print("Finished Initiation")

# Detect Metal
def detectMetal(GPIOsensor,point):
    state = GPIO.input(GPIOsensor)
    if state == 0:
      print("Metal Detected")
      asyncio.run(wss("orderIDReference",point))
      # camera()
    else :
      print("Metal Not Detected")

# Websocket
async def wss(orderIDReference,point):
    uri = "wss://iqy8xudwxl.execute-api.ap-southeast-1.amazonaws.com/unitTest"
    async with websockets.connect(uri) as websocket:
        event = {"action": "sendPrivate","companyID": orderIDReference,"amountScore": point}
        await websocket.send(json.dumps(event))


if __name__ == "__main__":
    # Pin of Input
    GPIOsensor1 = -1
    GPIOsensor2 = -1
    GPIOsensor3 = -1
    GPIOsensor4 = -1
    GPIOsensor5 = -1

    #  Pin of Sensor
    pin1 = 26
    pin2 = 19
    pin3 = 13
    pin4 = 6
    pin5 = 5

    initialInductive(pin1,pin2,pin3,pin4,pin5)

    while True:
        detectMetal(GPIOsensor1,1)
        # detectMetal(GPIOsensor2,2)
        # detectMetal(GPIOsensor3,3)
        # detectMetal(GPIOsensor4,4)
        # detectMetal(GPIOsensor5,5)
        time.sleep(0.2)