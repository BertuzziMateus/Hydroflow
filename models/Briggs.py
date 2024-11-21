import numpy as np
from scipy.optimize import fsolve

def Froude( Flow_info, tubing ) -> float:
    n_froude = ( Flow_info.vm**2) / ( 9.81* tubing.Dh)
    return n_froude

def flow_parameters( Flow_info ) -> list:

    L1 = 316 * Flow_info.λl**0.302
    L2 = 0.0009252 * Flow_info.λl**-2.4684
    L3 = 0.1 * Flow_info.λl**-1.4516
    L4 = 0.5 * Flow_info.λl**-6.738
    return[L1,L2,L3,L4]

def flow_type1( Flow_info, tubing ) -> str :

    froude = Froude( Flow_info, tubing )

    L1,L2,L3,L4 = flow_parameters(Flow_info)
    if  (( Flow_info.λl >= 0.4 ) and ( froude > L4 )) :
        flow_type = 'distributed'
    elif (( Flow_info.λl >= 0.001 ) and ( froude < L2 )):
        flow_type = 'segregated'
    elif (( Flow_info.λl >= 0.4 ) and ( L3 <= froude  and froude <= L4 )):
        flow_type = 'intermittent'
    else:
        raise IndexError('Out range')
    
    return flow_type

def flow_type( Flow_info, tubing ) -> str :

    froude = Froude(Flow_info, tubing )
    L1,L2,L3,L4 = flow_parameters(Flow_info)
    if (( Flow_info.λl < 0.4 ) and ( froude >= L1 )):
        flow_type = 'distributed'
    elif (( Flow_info.λl < 0.01 ) and ( froude < L1 )):
        flow_type = 'segregated'
    elif (( Flow_info.λl >= 0.01 ) and ( L2 <= froude  and froude <= L3 )):
        flow_type = 'transition'
    elif (( 0.01 <= Flow_info.λl and Flow_info.λl < 0.4 ) and ( L3 <= froude  and froude <= L1 )):
        flow_type = 'intermittent'
    else:
        flow_type = flow_type1(Flow_info,tubing)

    return flow_type

def segregated_liquid_holdup( Flow_info , tubing ) -> float:
    a = 0.9800
    b = 0.4846
    c = 0.0868
    Hlo = (a*(Flow_info.λl**b)) / (Froude(Flow_info, tubing)**c)
    
    
    if Hlo < Flow_info.λl:
        Hlo  = Flow_info.λl

    return Hlo


def intermittent_liquid_holdup( Flow_info, tubing) -> float:
    a = 0.8450
    b = 0.5351
    c = 0.0173
    Hlo = (a*(Flow_info.λl**b)) / (Froude(Flow_info, tubing)**c)
    
    
    if Hlo < Flow_info.λl:
        Hlo  = Flow_info.λl

    return Hlo


def distributed_liquid_holdup( Flow_info, tubing ) -> float:
    a = 1.0650
    b = 0.5824
    c = 0.0609
    Hlo = (a*(Flow_info.λl**b)) / (Froude(Flow_info, tubing)**c)
    
    
    if Hlo < Flow_info.λl:
        Hlo  = Flow_info.λl

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
        Hlo  = Flow_info.λl
    
    return Hlo

def liquid_velocity_number( Flow_info ) -> float:
    nvl = (Flow_info.vsl) * ( ((Flow_info.liquid_rho) / ( 9.81 * Flow_info.gas_liquid_sigma ))**(1/4) ) 
    return nvl

def angle_correction( Flow_info , tubing ) -> float :

    flow = flow_type(Flow_info,tubing)

    if tubing.direction == 'Ascendente':

        angle = tubing.angle

        if flow == 'transition':
            C  = 0
        if flow == 'segregated':

            d =  0.011
            e = -3.768
            f = 3.539
            g = -1.614

            C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )

        if flow == 'intermittent':

            d = 2.960
            e = 0.305
            f = -0.4473
            g = 0.0978

            C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
                
        if flow == 'distributed':
            C = 0

    elif tubing.direction == 'Descendente':
        
        angle= tubing.angle*-1

        if flow == 'transition':
            C = 0
        else:
            d = 4.7
            e = -0.3692
            f = 0.1244
            g = -0.5056
            C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
        
    
    correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))
    
    return correction

def angle_correction_transition( Flow_info, tubing, flow_s ) -> float :

    flow = flow_s

    if tubing.direction == 'Ascendente':

        angle = tubing.angle

        if flow == 'segregated':

            d = 0.011
            e = -3.768
            f = 3.539
            g = -1.614

            C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )

        if flow == 'intermittent':

            d = 2.960
            e = 0.305
            f = -0.4473
            g = 0.0978

            C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )

    elif tubing.direction == 'Descendente':
        
        angle= tubing.angle*-1

        d = 4.7
        e = -0.3692
        f = 0.1244
        g = -0.5056
        C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
        
    
    correction = 1 + (C*(np.sin(angle*1.8) - (1/3)*(np.sin(1.8*angle))**3))
    
    return correction


def liquid_Holdup( Flow_info , tubing ) -> float:

    Flow_type = flow_type(Flow_info, tubing)

    if Flow_type == 'transition':
        L1,L2,L3,L4 = flow_parameters(Flow_info) 
        A = ( L3 - Froude(Flow_info, tubing)) / (L3 - L2)
        hl_segregated = segregated_liquid_holdup(Flow_info, tubing)*angle_correction_transition(Flow_info,tubing,'segregated')
        hl_intermittent = intermittent_liquid_holdup(Flow_info, tubing)*angle_correction_transition(Flow_info,tubing,'intermittent')
        Hl = A*hl_segregated + (1-A)*hl_intermittent
        if Hl < Flow_info.λl:
            Hl  = Flow_info.λl
        if Hl > 1:
            Hl = 1
        elif Hl < 0 :
            Hl = 0
    else:
        Hlo = horizontal_liquid_holdup( Flow_info , tubing )
        if round(Hlo,4)  == round(Flow_info.λl,4):
            if tubing.angle != 0:
                correction = angle_correction( Flow_info, tubing)
            else:
                correction = 1

            Hl  = Hlo 
            
            if Hl > 1:
                Hl = 1
            elif Hl < 0 :
                Hl = 0

        else:
            if tubing.angle != 0:
                correction = angle_correction( Flow_info, tubing)
            else:
                correction = 1

            Hl  = Hlo * correction

            if Hl > 1:
                Hl = 1
            elif Hl < 0 :
                Hl = 0


    return Hl

def reynolds_no_slip(Flow_info, tubing) -> float:
    return  ( (Flow_info.mix_rho*Flow_info.vm*tubing.Dh) / (Flow_info.mix_viscosity) )

def ftp( Flow_info, tubing ) -> float:
    re = reynolds_no_slip(Flow_info,tubing)
    A = (10**6)/reynolds_no_slip( Flow_info, tubing)
    B = (2*(10**4))*(tubing.e_Dh)
    C = (A+B)**(1/3)
    Fn = 0.0055*(1+C)

    y = Flow_info.λl / liquid_Holdup(Flow_info,tubing)**2


    if (1 < y < 1.2):
        s = np.log(2.2 * y - 1.2)

    else: 
        s = ( np.log(y) )  / ( (-0.0523) + ( 3.182*np.log(y) ) - (0.8725*(np.log(y))**2) + (0.01853*(np.log(y))**4) )


    ftp = np.exp(s) * Fn

    return ftp

def slip_density_briggs( Flow_info ,  tubing ) -> float:
    Hl = liquid_Holdup(Flow_info,tubing)
    density = ( Flow_info.liquid_rho * Hl ) + Flow_info.gas_rho*( 1 - Hl) 
    return density

def friction_gradient_briggs( Flow_info ,  tubing ) -> float:
    return ( ftp( Flow_info , tubing  ) * ( (Flow_info.mix_rho * Flow_info.vm**2) / (2*tubing.Dh) ) )

def gravitational_gradient_briggs( Flow_info ,  tubing ) -> float:
    if tubing.direction == "Descendente":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = slip_density_briggs(Flow_info, tubing) * 9.81 * np.sin(angle)
    return grav

def Ek_briggs( Flow_info ,  tubing ) -> float:
    Ek = ( (slip_density_briggs( Flow_info, tubing )* Flow_info.vm* Flow_info.vsg) / (Flow_info.pressure*100000) )
    return Ek

def total_gradient_briggs( Flow_info,  tubing ) -> float:
    fric  = friction_gradient_briggs(Flow_info,tubing)
    grav = gravitational_gradient_briggs(Flow_info,tubing)
    lose = ((fric + grav) / (1-Ek_briggs(Flow_info,tubing ))) 

    return lose
