'''
Created on Feb 15, 2014

@author: svalmiki
'''
import os.path as ospath
import sys
import datetime
import json
from compute import cosine
from ds import DS
from google import Search as Search
from htmlparser import LinkParser as LinkParser
from htmlparser import TextParser as TextParser
from htmlparser import DataParser as DP
from urllib import request as urlrequest
from thr import CrawlThread as CT
from thr import ParentThread as PT


def saveAndQuit(query,pt):
    if input() == 'q':
        setFilename = "save/"+query.replace(" ", "-").lower()+"-s.json"
        queueFilename = "save/"+query.replace(" ", "-").lower()+"-q.json"
        dataFilename = "save/"+query.replace(" ", "-").lower()+"-d.json"
        
        setList = list(DS.linkSet)
        queueList = []
        while not DS.linkQueue.empty():
            queueList.append(DS.linkQueue.get())
        
        setFile = open(setFilename,"w")
        setFile.write(json.dumps(setList))
        setFile.close()
        queueFile = open(queueFilename,"w")
        queueFile.write(json.dumps(queueList))
        queueFile.close()
        
        dataFile = open(dataFilename,"w")
        dataFile.write(json.dumps({"size":DS.size,"count":DS.count}))
        dataFile.close()
        
        pt.stop()
        sys.exit(1)
    else:
        saveAndQuit(query,pt)
 

def setSavedData(query):
    setList = json.load(open("save/"+query.replace(" ", "-").lower()+"-s.json"))
    queueList = json.load(open("save/"+query.replace(" ", "-").lower()+"-q.json"))
    data = json.load(open("save/"+query.replace(" ", "-").lower()+"-d.json"))
    
    DS.linkSet = set(setList)
    for q in queueList:
        DS.linkQueue.put(q)
    
    DS.size = data["size"]
    DS.count = data["count"]


    
query = input("Enter query string: ")

if ospath.isfile("save/"+query.replace(" ", "-").lower()+"-d.json"):
    if input("There exists saved data for this query. Press y to continue. Press any other key to start from beginning: ") == 'y':
        setSavedData(query)

    else:
        startNo = int(input("Enter seed number: "))
        search = Search.Search(query, startNo)
        search.seturls()

else:
    startNo = int(input("Enter seed number: "))
    search = Search.Search(query, startNo)
    search.seturls()

print ('\n')

input("Press any key to start. Once you start, press 'q' to save progress and quit.")

pt = PT.ParentThread(query, DS.threadCount)
pt.start()

print("Crawling...")

saveAndQuit(query, pt)
    
    
# for i in range(startNo):
#     ct = CT.CrawlThread(query)
#     ct.start()


# 
# linkParser = LinkParser.LinkParser()
# for u in urls:
#     linkParser.url = u
#     rawData = urlrequest.urlopen(u).read().decode("utf-8")
#     linkParser.feed(rawData)
#     
#     print('\n'.join(linkParser.getlinks()))
    #print('\n'.join(DS.linkSet))
    
    
    
    
    
# textParser = TextParser.TextParser()
# for u in DS.linkSet:
#     try:
#         rawData = urlrequest.urlopen(u).read().decode("utf-8")
#         textParser.feed(rawData)
#         f = open("testfile.txt","w", encoding='utf-8')
#         data = str(textParser.get_data())
#         f.write(data)
#         print(cosine.get_cosine(query, data))
#         f.close()
#     except:
#         pass
#     finally:
#         if not f.closed:
#             f.close()   

# def updateunreadurls(u):           
#     linkParser.url = u
#     rawData = urlrequest.urlopen(u).read().decode("utf-8")
#     linkParser.feed(rawData)

        
#     
# def crawl(u):    
#     try:
#         dataParser = DP.DataParser()
#         rawData = urlrequest.urlopen(u).read().decode("utf-8")
#         dataParser.feed(rawData)
#         dt = datetime.datetime.now()
#         f = open(str(dt.year)+str(dt.month)+str(dt.day)+str(dt.hour)+str(dt.minute),"a", encoding='utf-8')
#         data = str(dataParser.get_data())
#         f.write(data)
#         cos = cosine.get_cosine(query, data)
#         
#         links = dataParser.getlinks()
#         
#         for l in links:
#             DS.linkQueue.put((l,cos))
#         
#         print()
#         f.close()
#     except:
#         pass
#     finally:
#         if not f.closed:
#             f.close()