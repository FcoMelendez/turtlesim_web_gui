from flask import Flask, send_from_directory, render_template
import requests
import logging
import threading
import time

turtleObject = ""

def start_context_broker_interface(name):
  while True:
    url = "http://localhost:1026/v2/entities/urn:ngsi-ld:Motion:001/attrs/turtlePose/value"
    payload={}
    headers = {
      'fiware-service': 'openiot',
      'fiware-servicepath': '/'
    }
    global turtleObject
    turtleObject = requests.request("GET", url, headers=headers, data=payload)
    time.sleep(0.25)

app = Flask(__name__)

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
  return turtleObject.text

# GET requests will be blocked
@app.route("/notify", methods=['POST'])
def json_example():
    request_data = request.get_json()
    print(request_data)
    print("Hello")

if __name__ == "__main__":
  format = "%(asctime)s: %(message)s"
  logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
  logging.info("Main    : Creating the main thread of the OEE microservice")
  x = threading.Thread(target=start_context_broker_interface, args=["Context Broker Interface"])
  logging.info("Main    : Starting the Context Broker Interface")
  x.start()
  app.run(host='0.0.0.0', port=8080)
  logging.info("Main    : waiting for the main thread to finish")
  x.join()
  logging.info("Main    : all done")
  
  
  



