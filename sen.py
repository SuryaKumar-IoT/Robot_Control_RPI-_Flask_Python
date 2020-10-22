import spidev
import time
import web

class MCP3208:
        def __init__(self, spi_channel=0):
                self.spi_channel = spi_channel
                self.conn = spidev.SpiDev(0, spi_channel)
                self.conn.max_speed_hz = 1000000 # 1MHz
 
        def __del__( self ):
                self.close
 
        def close(self):
                if self.conn != None:
                        self.conn.close
                        self.conn = None
 
        def bitstring(self, n):
                s = bin(n)[2:]
                return '0'*(8-len(s)) + s
 
        def read(self, adc_channel=0):
                # build command
                cmd  = 128 # start bit
                cmd +=  64 # single end / diff
                if adc_channel % 2 == 1:
                        cmd += 8
                if (adc_channel/2) % 2 == 1:
                        cmd += 16
                if (adc_channel/4) % 2 == 1:
                        cmd += 32
 
                # send & receive data
                reply_bytes = self.conn.xfer2([cmd, 0, 0, 0])
 
                #
                reply_bitstring = ''.join(self.bitstring(n) for n in reply_bytes)
                reply = reply_bitstring[7:19]
                return int(reply, 2)
 
if __name__ == '__main__':
        spi = MCP3208(0)
	count = 0
        a0 = 0
        a1 = 0
        a2 = 0
         
        while True:
                count += 1
                a0 += spi.read(0)
                a1 += spi.read(1)
                a2 += spi.read(2)
                 
                if count == 10:
                        a0=8+a0/400
			a0=a0*2
			a1=a1/100
			a2=a2/100
			
			print "ch0=%04d, ch1=%04d, ch2=%04d" % (a0, a1, a2)
			
			#RETRIEVING TEMPERATURE SENSOR DATA
			print "Uploading Sensor1"
			web.sensorUpload("field1",a0)
                        
			#RETRIEVING pH SENSOR DATA 
			print "Uploading Sensor2"
                        web.sensorUpload("field2",a1)
			
			#RETRIEVING MOISTURE SENSOR DATA
			print "Uploading Sensor3"
                        web.sensorUpload("field3",a2)
			
			count = 0
                        a0 = 0
                        a1 = 0
                        a2 = 0
                     
