import numpy as np
from scipy.optimize import fsolve
from scipy.optimize import brentq
from scipy.optimize import newton

from conversions import *

def z_hall(fluid_model) -> float:

    def equation(y, fluid_model):
        T_pr = 1 / fluid_model.T_pr
        A = 14.76 * T_pr - 9.76 * T_pr**2 + 4.58 * T_pr**3
        B = 90.7 * T_pr - 242.2 * T_pr**2 + 42.4 * T_pr**3
        term1 = -0.06125 * fluid_model.P_pr * T_pr * np.exp(-1.2 * (1 - T_pr)**2)
        term2 = (y + y**2 + y**3 - y**4) / (1 - y)**3
        term3 = -A * y**2
        term4 = B * y**(2.18 + 2.82 * T_pr)  # Corrected exponent
        return term1 + term2 + term3 + term4

    def equation_derivative(y, fluid_model):
        T_pr = 1 / fluid_model.T_pr
        A = 14.76 * T_pr - 9.76 * T_pr**2 + 4.58 * T_pr**3
        B = 90.7 * T_pr - 242.2 * T_pr**2 + 42.4 * T_pr**3
        exponent = 2.18 + 2.82 * T_pr  # Corrected exponent
        # Derivative of term2: (y + y² + y³ - y⁴)/(1 - y)^3
        dy_term2 = (1 + 2*y + 3*y**2 - 4*y**3) * (1 - y)**3 + (y + y**2 + y**3 - y**4) * 3*(1 - y)**2
        dy_term2 = dy_term2 / (1 - y)**6  # Simplified derivative of term2
        # Derivative of term3: -A y²
        dy_term3 = -2 * A * y
        # Derivative of term4: B y^(exponent)
        dy_term4 = B * exponent * y**(exponent - 1)
        # Sum all derivatives (term1 derivative is 0 as it's constant w.r. to y)
        return dy_term2 + dy_term3 + dy_term4

    T_pr = 1 / fluid_model.T_pr

    Y_initial = 0.0125 * fluid_model.P_pr * T_pr * np.exp(-1.2 * (1 - T_pr)**2)


    y = newton(
        func=lambda y: equation(y, fluid_model),
        x0=Y_initial,
        fprime=lambda y: equation_derivative(y, fluid_model),
        maxiter=1000,
        tol=1e-12
    )

    term1_val = 0.06125 * fluid_model.P_pr * T_pr * np.exp(-1.2 * (1 - T_pr)**2)
    Z = term1_val / y

    return Z


def z( Model  ) -> float:

    A = 1.39*(Model.T_pr - 0.92)**(1/2) - 0.36*Model.T_pr - 0.101
    B = (0.62 - 0.23*Model.T_pr)* Model.P_pr + ((0.066 / (Model.T_pr - 0.86)) - 0.037)*Model.P_pr**2 + ((0.32/(10**(9* (Model.T_pr - 1)))))*Model.P_pr**6
    C = 0.132 - 0.32*(np.log10(Model.T_pr))
    D = np.power(10,(0.3106 - 0.49*Model.T_pr + 0.1824*Model.T_pr**2))
    Z = A + ((1 - A) / np.exp(B)) + C*Model.P_pr**D
    
    return Z


def Bg( Model ) -> float: # m3/sm3
    T = C_to_K(Model)
    P = Bar_to_pa(Model)/1000
    bg_m3 = 0.350958*((z(Model)*T)/P)
    return bg_m3

def Gas_density( Model  ) -> float: #kg/m³
    density =  (Bar_to_pa(Model)*Model.Ma) / (z(Model)*8.314*C_to_K(Model)) 
    return density

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

def gas_viscosity_lee(fluid_model):

    temperature_c = fluid_model.T
    temperature_r = temperature_c *(9/5) + 491.67
    
    pg = Gas_density(fluid_model)*0.062427960576145

    Mg = 0.0289655* fluid_model.Dg *1000
    
    kv = ((9.379 + 0.0160*Mg)*temperature_r**1.5)/(209.2 + 19.26 * Mg + temperature_r)

    xv = 3.448 + 986.4/temperature_r + 0.01009 * Mg

    yv = 2.4 - 0.2 *xv

    μ = (10**-4) * kv * (np.exp(xv*(pg/62.4)**yv))

    return μ

