import random

#temperature of hot water
th = 140

#temperature of input cold water
#generated randomly
tc = random.randint(60,81)
#print (random.randint(60,81))

#performance ratio
pr = 0.9

#volume

print("Enter the capacity of water heater")
string = input()

print(string)

v = float(string)

#string = input("Enter the capacity of water heater")

#Specific heat of water
c = 4.187


deltaT = th-tc

#energy in kWh
E = 0



'''
E = C*V*DeltaT/PR

Where E = energy in kWh

C = Specific heat of water - 4.187 kJ/kgK, or 1,163 Wh/kg°C

V = volume of water to heat

deltaT = Th-Tc

Th = temperature of hot water

Tc = temperature of input cold water
'''