'''
Created on Feb 22, 2014

@author: svalmiki
'''
from thr import CrawlThread as CT
from threading import Thread
from ds import DS
import json
import sys
'''
This creates crawler threads
'''
class ParentThread(Thread):
    def __init__(self, query, totalCount, limit = 1000):
        Thread.__init__(self)
        self.totalCount = totalCount
        self.query = query
        self.filename = "save/"+query.replace(" ", "-").lower()
        self.cts = []
        self.limit = limit
    
    def stop(self):
        for ct in self.cts:
            ct.stop()
        self._stop()
       
        
    def run(self):
        for i in range(self.totalCount):
            ct = CT.CrawlThread(self.query)
            ct.start()
            self.cts.append(ct)
            