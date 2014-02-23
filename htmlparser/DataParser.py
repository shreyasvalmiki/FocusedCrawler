'''
Created on Feb 15, 2014

@author: svalmiki
'''
from ds import DS
from html.parser import HTMLParser
from urllib.parse import urljoin
import re
import urllib.robotparser as rp

MAX_EXT_LENGTH = 5
HTTPS = "https:"
HTTP = "http:"
MAX_PROTO_LEN = 8
ROBOTS_TXT = "/robots.txt"
escapeExts = [
               #images
               ".jpeg",
               ".jpg",
               ".gif",
               ".png",
               ".bmp",
               ".raw",
               ".tiff",
               ".jfif",
               ".exif",
               ".ico",
               
               
               #videos
               ".mp4",
               ".wmv",
               ".3gp",
               ".ogg",
               ".flv",
               
               
               #audio
               ".mp3",
               ".wma",
               
               
               #text
               ".pdf",
               ".xlsx",
               ".xls",
               ".docx",
               ".doc",
               ".ppt",
               ".pptx",
               ".css",
               ".js",
               ".py",
               
               #executable
               ".exe",
               ".chm",
               ".sh"
               ]

class DataParser(HTMLParser):
    def __init__(self, strict=False):
        HTMLParser.__init__(self, strict)
        self.url = ""
        self.links = []
        self.record = 1
        self.data = ""
    
        
    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'link' or tag == 'style' or tag == 'a':
            self.record = 0
        else:
            self.record = 1
        if tag == 'a':
            for attr, value in attrs:
                if attr == 'href':
                    link = self.filterlink(value)
                    if link != "":
                        if link not in DS.linkSet:
                            DS.linkSet.add(link)
                            self.links.append(link)
        
    def handle_data(self, data):
        #self.f = open("testfile.txt","a") 
        if self.record:
            try:
                #print(data)
                #self.f.write(str(data))
                self.data = self.data + str(data)
            except:
                pass
        
    def handle_endtag(self, tag):
        self.record = 0
    
    
    def getlinks(self):
        return self.links
       
    def filterlink(self, link):
        proto = HTTP
        reFwdSlash = re.compile("^//.*")
        reStartPound = re.compile("^#.*")
        reRelLink1 = re.compile('^[/][a-zA-Z0-9].*')
        reRelLink2 = re.compile('^[a-zA-Z0-9].*')
        reHttps = re.compile("^https://.*")
        #reHttp = re.compile("^http://.*")
        reJavascript = re.compile("^javascript:.*")
        reMailto = re.compile("^mailto:.*")
        #test
        #print("unchanged: "+link)
        
        
        if reHttps.match(self.url):
            proto = HTTPS
        else:
            proto = HTTP
        
        if reStartPound.match(link):
            return ""
        
        if reJavascript.match(link):
            return ""
        
        if reMailto.match(link):
            return ""
        
        isCurrUrlOkay = self.checkrobot(self.url)
        
        
        if reFwdSlash.match(link):
            if not isCurrUrlOkay:
                return ""
            link = proto + link
            
            
        if reRelLink1.match(link) or reRelLink2.match(link):
            link = urljoin(self.url, link)
            #test
            #print("\tAdded Protocol: "+link)
        
        lcLink = link.lower()
        subLink = lcLink[-MAX_EXT_LENGTH:]
        
        for ext in escapeExts:
            if subLink.find(ext) > -1:
                return ""
        #test
        #print("\t\tFinal Link: "+link)
        
        if self.checkrobot(link):
            return link
        else:
            return ""
    
    
    def get_data(self):
        return self.data
    
    
    def get_links(self):
        return self.links 
    
    def checkrobot(self,u):
        try:
            robUrl = u if u.find("/", MAX_PROTO_LEN) == -1 else u[:u.find("/",MAX_PROTO_LEN)]
            robUrl = robUrl + ROBOTS_TXT
            rob = rp.RobotFileParser()
            rob.set_url(robUrl)
            return rob.can_fetch("*", u) 
        except:
            return True         