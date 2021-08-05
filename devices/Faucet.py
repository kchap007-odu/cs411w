import locale
import time
import random
#import Devices

# turn water on/off 


class Faucet:  

    #variables
    Power = ["on", "off"]

    _pressureL: = 0
    _pressureM: = 1
    _pressureH: = 2

    #temperature control 32F - 210F
    _tempCurrent: 0
    _waterusage: 0 

    #Start Functions here:
    def temperature(self):
        return temp(32,210)



    #Pressure function 
    def pressure(self):
        return random(0,2)


  #water usage 
    def waterusage(self):
        return usage(0,100)

   # def 

