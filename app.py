from flask import Flask, send_from_directory, render_template
import requests
import logging
import threading
import time

global turtleObject
app = Flask(__name__)

def start_context_broker_interface(name):
  while True:
    url = "http://orion:1026/v2/entities/urn:ngsi-ld:Motion:001/attrs/turtlePose/value"
    payload={}
    headers = {
      'fiware-service': 'openiot',
      'fiware-servicepath': '/'
    }
    global turtleObject
    turtleObject = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(0.5)

@app.route("/static/<path:path>")
def static_dir(path):
  return send_from_directory("static", path)
  
@app.route("/")
def index():
  return send_from_directory("static", "index.html")

@app.route("/teleoperation_gui")
def teleoperation():
  return send_from_directory("static", "teleoperation_gui.html")
  
@app.route("/turtleValues")
def sendValues():
  global turtleObject
  if hasattr(turtleObject,'text'):
    return turtleObject.text
  elif hasattr(turtleObject,'json()'):
    return turtleObject.json()
  return turtleObject

if __name__ == "__main__":
  global turtleObject
  turtleObject = "empty"
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
  logging.info("Main    : Creating the main thread of the OEE microservice")
  x = threading.Thread(target=start_context_broker_interface, args=["Context Broker Interface"])
  logging.info("Turtlesim Web Gui    : Starting the Context Broker Interface")
  x.start()
  app.run(host='0.0.0.0', port=8080)
  logging.info("Turtlesim Web Guiin    : waiting for the main thread to finish")
  x.join()
  logging.info("Turtlesim Web Gui    : all done")
  
  
  



