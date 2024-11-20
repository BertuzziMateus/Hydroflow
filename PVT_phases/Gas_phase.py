import numpy as np
from conversions import *


def z_Papay( Model ) -> float:
    return 1 - (3.53*Model.P_pr / (10**(0.9813*Model.T_pr))) + (0.274*Model.P_pr**2 / (10**(0.8157*Model.T_pr))) 

def z( Model  ) -> float:

    A = 1.39*(Model.T_pr - 0.92)**(1/2) - 0.36*Model.T_pr - 0.101
    B = (0.62 - 0.23*Model.T_pr)* Model.P_pr + ((0.066 / (Model.T_pr - 0.86)) - 0.037)*Model.P_pr**2 + ((0.32/(10**(9* (Model.T_pr - 1)))))*Model.P_pr**6
    C = 0.132 - 0.32*(np.log10(Model.T_pr))
    D = np.power(10,(0.3106 - 0.49*Model.T_pr + 0.1824*Model.T_pr**2))
    Z = A + ((1 - A) / np.exp(B)) + C*Model.P_pr**D
    
    return Z


def Bg( Model ) -> float: # m3/sm3
    T = C_to_R(Model)
    P = Bar_to_psia(Model)
    return (((14.7)/(520))*z(Model)*((T)/(P)))

def Gas_density( Model  ) -> float: # lb/ft**3
    return ( (Bar_to_pa(Model)*Model.Ma) / (z(Model)*8.314*C_to_K(Model)) ) * 0.062428

def Eg( Model ) -> float:
    return 1 / Bg(Model)

def Gas_Viscosity( Model  ) -> float: #cP  Dempsey (1965)

    μ_g = ( 1.709*(10**-5) - (2.062*(10**-6))*Model.Dg )*C_to_F(Model) + (8.188*10**-3) - (6.15*10**-3) * np.log(Model.Dg)


    a0 = -2.46211820
    a1 = 2.970547414
    a2 = -2.86264054e-1
    a3 = 8.05420522e-3
    a4 = 2.80860949
    a5 = -3.49803305
    a6 = 3.60373020e-1
    a7 = -1.044324e-2
    a8 = -7.93385648e-1
    a9 = 1.39643306
    a10 = -1.49144925e-1
    a11 = 4.41015512e-3
    a12 = 8.39387178e-2
    a13 = -1.86408848e-1
    a14 = 2.03367881e-2
    a15 = -6.09579263e-4

    A = (
        a0 + a1 * Model.P_pr + a2 * Model.P_pr**2 + a3 * Model.P_pr**3 +
        Model.T_pr * ( a4 + (a5 * Model.P_pr) + (a6 * Model.P_pr**2) + (a7 * Model.P_pr**3) ) +
        (Model.T_pr**2) * (a8 + a9 * Model.P_pr + a10 * Model.P_pr**2 + a11 * Model.P_pr**3 ) +
        (Model.T_pr**3) * (a12 + (a13 * Model.P_pr) + (a14 * Model.P_pr**2) + (a15 * Model.P_pr**3) )
        )

    μ = μ_g * np.exp(A) /  Model.T_pr

    return μ

