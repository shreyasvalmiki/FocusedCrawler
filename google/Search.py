'''
Created on Feb 15, 2014

@author: svalmiki
'''
import json
import sys
from urllib import parse as urlparse
from urllib import request as urlrequest
from ds import DS

URL = "http://ajax.googleapis.com/ajax/services/search/web?"
RSZ = 8
VERSION = 1.0

class Search:
    def __init__(self,q,size=10):
        self.size = size
        self.q = q
        self.pages = 1
        self.start = 0
    
    def seturls(self):
        searchUrls = []        
        try:            
            if self.size <= RSZ:
                self.pages = 1
            else:
                mod = self.size % RSZ
                tempSize = self.size - mod
                self.pages = int(tempSize/RSZ) + 1 if  mod > 0  else int(tempSize/RSZ)
            
            for page in range(0, self.pages):
                args = {
                        "rsz": RSZ,
                        "q": self.q,
                        "start": page * RSZ,
                        "v": VERSION
                        }
            
                urlArgs = urlparse.urlencode(args)
                rawData = urlrequest.urlopen(URL+urlArgs).read()
                data = json.loads(rawData.decode("utf-8"))
                
                for result in data["responseData"]["results"]:
                    if len(searchUrls) >= self.size:
                        return searchUrls
                    print(result["unescapedUrl"])
                    DS.linkQueue.put((-1.0,result["unescapedUrl"]))
                    searchUrls.append(result["unescapedUrl"])
        except:
            print("Unexpected error:", sys.exc_info()[0])    
        return searchUrls