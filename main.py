'''
Created on Feb 15, 2014
Modified on Sep 12, 2019
@author: svalmiki

'''
import os.path as ospath
import sys
import json
from ds import DS
from google import Search as Search
from thr import ParentThread as PT

'''
Saves progress and stops all threads
'''
def sAndQ(filename, pt):
    pt.stop()
    setFilename = filename+"-s.json"
    queueFilename = filename+"-q.json"
    dataFilename = filename+"-d.json"
    
    setList = list(DS.linkSet)
    queueList = []
    while not DS.linkQueue.empty():
        c,d = DS.linkQueue.get()
        queueList.append((c,d))
    
    setFile = open(setFilename,"w")
    setFile.write(json.dumps(setList))
    setFile.close()
    
    queueFile = open(queueFilename,"w")
    queueFile.write(json.dumps(queueList))
    queueFile.close()
    
    dataFile = open(dataFilename,"w")
    dataFile.write(json.dumps({"size":DS.size,"count":DS.count}))
    dataFile.close()
    
    sys.exit(1)
        
def saveAndQuit(filename,pt):
    if input() == 'q':
        sAndQ(filename,pt)
    else:
        saveAndQuit(filename,pt)
 
'''
Gets saved data
'''
def setSavedData(filename):
    setList = json.load(open(filename+"-s.json"))
    queueList = json.load(open(filename+"-q.json"))
    data = json.load(open(filename+"-d.json"))
    
    DS.linkSet = set(setList)
    for q in queueList:
        DS.linkQueue.put((q[0],q[1]))
    
    DS.size = data["size"]
    DS.count = data["count"]




query = input("Enter query string: ")

saveFilename = "save/"+query.replace(" ", "-").lower()

if ospath.isfile(saveFilename+"-d.json"):
    if input("There exists saved data for this query.\nPress 'y' to continue. Press any other key to start from beginning: ") == 'y':
        setSavedData(saveFilename)

    else:
        startNo = int(input("Enter seed number: "))
        search = Search.Search(query, startNo)
        search.seturls()

else:
    startNo = int(input("Enter seed number: "))
    search = Search.Search(query, startNo)
    search.seturls()

print ('\n')

initCount = DS.count

limit = 1000
withLimit = False
if input("Do you want to add a limit? Answer 'y' for yes else press any button: ") == 'y':
    limit = int(input("Enter limit: "))
    withLimit = True
    input("Press any key to start.")
else:
    input("Press any key to start. Once you start, press 'q' at any point in time to save progress and quit.")


pt = PT.ParentThread(query, DS.threadCount)
pt.start()

print("\n\nCrawling...")

if withLimit:
    while True:
        if DS.count >= (limit + initCount):
            sAndQ(saveFilename,pt)
            break
else:
    saveAndQuit(saveFilename, pt)