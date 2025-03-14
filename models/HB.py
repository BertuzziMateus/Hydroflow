import numpy as np
from scipy.optimize import fsolve
import math

def liquid_velocity_number( Flow_info ) -> float:

    vsl = Flow_info.vsl 
    liquid_rho = Flow_info.liquid_rho 
    sigma = Flow_info.gas_liquid_sigma
 
    equation = vsl* (liquid_rho/(9.81*sigma))**(0.25)


    return equation


def gas_velocity_number( Flow_info ) -> float:

    vsg = Flow_info.vsg
    liquid_rho = Flow_info.liquid_rho 
    sigma = Flow_info.gas_liquid_sigma
 
    equation = vsg* (liquid_rho/(9.81*sigma))**(0.25)


    return equation

def diameter_tubing_number( Flow_info , tubing ) -> float:

    Dh = tubing.Dh 
    liquid_rho = Flow_info.liquid_rho 
    sigma = Flow_info.gas_liquid_sigma

    equation = Dh*((liquid_rho*9.81)/sigma)**(1/2)

    return equation

def liquid_viscosity_number( Flow_info  ) -> float:

    liquid_viscosity = Flow_info.liquid_viscosity
    liquid_rho = Flow_info.liquid_rho 
    sigma = Flow_info.gas_liquid_sigma

    equation = liquid_viscosity*(9.81/(liquid_rho*sigma**3))**(1/4)

    return equation

def psi( Flow_info, tubing  ) -> float:
    x = (gas_velocity_number(Flow_info)*liquid_viscosity_number(Flow_info)**0.380) / (diameter_tubing_number(Flow_info,tubing)**2.14)
    if x < 0.01:
        Psi = 1
    elif x > 0.09:
        Psi = 1.83
    else:
        def calculate_psi(B):
            if B > 0.055:
                return 2.5714 * B + 1.5962
            elif B > 0.025:
                return -533.33 * (B ** 2) + 58.524 * B + 0.1171
            else:
                return 27170 * (B ** 3) - 317.52 * (B ** 2) + 0.5472 * B + 0.9999

        Psi = calculate_psi(x)

    return Psi

def nlc(Flow_info) -> float:
    x_test = liquid_viscosity_number(Flow_info)
    
    if x_test < 0.0019306977288832496:
        nlc = 0.001873
    elif x_test > 0.48599963679715436:
        nlc = 0.0113
    else:
        def calculate_cnl(N_L):
            return 0.061 * (N_L**3) - 0.0929 * (N_L**2) + 0.0505 * N_L + 0.0019
        nlc = calculate_cnl(x_test) 
    return nlc


def HL_HB( Flow_info, tubing ) -> float:

    vm = Flow_info.vm
    vsl = Flow_info.vsl
    vsg = Flow_info.vsg
    vs = 2.4384

    Cl =  vsl / vm

    Lb = max(1.071-0.2218* ((vm**2)/tubing.Dh),0.13)

    if (1-Cl) < Lb:
        hl = 1 - (1/2)*(1+(vm/vs)-((1+ ((vm/vs)))**2 - 4*((vsg/vs)))**0.5)
    else:
        x_test = (
            (liquid_velocity_number(Flow_info)/(gas_velocity_number(Flow_info)**0.575))*
            (((Flow_info.pressure*14.503773773020924)/(14.7))**0.10)*
            ((nlc(Flow_info))/(diameter_tubing_number(Flow_info,tubing)))
            )
    
        if x_test < 0.0000021787779864028906:
            y_pred =  0.0
        elif x_test > 0.005428925924399341:
            y_pred = 1.0
        else:
            def calculate_equation(H):
                numerator = 0.0047 + 1123.32 * H + 729489.64 * (H ** 2)
                denominator = 1 + 1097.1566 * H + 722153.97 * (H ** 2)
                return math.sqrt(numerator / denominator)
            y_pred = calculate_equation(x_test)
        
        hl = y_pred* psi(Flow_info, tubing)

    if hl > Flow_info.λl:
        hl = hl
    else:
        hl = Flow_info.λl

    return max(0.0, min(1.0, hl)) 

def slip_viscosity_Hb( Flow_info, tubing) -> float:

    Hl = HL_HB(Flow_info,tubing)
    viscosity  =  ( Flow_info.liquid_viscosity**Hl ) * (Flow_info.gas_viscosity**(1-Hl))

    return  viscosity

def reynolds_HB(Flow_info, tubing) -> float:
    
    reynolds = (Flow_info.mix_rho*Flow_info.vm*tubing.Dh) / (slip_viscosity_Hb(Flow_info,tubing)) 

   
    return  reynolds

def FD_HB(Flow_info, tubing) -> float:
    re = reynolds_HB(Flow_info,tubing)
    def f(F):
        return ((- 2*np.log10( ( (tubing.e/tubing.Dh) / (3.7) ) + ( 2.51 / ( re*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]

    return F

def mix_slip_density_HB( Flow_info,  tubing) -> float:
    Hl = HL_HB(Flow_info,tubing)
    density  =  ( Flow_info.liquid_rho * Hl ) + Flow_info.gas_rho*( 1 - Hl) 
    return density

def friction_gradient_HB( Flow_info, tubing) -> float:
    f = FD_HB( Flow_info , tubing  )
    rho_ns =  Flow_info.mix_rho
    mix_velocity = Flow_info.vm
    dh = tubing.Dh

    friction_gradient = (f*(rho_ns**2)*(mix_velocity**2)) / (2*dh*mix_slip_density_HB(Flow_info,tubing))


    return friction_gradient

def gravitational_gradient_HB( Flow_info, tubing) -> float:
    if tubing.direction == "Downhill":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = mix_slip_density_HB(Flow_info, tubing) * 9.81 * np.sin(angle)
    return grav


def Ek_briggs_hb( Flow_info ,  tubing ) -> float:
    Ek = ( (mix_slip_density_HB( Flow_info, tubing )* Flow_info.vm* Flow_info.vsg) / (Flow_info.pressure*100000) )
    return Ek

def total_Hb(Flow_info, tubing):
    grav_grad = gravitational_gradient_HB(Flow_info, tubing)
    friction_grad = friction_gradient_HB(Flow_info, tubing)
    lose = (grav_grad + friction_grad) / (1-Ek_briggs_hb(Flow_info,tubing ))
    return lose