from heapq import heappush, heappop, heapify
import os

# class consists of
# q: event queue
# time: current time
# evCount: counter of all popped events
# methods push, pop, and start as described in the problem description

class EventQueue:
    
  def __init__(self):
    self.q = []
    self.time = 0
    self.evCount = 0

    heapify(self.q)

  def push(self, ev):
    heappush(self.q, ev)


  def pop(self):
    ev = heappop(self.q)
    self.time = ev.t
    self.evCount += 1
    return 

  def start(self):
    while len(self.q) > 0:
      ev = self.pop()
      ev.process(self)
      
  def __str__(self):
    return "%s" % str(self.q)
    