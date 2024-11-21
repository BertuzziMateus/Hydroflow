import numpy as np
from PVT_phases.Gas_phase import Bg
from conversions import *

def Pb_standing( fluid_model ) -> float:  #psia
    T = C_to_F(fluid_model)
    RS = fluid_model.RGO*5.614583333333333
    a = 0.00091 * T - 0.0125 * fluid_model.API
    pb = (18.2 * (  (10**a) * (RS / fluid_model.Dg)**0.83 - 1.4))
    return pb


def Rs_standing( fluid_model  ) -> float:  #scf/STb
    pressure = Bar_to_psia(fluid_model)
    PB = Pb_standing(fluid_model)
    T = C_to_F(fluid_model)
    if pressure > PB:
        Rs = fluid_model.RGO*5.614583333333333
    else:
        term1 = (pressure / 18.2) + 1.4
        term2 = 10 ** (0.0125 * fluid_model.API - 0.00091 * T)
        Rs = fluid_model.Dg * ((term1 * term2) ** (1 / 0.83))

    return Rs  #*0.17810760667903525


def Bob_standing( fluid_model ) -> float: #bbl/STb

    T = C_to_F(fluid_model)
    RS = fluid_model.RGO*5.614583333333333
    term1 = RS * (fluid_model.Dg / fluid_model.Do) ** 0.5
    term2 = 1.25 * T
    Bob = 0.9459 + 0.00012 * ((term1 + term2) ** 1.2)    

    return Bob



def Co_standing( fluid_model ) -> float: # psia-1
    P = Bar_to_psia(fluid_model)
    Pb = Pb_standing(fluid_model)
    if P  >= Pb:
        rho_ob = Oil_Density_standing_pb(fluid_model)
        term1 = rho_ob + 0.004347 * (P - Pb) - 79.1
        term2 = 0.0007141 * (P - Pb) - 12.938
        Co = 10**(-6) * np.exp(term1 / term2)
    else:

        def Bg( fluid_model ) -> float: # bbl/scf
            def z( fluid_model  ) -> float:

                A = 1.39*(fluid_model.T_pr - 0.92)**(1/2) - 0.36*fluid_model.T_pr - 0.101
                B = (0.62 - 0.23*fluid_model.T_pr)* fluid_model.P_pr + ((0.066 / (fluid_model.T_pr - 0.86)) - 0.037)*fluid_model.P_pr**2 + ((0.32/(10**(9* (fluid_model.T_pr - 1)))))*fluid_model.P_pr**6
                C = 0.132 - 0.32*(np.log10(fluid_model.T_pr))
                D = np.power(10,(0.3106 - 0.49*fluid_model.T_pr + 0.1824*fluid_model.T_pr**2))
                Z = A + ((1 - A) / np.exp(B)) + C*fluid_model.P_pr**D
                return Z
            
            T = C_to_R(fluid_model)
            P = Bar_to_psia(fluid_model)

            return ( ( 0.005035 )*( (z(fluid_model)*T)/ (P) ) ) 
        
        T = C_to_R(fluid_model)
        denominator = Bo_standing(fluid_model) * (0.83 * P + 21.75)
        internal_root =  ( Rs_standing(fluid_model) *  ((fluid_model.Dg /fluid_model.Do)**0.5) + 1.25 * (T - 460))**0.12
        bracket_term = (0.00014*((fluid_model.Dg /fluid_model.Do)**0.5) * internal_root) - Bg(fluid_model)
        Co = (-Rs_standing(fluid_model) / denominator) * bracket_term
    return Co



def Bo_standing( fluid_model ) -> float: #bbl/STb

    pressure =  Bar_to_psia(fluid_model)

    if pressure > Pb_standing(fluid_model):
        
        Bo = Bob_standing(fluid_model)* np.exp( -Co_standing(fluid_model) * ( pressure - Pb_standing(fluid_model) ) )

    else:
        T = C_to_F(fluid_model)
        term1 = Rs_standing(fluid_model) * (fluid_model.Dg / fluid_model.Do) ** 0.5
        term2 = 1.25 * T
        Bo = 0.9459 + 0.00012 * ((term1 + term2) ** 1.2)    
    return Bo 


def Oil_Density_standing_pb( fluid_model  ) -> float: #lb/ft**3
    RS = fluid_model.RGO*5.614583333333333
    po = ( ( 62.4*fluid_model.Do + 0.0136*RS*fluid_model.Dg ) / ( Bob_standing(fluid_model) ) )
    return po # *16.01846337396014


def Oil_Density_standing( fluid_model ) -> float: #lb/ft**3
    pressure  = Bar_to_psia(fluid_model) 
    if pressure > Pb_standing(fluid_model):
        pob = Oil_Density_standing_pb(fluid_model)
        po = pob*np.exp( Co_standing(fluid_model) * ( pressure - Pb_standing(fluid_model) ) )
    else: 
        po = ( ( 62.4*fluid_model.Do + 0.0136*Rs_standing(fluid_model)*fluid_model.Dg ) / ( Bo_standing(fluid_model) ) )
    return po # *16.01846337396014

def Dead_Oil_Viscosity_standing( fluid_model ) -> float:#cP
    A = 10**(0.43 + 8.33/fluid_model.API) 
    T = fluid_model.T * (9/5) + 491.67
    U_od = 0.32 + ( (1.8*10**7)/(fluid_model.API**4.53))*(360/(T-260) )**A
    return U_od

def Oil_Viscosity_standing( fluid_model ) -> float:#cP

    pressure = Bar_to_psia(fluid_model)
    Pb = Pb_standing(fluid_model)
    R_s = Rs_standing(fluid_model)

    b1 =  ( (0.68) / 10**((8.62e-5)*R_s))
    b2 = ( (0.25) / 10**((1.1e-3)*R_s))
    b3 = ( (0.062) / 10**((3.74e-3)*R_s))
    b = b1 + b2 + b3
    a = 10**((R_s*-7.4e-4)+((2.2e-7)*(R_s**2)))
    U_o = a * Dead_Oil_Viscosity_standing(fluid_model)**b

    if pressure > Pb:    
        U_o = U_o + (0.001 * (pressure - Pb) * ((0.024 * U_o ** 1.6) + (0.038 *U_o ** 0.56)))
   
    return U_o


