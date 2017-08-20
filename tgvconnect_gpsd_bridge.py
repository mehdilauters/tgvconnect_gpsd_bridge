import socket
import urllib2
import json
import time
from datetime import datetime
gps_uri = 'https://www.tgvconnect.com/router/api/train/gps'


TCP_IP = ''
TCP_PORT = 5006
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

#  run this script
#  start "gpsd -N tcp://localhost:5005"
#  connect with any gpsd client such as cgps
#  /!\ work in progress

def get_gps_data():
  
  mode = 1
  try:
    req = urllib2.Request(gps_uri)
    response = urllib2.urlopen(req)
    plain = response.read()
    data = json.loads(plain)
    mode = 3
  except:
    print "Error fetching gps data"
  
  #data = {
    #'latitude':44,
    #'longitude': -0.1,
    #'altitude': 20,
    #'heading': 230,
    #'speed': 10
    #}
  
  hour = datetime.now().isoformat()
  res='''{"class":"TPV","device":"/dev/ttyUSB0","mode":%s,"time":"%s","ept":0.005,"lat":%s,"lon":%s,"alt":%s,"epx":9.125,"epy":17.778,"epv":34.134,"track":%s,"speed":%s,"climb":0.000,"eps":36.61}'''%(mode, hour, data['latitude'], data['longitude'], data['altitude'], data['heading'], data['speed'])
  return res

def send_loop(conn):
  while 1:
    #data = conn.recv(BUFFER_SIZE)
    #if not data: break
    #print "received data:", data
    tosend = get_gps_data()
    print tosend
    conn.send(tosend)  # echo
    time.sleep(1)
  print "close"
  conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
send_loop(conn)
