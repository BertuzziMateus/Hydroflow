import numpy as np
import matplotlib.pyplot as plt
from classes_.Data_fluid import *
from classes_.Data_pipe import *
from classes_.Data_temperature import *
from single_simulation_code import *
import pandas as pd
from presfil_simulation_code import*


fluid = Fluid_model(
    P = 223.128, #bar  
    T = 80,#C 
    Dg = 0.7,
    Do = 0,
    API = 32.8,
    RGL = 138.033,# sM^3/sM^3 
    BSW = 0, # %
    rate = 647.87/86400 # m^3 /s
    ) 

line1 = pipe(Dh = 2.441* 0.0254, e =  0.0001 * 0.0254, L = 2150, angle = 90 ,direction='Uphill' )

temp1 = Extern_Temperature(T1 = 15, T2 = 80, H = 2150, TEC = 12.5)

#'Beggs_Brill'
Modelos = ['Hagedorn','Beggs_Brill']
results = dict([(models,()) for models in Modelos])

print(results)

for models in Modelos:

    custom_style = {
            'font.size': 12,
            'axes.labelsize': 14,
            'axes.titlesize': 16,
            'axes.linewidth': 1.5,
            'xtick.labelsize': 12,
            'ytick.labelsize': 12,
            'lines.linewidth': 2,
            'lines.markersize': 6,
            'legend.fontsize': 12,
            'legend.frameon': False,
            'legend.loc': 'best',
            'figure.figsize': (8, 6),
            'savefig.dpi': 600,
            'savefig.bbox': 'tight',
        }
    plt.rcParams.update(custom_style)

    temp,press,var,pump = single_simulation(fluid,[line1],[temp1],0,models)

    results[models] = temp,press

    pressures = var[0]
    temperatures = var[1]
    Hl = var[2]
    

    lenght = np.linspace(0,len(pressures),len(pressures))

    plt.plot(lenght, Hl, label=f'{models} Hl')
    plt.xlim(0, lenght[-1])
    plt.xticks(np.linspace(0, lenght[-1], num=10))
    plt.xlabel('Length pipe [m]')
    plt.ylabel('Holdup (Hl)')
    plt.title('Fluid Holdup across the pipe')
    plt.grid(alpha=0.5)
    plt.legend()
    plt.show()

for models in Modelos:

    print('')
    print(f'The finals results for {models} are:')
    print(f'Pressure:  {round(results[models][1],3)} bar')
    print(f'Temperature:  {round(results[models][0],3)} C')
    print(f'Pump:  {round(pump,3)} bar')
    print('')








