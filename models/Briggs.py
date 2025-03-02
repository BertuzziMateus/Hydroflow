import numpy as np
from scipy.optimize import fsolve

def Froude( Flow_info, tubing ) -> float:
    n_froude = ( Flow_info.vm**2) / ( 9.81* tubing.Dh)
    return n_froude

def flow_parameters( Flow_info ) -> list:
    λl = Flow_info.λl
    L1 = 316 * λl**0.302
    L2 = 0.000925 * λl**-2.468
    L3 = 0.1 * λl**-1.452
    L4 = 0.5 * λl**-6.738
    return[L1,L2,L3,L4]


def flow_type( Flow_info, tubing ) -> str :
    λl = Flow_info.λl
    froude = Froude(Flow_info, tubing )
    L1,L2,L3,L4 = flow_parameters(Flow_info)

    # -------------------Segregated--------------------- #

    if λl < 0.01 and froude  < L1:
        flow_type = 'segregated'
    elif λl >= 0.01 and froude < L2:
        flow_type = 'segregated'

    # -------------------Transition--------------------- #
    elif λl >= 0.01 and L2 <= froude <= L3:
        flow_type = 'transition'

    # -------------------Intermittent--------------------- #

    elif 0.01 <= λl < 0.4 and L3 < froude <= L1:
        flow_type = 'intermittent'
    elif λl >= 0.4 and L3 < froude <= L4:
        flow_type = 'intermittent'
    
    # -------------------Distributed--------------------- #

    elif  λl < 0.4 and froude >= L1:
        flow_type = 'distributed'
    elif λl >= 0.4 and froude > L4:
        flow_type = 'distributed'
    
    # -------------------Out of Range--------------------- #
    else:
        raise ValueError('Out of range')
    
    return flow_type
    
def segregated_liquid_holdup( Flow_info , tubing ) -> float:
    λl = Flow_info.λl
    a = 0.9800
    b = 0.4846
    c = 0.0868
    Hlo = (a*(λl**b)) / (Froude(Flow_info, tubing)**c)
    
    if Hlo < λl:
        Hlo  = λl

    return Hlo


def intermittent_liquid_holdup( Flow_info, tubing) -> float:
    λl = Flow_info.λl
    a = 0.8450
    b = 0.5351
    c = 0.0173
    Hlo = (a*(λl**b)) / (Froude(Flow_info, tubing)**c)
    
    if Hlo < λl:
        Hlo  = λl

    return Hlo


def distributed_liquid_holdup( Flow_info, tubing ) -> float:
    λl = Flow_info.λl
    a = 1.0650
    b = 0.5824
    c = 0.0609
    Hlo = (a*(λl**b)) / (Froude(Flow_info, tubing)**c)
    
    if Hlo < λl:
        Hlo  = λl

    return Hlo


def horizontal_liquid_holdup( Flow_info , tubing ) -> float:

    Flow_type = flow_type(Flow_info, tubing)

    if Flow_type == 'distributed':
        Hlo = distributed_liquid_holdup(Flow_info, tubing)
    elif Flow_type == 'intermittent':
        Hlo = intermittent_liquid_holdup(Flow_info, tubing)
    elif Flow_type == 'segregated':
        Hlo = segregated_liquid_holdup(Flow_info, tubing)
    elif Flow_type == 'transition':
        Hlo = (segregated_liquid_holdup(Flow_info , tubing),intermittent_liquid_holdup(Flow_info , tubing))
    
    return Hlo

def liquid_velocity_number( Flow_info ) -> float:
    nvl = (Flow_info.vsl) * ( ((Flow_info.liquid_rho) / ( 9.81 * Flow_info.gas_liquid_sigma ))**(1/4) ) 
    return nvl

import numpy as np

def liquid_Holdup(Flow_info, tubing) -> float:
    flow = flow_type(Flow_info, tubing)
    Hl = 0.0

    if tubing.direction == 'Uphill':
        angle_rad = tubing.angle
    elif tubing.direction == 'Downhill':
        angle_rad = -tubing.angle

    angle_deg = np.degrees(angle_rad)
    apply_payne = (abs(angle_deg) <= 5.0)
    angle_deg_conv = np.degrees(angle_rad)
    angle_beggs = 1.8 * angle_deg_conv
    angle_for_sin = np.radians(angle_beggs)

    if tubing.direction == 'Uphill':
        if flow == 'transition':
            if abs(angle_rad) < 1e-5:
                L1, L2, L3, L4 = flow_parameters(Flow_info)
                A = (L3 - Froude(Flow_info, tubing)) / (L3 - L2)
                Hls = horizontal_liquid_holdup(Flow_info, tubing)[0]
                Hli = horizontal_liquid_holdup(Flow_info, tubing)[1]
                Hl = A * Hls + (1 - A) * Hli
                if apply_payne: Hl *= 0.924
            else:
                L1, L2, L3, L4 = flow_parameters(Flow_info)
                A = (L3 - Froude(Flow_info, tubing)) / (L3 - L2)
                d_seg, e_seg, f_seg, g_seg = 0.011, -3.768, 3.539, -1.614
                C_seg = (1 - Flow_info.λl) * np.log(d_seg * (Flow_info.λl**e_seg) * (liquid_velocity_number(Flow_info)**f_seg) * (Froude(Flow_info, tubing)**g_seg))
                C_seg = max(C_seg, 0)
                correction_seg = 1 + C_seg * (np.sin(angle_for_sin) - 0.333 * (np.sin(angle_for_sin)**3))
                Hls = horizontal_liquid_holdup(Flow_info, tubing)[0] * correction_seg
                d_int, e_int, f_int, g_int = 2.96, 0.305, -0.4473, 0.0978
                C_int = (1 - Flow_info.λl) * np.log(d_int * (Flow_info.λl**e_int) * (liquid_velocity_number(Flow_info)**f_int) * (Froude(Flow_info, tubing)**g_int))
                C_int = max(C_int, 0)
                correction_int = 1 + C_int * (np.sin(angle_for_sin) - 0.333 * (np.sin(angle_for_sin)**3))
                Hli = horizontal_liquid_holdup(Flow_info, tubing)[1] * correction_int
                Hl = A * Hls + (1 - A) * Hli
                if apply_payne: Hl *= 0.924

        elif flow == 'segregated':
            if abs(angle_rad) < 1e-5:
                Hl = horizontal_liquid_holdup(Flow_info, tubing)
                if apply_payne: Hl *= 0.924
            else:
                d_seg, e_seg, f_seg, g_seg = 0.011, -3.768, 3.539, -1.614
                C_seg = (1 - Flow_info.λl) * np.log(d_seg * (Flow_info.λl**e_seg) * (liquid_velocity_number(Flow_info)**f_seg) * (Froude(Flow_info, tubing)**g_seg))
                C_seg = max(C_seg, 0)
                correction_seg = 1 + C_seg * (np.sin(angle_for_sin) - 0.333 * (np.sin(angle_for_sin)**3))
                Hl = horizontal_liquid_holdup(Flow_info, tubing) * correction_seg
                if apply_payne: Hl *= 0.924

        elif flow == 'intermittent':
            if abs(angle_rad) < 1e-5:
                Hl = horizontal_liquid_holdup(Flow_info, tubing)
                if apply_payne: Hl *= 0.924
            else:
                d_int, e_int, f_int, g_int = 2.96, 0.305, -0.4473, 0.0978
                C_int = (1 - Flow_info.λl) * np.log(d_int * (Flow_info.λl**e_int) * (liquid_velocity_number(Flow_info)**f_int) * (Froude(Flow_info, tubing)**g_int))
                C_int = max(C_int, 0)
                correction_int = 1 + C_int * (np.sin(angle_for_sin) - 0.333 * (np.sin(angle_for_sin)**3))
                Hl = horizontal_liquid_holdup(Flow_info, tubing) * correction_int
                if apply_payne: Hl *= 0.924

        elif flow == 'distributed':
            Hl = horizontal_liquid_holdup(Flow_info, tubing)

    elif tubing.direction == 'Downhill':
        d, e, f, g = 4.7, -0.3692, 0.1244, -0.5056
        C = (1 - Flow_info.λl) * np.log(d * (Flow_info.λl**e) * (liquid_velocity_number(Flow_info)**f) * (Froude(Flow_info, tubing)**g))
        C = max(C, 0)
        correction = 1 + C * ( (np.sin(angle_for_sin) - 0.333 * (np.sin(angle_for_sin)**3)) )
        if flow == 'transition':
            L1, L2, L3, L4 = flow_parameters(Flow_info)
            A = (L3 - Froude(Flow_info, tubing)) / (L3 - L2)
            Hls = horizontal_liquid_holdup(Flow_info, tubing)[0] * correction
            Hli = horizontal_liquid_holdup(Flow_info, tubing)[1] * correction
            Hl = A * Hls + (1 - A) * Hli
        else:
            Hl = horizontal_liquid_holdup(Flow_info, tubing) * correction
        if apply_payne: Hl *= 0.685

    Hl = np.clip(Hl, 0.0, 1.0)
    return Hl

def reynolds_no_slip(Flow_info, tubing) -> float:
    return  ( (Flow_info.mix_rho*Flow_info.vm*tubing.Dh) / (Flow_info.mix_viscosity) )

def ftp( Flow_info, tubing ) -> float:

    def f(F):
        return ((- 2*np.log10( ( (tubing.e/tubing.Dh) / (3.7) ) + ( 2.51 / ( reynolds_no_slip(Flow_info,tubing)*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]

    y = Flow_info.λl / liquid_Holdup(Flow_info,tubing)**2


    if (1 < y < 1.2):
        s = np.log(2.2 * y - 1.2)

    else: 
        s = ( np.log(y) )  / ( (-0.0523) + ( 3.182*np.log(y) ) - (0.8725*(np.log(y))**2) + (0.01853*(np.log(y))**4) )


    ftp = np.exp(s) * F

    return ftp

def slip_density_briggs( Flow_info ,  tubing ) -> float:
    Hl = liquid_Holdup(Flow_info,tubing)
    density = ( Flow_info.liquid_rho * Hl ) + Flow_info.gas_rho*( 1 - Hl) 
    return density

def friction_gradient_briggs( Flow_info ,  tubing ) -> float:
    friction = ( ftp( Flow_info , tubing  ) *  (Flow_info.mix_rho * Flow_info.vm**2) ) / (2*tubing.Dh) 
    return friction

def gravitational_gradient_briggs( Flow_info ,  tubing ) -> float:
    if tubing.direction == "Downhill":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = slip_density_briggs(Flow_info, tubing) * 9.81 * np.sin(angle)
    return grav

def Ek_briggs( Flow_info ,  tubing ) -> float:
    Ek = ( (slip_density_briggs( Flow_info, tubing )* Flow_info.vm* Flow_info.vsg) / (Flow_info.pressure*100000) )
    Ek = 0
    return Ek

def total_gradient_briggs( Flow_info,  tubing ) -> float:
    fric  = friction_gradient_briggs(Flow_info,tubing)
    grav = gravitational_gradient_briggs(Flow_info,tubing)
    lose = (fric + grav) / (1-Ek_briggs(Flow_info,tubing ))

    return lose
