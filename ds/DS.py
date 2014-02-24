'''
Created on Feb 19, 2014

@author: svalmiki
'''
from queue import PriorityQueue
from queue import Queue

linkQueue = PriorityQueue()

linkSet = set()

unreadLinks = Queue()

count = 0

size = 0.0

threadCount = 20