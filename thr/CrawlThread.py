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
    
    def run(self):
        print("Inside")
        while True:
            if not DS.linkQueue.empty():
                dt = datetime.datetime.now()
                fName = "dumps/"+str(dt.year)+str(dt.month)+str(dt.day)+str(dt.hour)+str(dt.minute)+"t"+self.name
                print(fName)
                f = open(fName,"a", encoding='utf-8')
                print(DS.linkQueue.qsize())
                
                try:
                    c,u = DS.linkQueue.get()
                    print("Processing (Cos:"+str(c)+" ): "+str(u))
                    
                    dataParser = DP.DataParser()
                    rawData = urlrequest.urlopen(u).read().decode("utf-8")
                    dataParser.url = u
                    dataParser.feed(rawData)

                    data = str(dataParser.get_data())
                    f.write(data)
                    cos = cosine.get_cosine(self.query, data)
                    
                    links = dataParser.get_links()
                    print("\nLinks: ".join(links))
                    
                    for l in links:
                        DS.linkQueue.put((-cos,l))
                    f.close()
                except:
                    print(sys.exc_info()[0])
                    pass
                finally:
                    if not f.closed:
                        f.close()