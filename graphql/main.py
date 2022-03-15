# Graphql
import json
import requests
# GPIO
import time
import RPi.GPIO as GPIO
# Camera
import cv2

# Take Image
def camera(point):
    datetime = time.strftime("%d%m%Y_%H:%M%H:%M")
    camera = cv2.VideoCapture(0)
    for i in range(1):
        ret,image = camera.read()
        cv2.imwrite('user'+str(datetime)+"_point_"+str(point)+'.png', image)
    camera.release()
    cv2.destroyAllWindows()

# Post Graphql
def post_point(orderIDReference,point):
    accessToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySUQiOiJVU0VSX1ZIVmxJRTFoY2lBd09DQXlNREl5SURBNE9qVXlPalUwSUVkTlZDc3dNREF3SUNoRGIyOXlaR2x1WVhSbFpDQlZibWwyWlhKellXd2dWR2x0WlNrNlYwUjNhWEE9IiwidXNlcm5hbWUiOiJib3RfdW5pdF90ZXN0IiwidXNlclJvbGUiOiJPV05FUiIsInBob25lTnVtYmVyIjoiMDk0NjYwMTM0MyIsIm5hbWUiOiJib3RfdW5pdF90ZXN0IiwiY29tcGFueUlEIjoiQ09NUEFOWV9WSFZsSUUxaGNpQXdPQ0F5TURJeUlEQTRPalV5T2pJeklFZE5WQ3N3TURBd0lDaERiMjl5WkdsdVlYUmxaQ0JWYm1sMlpYSnpZV3dnVkdsdFpTazZOako1UzNBPSIsInR5cGVUb2tlbkF1dGgiOiJhY2Nlc3MiLCJpYXQiOjE2NDY3MzI2NjAsImV4cCI6MTY0NjgxOTA2MH0.QRbOoeNHL5BRqPQK_gDImngwFYDCLZQBTN3M2gqZpoc"

    endpoint = f"https://tznjouqyk7.execute-api.ap-southeast-1.amazonaws.com/dev/graphql"
    headers = {"Authorization": f"Bearer {accessToken}"}

    query = """mutation CreateVocScoreTransaction($input: CreateVocScoreTransactionInput!) {
  createVocScoreTransaction(input: $input) {
    res_code
    res_desc
    companyID
    transactionNo
    orderIDReference
    amountScore
    typeScore
    createdAt
    updatedAt
  }
}
"""
    variable = {"input":{"orderIDReference": "orderIDReference","amountScore": point }}
    r = requests.post(endpoint, json={"query": query,"variables":variable}, headers=headers)
    if r.status_code == 200:
        with open('log_api.json', 'a+') as f:
          json.dump(r.json()['data']['createVocScoreTransaction'], f,indent=1)
    else:
        raise Exception(f"Query failed to run with a {r.status_code}.")

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
      # post_point("orderIDReference",point)
      # camera()
    else :
      print("Metal Not Detected")


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