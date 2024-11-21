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
    P = 150, #bar  
    T = 80,#C 
    Dg = 0.846,
    Do = 0.836,
    API = 0,
    RGL = 150,# sM^3/sM^3 
    BSW = 0.2, # %
    rate = 1500/86400 # m^3 /s
    ) 

line1 = pipe(Dh = 3* 0.0254, e =  0.0005 * 0.0254, L = 1500, angle = 90 ,direction='Ascendente' )
# line2 = pipe(Dh = 3* 0.0254, e =  0.0005 * 0.0254, L = 867 , angle = 10, direction='Ascendente' )
# line3 = pipe(Dh = 3* 0.0254, e =  0.0005 * 0.0254, L = 1500 , angle = 90, direction='Ascendente'  )
# # temp1 = Extern_Temperature(6,80,150,2)
# # temp2 = Extern_Temperature(22,6,1650,1)
# # temp3 = Extern_Temperature(22,9,1500,1)


lines = [line1]
temps = None
pump_LINE = 0


# # P0,T0,var0,pump0 = single_simulation(fluid,lines,temps,pump_LINE,"BB")
P1,T1,var1,pump1 = single_simulation(fluid,lines,temps,pump_LINE,'Homogeneous')

comp = np.arange(0,len(var1[0]),1)
print(comp)
plt.plot(comp,var1[0])
plt.show()

print("--- %s seconds ---" % (time.time() - start_time))

# a = np.arange(0,850.1,0.1)
# print(a[-1])
# print(a)
