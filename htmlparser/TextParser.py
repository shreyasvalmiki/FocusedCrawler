'''
Created on Feb 15, 2014

@author: svalmiki
'''
from html.parser import HTMLParser
from urllib.parse import urlparse
class TextParser(HTMLParser):
    def __init__(self, strict=False):
        HTMLParser.__init__(self, strict)
        self.record = 1
        self.f = object
        self.data = ""
    def handle_starttag(self, tag, attrs):
        self.record = 1
        if tag == 'script' or tag == 'link' or tag == 'style' or tag == 'a':
            self.record = 0
        
    def handle_data(self, data):
        #self.f = open("testfile.txt","a") 
        if self.record:
            try:
                #print(data)
                #self.f.write(str(data))
                self.data = self.data + str(data)
            except:
                pass
    def get_data(self):
        return self.data
    
    def handle_endtag(self, tag):
        self.record = 0
        #self.f.close()