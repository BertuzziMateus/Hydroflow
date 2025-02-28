import numpy as np
from scipy.optimize import fsolve

g = 9.81


def bendiksen( Flow_info,  tubing ) -> list:
    if tubing.direction == "Downhill":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    froude = abs(Flow_info.vm) / ((g*tubing.Dh)**(0.5))
    if froude < 3.5: 
        C0 = 1.05 + 0.15*np.sin(angle)
        vd = ((g*tubing.Dh*(1 - Flow_info.gas_rho/Flow_info.liquid_rho))**(0.5))*( 0.35*np.sin(angle) + 0.54*np.cos(angle) )
    else:
        C0 = 1.2
        vd = 0.35*((g*tubing.Dh*(1 - Flow_info.gas_rho/Flow_info.liquid_rho))**(0.5))*np.sin(angle)

    return [C0,vd]

def drift_infos_bendisken( Flow_info, tubing, ) -> list[float]:


    C0,vd = bendiksen(Flow_info, tubing)
    vsg = (C0*Flow_info.vm  + vd) * (1 - Flow_info.λl )
    vsl = ( 1 - (1 - Flow_info.λl )*C0 )*Flow_info.vm - ( (1 - Flow_info.λl )*vd )
    vm = (vsg+vsl)

    Hl = vsl / vm       
    if Hl > 1:
        Hl = 1
    elif Hl < 0 :
        Hl = 0       
    mix_rho = Hl*Flow_info.liquid_rho + ( 1 - Hl )*Flow_info.gas_rho
    mix_viscosity = Hl*Flow_info.liquid_viscosity + ( 1 - Hl )*Flow_info.gas_viscosity
    

    return [vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd]

def reynolds_bendisken( Flow_info, tubing ) -> float:
    vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos_bendisken(Flow_info,tubing)
    re = (mix_rho*vm*tubing.Dh)/mix_viscosity
    return  re

def F_bendiksen( Flow_info, tubing,  )  -> float:
    re = reynolds_bendisken(Flow_info,tubing)
    def f(F):
        return ((- 2*np.log10( ( (tubing.e/tubing.Dh) / (3.7) ) + ( 2.51 / ( re*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]

    return F

def mass_flow_mix_bendisken( Flow_info, tubing) -> float:
    Hl = drift_infos_bendisken(Flow_info,tubing)[3]
    return ( (Flow_info.flow_liquid_mass * Hl) + Flow_info.flow_gas_mass*(1-Hl) )

def titulo_bendisken( Flow_info, tubing) -> float:
    return (Flow_info.flow_gas_mass/mass_flow_mix_bendisken(Flow_info,tubing))

def frictional_gradient_Ben( Flow_info, tubing) -> float:
    vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos_bendisken(Flow_info,tubing)
    return ( F_bendiksen( Flow_info , tubing)*( (mix_rho*vm**2)/(2*tubing.Dh) ) )

def gravitational_gradient_Ben( Flow_info, tubing ) -> float:
    mix_rho = drift_infos_bendisken(Flow_info,tubing)[4]
    if tubing.direction == "Downhill":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = mix_rho*9.81*np.sin(angle)
    return grav

def ek_Ben( Flow_info, tubing) -> float: 
    A = (mass_flow_mix_bendisken(Flow_info,tubing)**2) / (tubing.area**2)
    B = (Flow_info.MM) / (8.314462*Flow_info.T*Flow_info.gas_rho**2)
    ekk = (A*titulo_bendisken(Flow_info,tubing)*B) 
    ekk = 0
    return ekk

def totaL_gradient_bendi( Flow_info, tubing) -> float:
    return ((frictional_gradient_Ben(Flow_info,tubing) + gravitational_gradient_Ben(Flow_info,tubing)) / (1 - ek_Ben(Flow_info,tubing) ))

def kinetic_gradient_Ben( Flow_info, tubing ) -> float:
    return (ek_Ben(Flow_info,tubing)*totaL_gradient_bendi(Flow_info,tubing))
