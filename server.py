#!/usr/bin/python
import socket
import threading
import BaseHTTPServer
import max31856
import RPi.GPIO as GPIO
import sys
import time
import json

sensors=[]


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
		temps = {}
		i=0;
		for sensor in sensors:
			temps["zone{}".format(i)] = sensor.lastTempC
			i=i+1
		response = "{}".format(json.JSONEncoder().encode(temps))
		self.send_response(200)
		self.send_header("Content-Type", "applicaiton/json")
		self.send_header("Content-Length", str(len(response)))
		self.end_headers()
		self.wfile.write(response)


def maxPollingWorker(sensors):
	while True:
                for sensor in sensors:
                    try:
		        thermoTempC = sensor.readThermocoupleTemp()
		        thermoTempF = (thermoTempC * 9.0/5.0)+32
                    except Exception:
                        thermoTempC = 0
                        thermoTempF = 0
		time.sleep(1)

if __name__ == "__main__":
	# Port 0 means to select an arbitrary unused port
	HOST, PORT = "localhost", 1856
        GPIO.setmode(GPIO.BCM)
	server = BaseHTTPServer.HTTPServer((HOST, PORT), RequestHandler)
	ip, port = server.server_address

	# Start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target=server.serve_forever)
	# Exit the server thread when the main thread terminates
	server_thread.daemon = True


	csPin = 8
	misoPin = 9
	mosiPin = 10
	clkPin = 11
	sensors.append(max31856.max31856(csPin,misoPin,mosiPin,clkPin))
	csPin = 17
	sensors.append(max31856.max31856(csPin,misoPin,mosiPin,clkPin))
	csPin = 27
	sensors.append(max31856.max31856(csPin,misoPin,mosiPin,clkPin))
	csPin = 22
	sensors.append(max31856.max31856(csPin,misoPin,mosiPin,clkPin))

	p=threading.Thread(name="PollingThread",target=maxPollingWorker, args=(sensors,))
	p.daemon=True

	server_thread.start()
	p.start()

	try:
		while True:
			p.join(250)
			if not p.isAlive():
				break
	except KeyboardInterrupt:
		print "Cleaining up GPIO and exiting."
		GPIO.cleanup()
		server.shutdown()
		server.server_close()
		sys.exit(0)
	
	#thermoTempC = max.readThermocoupleTemp()
	#thermoTempF = (thermoTempC * 9.0/5.0) + 32
	#print "Thermocouple Temp: %f degF" % thermoTempF
	#juncTempC = max.readJunctionTemp()
	#juncTempF = (juncTempC * 9.0/5.0) + 32
	#print "Cold Junction Temp: %f degF" % juncTempF
	#GPIO.cleanup()
