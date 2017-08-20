import socket
import urllib2
import json
gps_uri = 'https://www.tgvconnect.com/router/api/train/gps'


TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

#  run this script
#  start "gpsd -N tcp://localhost:5005"
#  connect with any gpsd client such as cgps
#  /!\ work in progress

def get_gps_data():
  
  try:
    req = urllib2.Request(gps_uri)
    response = urllib2.urlopen(req)
    plain = response.read()
    data = json.loads(plain)
  except:
    print "Error fetching gps data"
  
  #data = {
    #'latitude':44,
    #'longitude': -0.1,
    #'altitude': 20,
    #'heading': 230,
    #'speed': 230
    #}
  
  res='''{"class":"TPV","device":"/dev/pts/1",
    "time":"2005-06-08T10:34:48.283Z","ept":0.005,
    "lat":%s,"lon":%s,"alt":%s,
    "eph":36.000,"epv":32.321,
    "track":%s,"speed":%s,"climb":-0.085,"mode":3}'''%(data['latitude'], data['longitude'], data['altitude'], data['heading'], data['speed'])
  return res

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print 'Connection address:', addr
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    print "received data:", data
    tosend = get_gps_data()
    print tosend
    conn.send(tosend)  # echo
print "close"
conn.close()