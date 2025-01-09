from classes_.Data_fluid import Fluid_model
from classes_.Data_pipe import pipe
from classes_.Data_temperature import Extern_Temperature
import matplotlib.pyplot as plt
import numpy as np

from single_simulation_code import single_simulation
from presfil_simulation_code import *


import time
start_time = time.time()

fluid = Fluid_model(
    P = 100,#bar  
    T = 80,#C 
    Dg = 0.75,
    Do = 0.846,
    API = 0,
    RGL = 157,# sM^3/sM^3 
    BSW = 0.45, # %
    rate = 1500/86400 # m^3 /s
    ) 

line1 = pipe(Dh = 4*0.0254, e =  0.0001 * 0.0254, L = 500 , angle = 90 ,direction='Uphill' )
line2 = pipe(Dh = 4*0.0254, e =  0.0001 * 0.0254, L = 500 , angle = 0, direction='Uphill' )
line3 = pipe(Dh = 4*0.0254, e =  0.0001 * 0.0254, L = 1500 , angle = 90, direction='Uphill'  )
temp1 = Extern_Temperature(4,80,150,2)
temp2 = Extern_Temperature(22,4,1650,1)
temp3 = Extern_Temperature(22,5.5,1500,1)


lines = [line1,line2,line3]
#lines = [line1]
#temps = [temp1,temp2,temp3]
temps = None
pump_LINE = 1

#'Beggs_Brill': 'Hagedorn':'Bendisken':'Bhagwat':
P1,T1,var1,pump1 = single_simulation(fluid,lines,temps,pump_LINE,'Bhagwat')
#P1,T1,var1,pump1 = simulation(fluid,lines,temps,pump_LINE, vertical='Hagedorn',inclined='Beggs_Brill',horizontal='Beggs_Brill')


print(P1,T1,pump1)


comp = np.arange(0,len(var1[0]),1)
print(comp)
plt.plot(comp,var1[0])
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))

# a = np.arange(0,850.1,0.1)
# print(a[-1])
# print(a)

