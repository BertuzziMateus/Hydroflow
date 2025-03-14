from conversions import *
import numpy as np


def Rsw_pure( fluid_model ) -> float: # scf/bbl
    pressure = Bar_to_psia(fluid_model)
    T = C_to_F(fluid_model)
    
    A = 2.12 + 3.45e-3 * T - 3.59e-5 * T**2
    B = 0.0107 - 5.26e-5 * T + 1.48e-7 * T**2
    C = -8.75e-7 + 3.9e-9 * T - 1.02e-11 * T**2

    rw = A + B*pressure + C*pressure**2
      
    return rw #* 0.17810776923 ? -> sm3/m3

def Bw( fluid_model ) -> float: # bbl/stb
    pressure = Bar_to_psia(fluid_model)
    temperature = C_to_F(fluid_model)
    d_vwt = -1.0001e-2 + (1.33391e-4)*temperature + (5.50654e-7)*temperature**2
    d_vwp =  -(3.58922e-7 + (1.95301e-9)*temperature)*pressure - ( 2.25341e-10 + (1.72834e-13)*temperature )*pressure**2
    return (( 1 + d_vwt)*(1+d_vwp ))

def Water_viscosity( fluid_model ) -> float: #cP
    
    temperature = C_to_F(fluid_model)

    u = np.exp(1.003 - (1.479e-2)*temperature + (1.982e-5)*temperature**2)

    return u

def Water_density( fluid_model ) -> float: #lb/scf
    return (62.4/Bw(fluid_model))#*16.01846337396

def gas_water_interfacial_tension(fluid_model) :

    pressure  = fluid_model.P * 14.503773800722
    temperature_c = fluid_model.T
    temperature_f = temperature_c*(9/5) + 32

    sigma_74 = 75 - 1.108*pressure**0.349
    sigma_280 = 53 - 0.1048*pressure**0.637

    if temperature_f <  74 : 
        sigma_w = sigma_74
    elif (74 < temperature_f < 280):
        sigma_w = sigma_74  + ((temperature_f-74)*(sigma_280-sigma_74))/(280-74)
    else:
        sigma_w = sigma_280

    if sigma_w < 1 :
        sigma_w = 1
    
    return sigma_w*0.001 # n/m