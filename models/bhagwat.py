import numpy as np
from scipy.optimize import fsolve

g = 9.81


def bhagwat_ghajar ( Flow_info,  tubing) -> list:

    if tubing.direction == "Descendente":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle

    K8 = ( ( (g*tubing.Dh*( Flow_info.liquid_rho - Flow_info.gas_rho ) ) / Flow_info.liquid_rho )**(0.5))*( 1 / (Flow_info.λl)**(0.5*np.sin(angle)) )

    vd = ((Flow_info.liquid_viscosity / Flow_info.gas_viscosity)**(-0.25)) * ( (0.35*np.sin(angle)) + (0.54*np.cos(angle)) )*K8
    
    C0 = ( ( 1 / ( ( (1+np.cos(angle))**1.25 ) ))**((Flow_info.λl)**(0.5)) ) + ( 0.18*( Flow_info.vsl / Flow_info.vm )**0.1 )

    return [C0,vd]


def drift_infos( Flow_info, tubing, ) -> list[float]:


    C0,vd = bhagwat_ghajar(Flow_info, tubing)
    vsg = (C0*Flow_info.vm  + vd) * (1 - Flow_info.λl )
    vsl = ( 1 - (1 - Flow_info.λl )*C0 )*Flow_info.vm - ( (1 - Flow_info.λl )*vd )
    vm = (vsg+vsl)
    Hl = vsl / vm              
    mix_rho = Hl*Flow_info.liquid_rho + ( 1 - Hl )*Flow_info.gas_rho
    mix_viscosity = Hl*Flow_info.liquid_viscosity + ( 1 - Hl )*Flow_info.gas_viscosity


    # if tubing.direction == "Descendente":
    #     angle = tubing.angle*-1
    # else:
    #     angle = tubing.angle


    # K8 = ( ( (g*tubing.Dh*( Flow_info.liquid_rho - Flow_info.gas_rho ) ) / Flow_info.liquid_rho )**(0.5))*( 1 / (Hl)**(0.5*np.sin(angle)) )
    # vd = ((Flow_info.liquid_viscosity / Flow_info.gas_viscosity)**(-0.25)) * ( (0.35*np.sin(angle)) + (0.54*np.cos(angle)) )*K8
    # C0 = ( ( 1 / ( ( (1+np.cos(angle))**1.25 ) ))**((Hl)**(0.5)) ) + ( 0.18*( vsl / vm )**0.1 )


    # vsg = (C0*vm  + vd) * (1 - Hl)
    # vsl = ( 1 - (1 - Hl )*C0 )*vm - ( (1 - Hl )*vd )
    # vm = (vsg+vsl)
    # Hl = vsl / vm
    # mix_rho = Hl*Flow_info.liquid_rho + ( 1 - Hl )*Flow_info.gas_rho
    # mix_viscosity = Hl*Flow_info.liquid_viscosity + ( 1 - Hl )*Flow_info.gas_viscosity

    return [vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd]

def reynolds ( Flow_info, tubing ) -> float:
    vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos(Flow_info,tubing)
    return  ((mix_rho*vm*tubing.Dh)/mix_viscosity)

def F( Flow_info, tubing,  )  -> float:
    re = reynolds(Flow_info,tubing)
    def f(F):
        return ((- 2*np.log10( ( (tubing.e/tubing.Dh) / (3.7) ) + ( 2.51 / ( re*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]

    return F

def mass_flow_mix( Flow_info, tubing) -> float:
    Hl = drift_infos(Flow_info,tubing)[3]
    return ( (Flow_info.flow_liquid_mass * Hl) + Flow_info.flow_gas_mass*(1-Hl) )

def titulo( Flow_info, tubing) -> float:
    return (Flow_info.flow_gas_mass/mass_flow_mix(Flow_info,tubing))

def frictional_gradient_Bha( Flow_info, tubing) -> float:
    vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos(Flow_info,tubing)
    return ( F( Flow_info , tubing)*( (mix_rho*vm**2)/(2*tubing.Dh) ) )

def gravitational_gradient_Bha( Flow_info, tubing ) -> float:
    mix_rho = drift_infos(Flow_info,tubing)[4]
    if tubing.direction == "Descendente":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = mix_rho*9.81*np.sin(angle)
    return grav

def ek_Bha( Flow_info, tubing) -> float: 
    A = (mass_flow_mix(Flow_info,tubing)**2) / (tubing.area**2)
    B = (Flow_info.MM) / (8.314462*Flow_info.T*Flow_info.gas_rho**2)
    ekk = (A*titulo(Flow_info,tubing)*B) 
    return ekk

def totaL_gradient_bhagwat( Flow_info, tubing) -> float:
    return ((frictional_gradient_Bha(Flow_info,tubing) + gravitational_gradient_Bha(Flow_info,tubing)) / (1 - ek_Bha(Flow_info,tubing) ))

def kinetic_gradient_Bha( Flow_info, tubing ) -> float:
    return (ek_Bha(Flow_info,tubing)*totaL_gradient_bhagwat(Flow_info,tubing))
