'''
Created on Feb 15, 2014

@author: svalmiki
'''
import datetime
from compute import cosine
from ds import DS
from google import Search as Search
from htmlparser import LinkParser as LinkParser
from htmlparser import TextParser as TextParser
from htmlparser import DataParser as DP
from urllib import request as urlrequest
from thr import CrawlThread as CT
from thr import ParentThread as PT

query = input("Enter query string: ")
startNo = int(input("Enter seed number: "))

search = Search.Search(query, startNo)
search.seturls()

print ('\n')


pt = PT.ParentThread(query, startNo)
pt.start()
# 
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

        
    
def crawl(u):    
    try:
        dataParser = DP.DataParser()
        rawData = urlrequest.urlopen(u).read().decode("utf-8")
        dataParser.feed(rawData)
        dt = datetime.datetime.now()
        f = open(str(dt.year)+str(dt.month)+str(dt.day)+str(dt.hour)+str(dt.minute),"a", encoding='utf-8')
        data = str(dataParser.get_data())
        f.write(data)
        cos = cosine.get_cosine(query, data)
        
        links = dataParser.getlinks()
        
        for l in links:
            DS.linkQueue.put((l,cos))
        
        print()
        f.close()
    except:
        pass
    finally:
        if not f.closed:
            f.close()