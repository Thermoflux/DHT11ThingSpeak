"""
Humidity and Temperature data logging script.
For ANLY 510 class
Anurag Kotha

Based on below sketch.
Temperature/Humidity Light monitor using Raspberry Pi, DHT11, and photosensor 
Data is displayed at thingspeak.com
2015/06/15
SolderingSunday.com

Based on project by Mahesh Venkitachalam at electronut.in

"""


# Import all the libraries we need to run
import sys
import os
import time
import Adafruit_DHT
import urllib2



pwd = "/home/pi/TempHum/"
DEBUG = 0
# Setup the pins we are connect to
DHTpin = 4

#Setup our API and delay
myAPI = "UUQ0WS05R5PB9VV6"
myDelay = 45 #how many seconds between posting data

# File name for data logging
fname = pwd + 'TemHumLog_'+time.strftime("%d%m%Y", time.gmtime()) + '.csv'
# File name for error recovery
fErrRec = pwd + 'TempHumErrorStatus.log'

def getSensorData():
    RHW, TW = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHTpin)
    
    #Convert from Celius to Farenheit
    TWF = 9/5*TW+32
   
    # return dict
    return (str(RHW), str(TW),str(TWF))

# main() function
def main():
    
    print 'starting... '

    baseURL = 'https://api.thingspeak.com/update?api_key=%s' % myAPI
    print baseURL
    
    while True:
        
		try:
			
			# Log data to file
            mData = "%s,%s,%s,%s\n" %(mTime,TW,TWF,RHW)
            logfile = open(fname,'a',0)
            logfile.write(mData)
            logfile.close()
            
	    	# Log error status to file
            logfile = open(fErrRec,'w',0)
            logfile.write("1\n")
            logfile.close()
			try: 
				
            	mTime = time.strftime("%d/%m/%Y %H:%M:%S", time.gmtime())
            	RHW, TW, TWF = getSensorData()

            	# Send data to ThingSpeak takes some time to open the connection
            	f = urllib2.urlopen(baseURL + 
                                "&field1=%s&field2=%s&field3=%s" % (TW, TWF, RHW)+
                                "&field4=%s" % ("1"))

            	print f.read()
            	print TW + " " + TWF+ " " + RHW + " " + "1"
            	f.close()
			except:
				
				# Log error status to file
	            logfile = open(fErrRec,'w',0)
    	        logfile.write("0")
        	    logfile.close()
            	print 'Failed to connect to the server.'

            
			time.sleep(int(myDelay))

        except:
            # Log error status to file
            logfile = open(fErrRec,'w',0)
            logfile.write("0\n")
            logfile.close()
            print 'Exception caught'
            # break  		  Dont want to exit everytime we loose network connection.

# call main
if __name__ == '__main__':
    main()
