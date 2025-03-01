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
    P = 102.41, #bar  
    T = 76,#C 
    Dg = 0.78,
    Do = 0,
    API = 15.6,
    RGL = 66.63,# sM^3/sM^3 
    BSW = 0.604, # %
    rate = 17.10/86400 # m^3 /s
    ) 

line1 = pipe(Dh = 1.995* 0.0254, e =  0.00001 * 0.0254, L = 1025, angle = 90 ,direction='Uphill' )



#Hagedorn = single_simulation(fluid,[line1],None,0,'Hagedorn')

Beggs_brill = single_simulation(fluid,[line1],None,0,'Beggs_Brill')

#print(Hagedorn[1])
print('')
print(Beggs_brill[1])

