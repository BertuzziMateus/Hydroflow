import numpy as np
from scipy.optimize import fsolve

def reynolds_homo( Flow_info, line) -> float:
    return  ((Flow_info.mix_rho*Flow_info.vm*line.Dh)/Flow_info.mix_viscosity)

def F_homo( Flow_info, line ) -> float:

    def f(F):
        return ((- 2*np.log10( ( (line.e/line.Dh) / (3.7) ) + ( 2.51 / ( reynolds_homo(Flow_info,line)*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]
    return F

def frictional_gradient_homo(Flow_info, line) -> float:
    return ( F_homo(Flow_info, line )*( (Flow_info.mix_rho*Flow_info.vm**2)/(2*line.Dh) ) )

def gravitational_gradient_homo(Flow_info, line) -> float:
    if line.direction == "Descendente":
        angle = line.angle*-1
    else:
        angle = line.angle
        
    grav = Flow_info.mix_rho*9.81*np.sin(angle)

    return grav

def Flow_mass_mix_homo(Flow_info) ->  float:
    mass_flow = Flow_info.flow_liquid_mass*Flow_info.λl + Flow_info.flow_gas_mass*( 1 - Flow_info.λl) # kg /s
    return mass_flow

def title_homo(Flow_info) -> float:
    return (Flow_info.flow_gas_mass / Flow_mass_mix_homo(Flow_info))


def kinetic_dl_t(Flow_info, line) -> float: # em função de Dp/dl total
    A = ((Flow_mass_mix_homo(Flow_info))**2)*title_homo(Flow_info) / (line.area**2)
    B = (Flow_info.MM) / (8.314462*(Flow_info.T +  273.15)*Flow_info.gas_rho**2)
    valor = A*B
    #valor = 0
    return valor

def total_gradient_homogeneous(Flow_info, line)-> float:
    partial = frictional_gradient_homo(Flow_info,line) + gravitational_gradient_homo(Flow_info,line)
    return (partial/ (1 - kinetic_dl_t(Flow_info,line) ))
