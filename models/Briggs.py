import numpy as np
from scipy.optimize import fsolve

def Froude( Flow_info, tubing ) -> float:
    n_froude = ( Flow_info.vm**2) / ( 9.81* tubing.Dh)
    return n_froude

def flow_parameters( Flow_info ) -> list:
    λl = Flow_info.λl
    L1 = 316 * λl**0.302
    L2 = 0.0009252 * λl**-2.468
    L3 = 0.1 * λl**-1.468
    L4 = 0.5 * λl**-6.738
    return[L1,L2,L3,L4]


def flow_type( Flow_info, tubing ) -> str :
    λl = Flow_info.λl
    froude = Froude(Flow_info, tubing )
    L1,L2,L3,L4 = flow_parameters(Flow_info)
    if (λl < 0.4  and froude >= L1)  or (λl >= 0.4 and froude > L4) :
        flow_type = 'distributed'
    elif (λl < 0.01 and froude < L1)  or (λl >= 0.01 and froude < L2) :
        flow_type = 'segregated'
    elif ( λl >= 0.01  and  L2 <= froude <= L3 ):
        flow_type = 'transition'
    elif ( 0.01 <= λl < 0.4  and  L3 <= froude <= L1 ) or  (λl >= 0.4 and L3 <= froude <= L4):
        flow_type = 'intermittent'
    else:
        raise ValueError('Out range')
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
        Hlo = (segregated_liquid_holdup(Flow_info),intermittent_liquid_holdup(Flow_info))
    
    return Hlo

def liquid_velocity_number( Flow_info ) -> float:
    nvl = (Flow_info.vsl) * ( ((Flow_info.liquid_rho) / ( 9.81 * Flow_info.gas_liquid_sigma ))**(1/4) ) 
    return nvl

def liquid_Holdup( Flow_info , tubing ) -> float :

    flow = flow_type(Flow_info,tubing)

    if tubing.direction == 'Uphill':

        angle = tubing.angle

        if flow == 'transition':

            if angle == 0:

                L1,L2,L3,L4 = flow_parameters(Flow_info) 
                A = ( L3 - Froude(Flow_info, tubing)) / (L3 - L2)
                Hls = horizontal_liquid_holdup(Flow_info , tubing)[0]
                Hli = horizontal_liquid_holdup(Flow_info , tubing)[1]
                Hl = A*Hls + (1-A)*Hli
                Hl = 0.924*Hl #Payne corretion

            else:
                
                L1,L2,L3,L4 = flow_parameters(Flow_info) 
                A = ( L3 - Froude(Flow_info, tubing)) / (L3 - L2)

                #segregado 

                d =  0.011
                e = -3.768
                f = 3.539
                g = -1.614

                C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
                if C < 0 :
                    C = 0
                correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))

                Hls = horizontal_liquid_holdup(Flow_info , tubing)[0]*correction
            


                # intermitent

                d =  0.011
                e = -3.768
                f = 3.539
                g = -1.614

                C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )

                if C < 0 :
                    C = 0

                correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))

                Hli = horizontal_liquid_holdup(Flow_info , tubing)[1]*correction

                Hl = A*Hls + (1-A)*Hli

                Hl = 0.924*Hl #Payne corretion
        
        if flow == 'segregated':

            if angle == 0 : 
                Hl = horizontal_liquid_holdup(Flow_info , tubing)
            else:
                d =  0.011
                e = -3.768
                f = 3.539
                g = -1.614

                C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )

                if C < 0 :
                    C = 0

                correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))

                Hl = horizontal_liquid_holdup(Flow_info , tubing)*correction

                Hl = 0.924*Hl #Payne corretion
     
        if flow == 'intermittent':

            if angle == 0:
                Hl = horizontal_liquid_holdup(Flow_info , tubing)
            else:
                d = 2.960
                e = 0.305
                f = -0.4473
                g = 0.0978

                C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
                
                if C < 0 :
                    C = 0

                correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))

                Hl = horizontal_liquid_holdup(Flow_info , tubing)*correction
                Hl = 0.924*Hl #Payne corretion

        if flow == 'distributed':

            Hl = horizontal_liquid_holdup(Flow_info , tubing)
            Hl = 0.924*Hl #Payne corretion

    elif tubing.direction == 'Downhill':
        
        angle= tubing.angle*-1

        d = 4.7
        e = -0.3692
        f = 0.1244
        g = -0.5056
        C = ( 1 - Flow_info.λl )*np.log( d * ( Flow_info.λl**e ) * (liquid_velocity_number(Flow_info)**f) * (Froude (Flow_info, tubing)**g) )
        
        if C < 0 :
            C = 0

        correction = 1 + (C*(np.sin(angle*1.8) - 0.333*(np.sin(1.8*angle))**3))


        if flow == 'transition':
            L1,L2,L3,L4 = flow_parameters(Flow_info) 
            A = ( L3 - Froude(Flow_info, tubing)) / (L3 - L2)
            Hls = horizontal_liquid_holdup(Flow_info , tubing)[0]*correction
            Hli = horizontal_liquid_holdup(Flow_info , tubing)[1]*correction
            Hl = A*Hls + (1-A)*Hli
            Hl = 0.685*Hl #Payne corretion
        else:
            Hl = horizontal_liquid_holdup(Flow_info , tubing)*correction
            Hl = 0.685*Hl #Payne corretion

    if Hl > 1: 
        Hl = 1
    elif Hl < 0:
        Hl = 0

    if Hl < Flow_info.λl:
        Hl = Flow_info.λl
    
       
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
