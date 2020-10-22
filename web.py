import httplib, urllib
import time

def sensorUpload(field,value):
    params = urllib.urlencode({field: value,'key':'HH0RA7I7QU2V3LHW'})
    headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("api.thingspeak.com:80")
    try:
        conn.request("POST", "/update", params, headers)
        response = conn.getresponse()
        print (value)
        print (response.status, response.reason)
        data = response.read()
        conn.close()
    except:
        print ("Connection Failed")
        
