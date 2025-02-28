import numpy as np
import matplotlib.pyplot as plt
from classes_.Data_fluid import *
from classes_.Data_pipe import *
from classes_.Data_temperature import *
from single_simulation_code import *
import pandas as pd
from presfil_simulation_code import*

import time
start_time = time.time()

fluid = Fluid_model(
    P = 435, #bar  
    T = 85,#C 
    Dg = 0.72,
    Do = 0,
    API = 29,
    RGL = 319,# sM^3/sM^3 
    BSW = 0.2, # %
    rate = 3400/86400 # m^3 /s
    ) 

line1 = pipe(Dh = 4.9* 0.0254, e =  0.0001 * 0.0254, L = 2800, angle = 90 ,direction='Uphill' )



#Hagedorn = single_simulation(fluid,[line1],None,0,'Hagedorn')

Beggs_brill = single_simulation(fluid,[line1],None,0,'Beggs_Brill')

#print(Hagedorn[1])
print('')
print(Beggs_brill[1])

