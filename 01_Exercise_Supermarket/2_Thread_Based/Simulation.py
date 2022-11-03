import os

from ClassCustomer import *
from ClassStation import *
from threading import Thread
from ClassUtility import *
import time

#--------------------------------------------------------------------------------------------------- File handling
directory_path = os.getcwd()
f   = open(directory_path + "\\01_Exercise_Supermarket\\2_Thread_Based\data\supermarkt.txt", "w")
fc  = open(directory_path + "\\01_Exercise_Supermarket\\2_Thread_Based\data\supermarkt_customer.txt", "w")
fs  = open(directory_path + "\\01_Exercise_Supermarket\\2_Thread_Based\data\supermarkt_station.txt", "w")


def my_print(msg):
  """
  #### print on console and into supermarket log
  """
  print(msg)
  f.write(msg + '\n')
        
class AddCustomer(Thread):
  '''
  #### Creates a new customer every durationTime seconds
  '''
  def __init__(self, einkaufsliste, name, sT, dT, mT):
    Thread.__init__(self)
    self.einkaufsliste = einkaufsliste
    self.name = name
    self.name_count = 1
    self.startTime = sT
    self.durationTime = dT
    self.maxTime = mT
  
  def run(self):
    
    # wait until startTime  
    time.sleep(self.startTime / utility.debug_factor)
    
    while(True):
      # create new customer
      kunde = Customer(list(self.einkaufsliste), self.name + str(self.name_count))
      kunde.start()
      self.name_count += 1
      # wait until next customer
      time.sleep(self.durationTime / utility.debug_factor)
      # check if maxTime is reached
      self.maxTime -= self.durationTime
      if(self.maxTime <= 0):
        print("| INFO     |           | >>> AddCustomer Thread terminated")
        break


def printHeader():
    #print("------ Simulation started -------")
    print("|-------------------------------------------------------------")
    print("| Element  |     Value | Action                               ")
    print("|-------------------------------------------------------------")


def printLine():
    print("|-------------------------------------------------------------")

        
printHeader()

# ----------------- create stations -----------------
baecker = Station(10, 'Bäcker')
baecker.start()
utility.allStations.append(baecker)
metzger = Station(30, 'Metzger')
metzger.start()
utility.allStations.append(metzger)
kaese = Station(60, 'Käse')
kaese.start()
utility.allStations.append(kaese)
kasse = Station(5, 'Kasse')
kasse.start()
utility.allStations.append(kasse)

printLine()

Customer.served['Bäcker'] = 0
Customer.served['Metzger'] = 0
Customer.served['Käse'] = 0
Customer.served['Kasse'] = 0
Customer.dropped['Bäcker'] = 0
Customer.dropped['Metzger'] = 0
Customer.dropped['Käse'] = 0
Customer.dropped['Kasse'] = 0

einkaufsliste1 = [(10, baecker, 10, 10), (30, metzger, 5, 10), (45, kaese, 3, 5), (60, kasse, 30, 20)]
einkaufsliste2 = [(30, metzger, 2, 5), (30, kasse, 3, 20), (20, baecker, 3, 20)]

# ----------------- create customers -----------------
createCustomerAThread = AddCustomer(einkaufsliste1, 'A', 0, 200, 400)
createCustomerBThread = AddCustomer(einkaufsliste2, 'B', 0, 60, 120)

#createCustomerAThread = AddCustomer(einkaufsliste1, 'A', 0, 200, 30 * 60 + 1)
#createCustomerBThread = AddCustomer(einkaufsliste2, 'B', 0, 60, 30 * 60 + 1)

starttime = time.time_ns()
createCustomerAThread.start()
createCustomerBThread.start()


utility.endSimulationEv.wait()
endtime = time.time_ns()
duration = endtime - starttime #@todo before terminating tasks? (Overload)
#@todo printout stats

print("| >>> Main Thread terminated")
print("| >>> INFO: Simulation ended after " + str(duration / 1000000000) + " seconds")
printLine()

#--------------------------------------------------------------------------------------------------- Print Customer log
my_print('| Simulationsende: ')#%is' % EventQueue.time)
my_print('| Anzahl Kunden: %i' % (Customer.count))
my_print('| Anzahl vollständige Einkäufe %i' % Customer.complete)
