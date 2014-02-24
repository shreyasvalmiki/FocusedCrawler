'''
Created on Feb 22, 2014

@author: svalmiki
'''
import sys
from ds import DS
from threading import Thread
from htmlparser import DataParser as DP
from urllib import request as urlrequest
import datetime
from compute import cosine

class CrawlThread(Thread):
    def __init__(self, query):
        Thread.__init__(self)
        self.query = query
        self.filnamePart = "dumps/"+self.query.replace(" ","-")
    
    def stop(self):
        self._stop()
    
    
    '''
    This crawls pages based on priority
    '''
    def run(self):
        while True:
            if not DS.linkQueue.empty():
                url = ""
                try:
                    c,u = DS.linkQueue.get()
                    dt = datetime.datetime.now()
                    fName = self.filnamePart+str(dt.year)+str(dt.month)+str(dt.day)+str(dt.hour)+"t"+self.name
                    f = open(fName,"a", encoding='utf-8')

                    url = u
                    dataParser = DP.DataParser()
                    rawData = urlrequest.urlopen(u).read().decode("utf-8")
                    dataParser.url = u
                    dataParser.feed(rawData)

                    data = str(dataParser.get_data())
                    f.write(data)
                    cos = cosine.get_cosine(self.query, data)
                    
                    links = dataParser.get_links()
                    
                    for l in links:
                        DS.linkQueue.put((-cos,l))
                    f.close()
                    
                    DS.size += (sys.getsizeof(data)/1073741824)
                    DS.count += 1
                    
                    print("Total Count: "+str(DS.count)+"; Total Size: "+str(DS.size)+" GB")
                    
                except:
                    logName = "logs/"+self.query.replace(" ","-") + ".log"
                    logFile = open(logName, "a", encoding='utf-8')
                    logFile.write(str("URL: "+str(url)+"; Error: "+str(sys.exc_info()[0])))
                    logFile.close()
                    pass
                finally:
                    if not f.closed:
                        f.close()