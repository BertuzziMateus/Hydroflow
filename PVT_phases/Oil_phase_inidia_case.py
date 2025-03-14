import numpy as np

from PVT_phases.Oil_phase_standing import Bo_standing

from scipy.optimize import fsolve

from scipy.optimize import root_scalar


def PB_lasater(fluid_model) -> float:
    RGO = fluid_model.RGO*5.614583333333333
    oil_sg = fluid_model.Do
    API = fluid_model.API
    gas_sg = fluid_model.Dg
    temperature_c = fluid_model.T
    temperature_F = temperature_c*(9/5) + 32
    def calculate_mo(api):
        mo = (558.16 
            + 1.1025 * api 
            - 0.50033 * api**2 
            + 8.32591e-3 * api**3 
            - 3.8688e-5 * api**4)
        return mo
    
    gas_mole_fraction = ((RGO/379.3)) / ( ((RGO/379.3)) + ((350*oil_sg)/calculate_mo(API)) )
    
    def calculate_pf(y_g):

        x = y_g

        value = 21.78*(x**5) - 48.75*(x**4) + 44.93*(x**3) - 11.48*(x**2) + 3.616*x + 0.01679

        return value

    
    bubble_point = ((calculate_pf(gas_mole_fraction)*(temperature_F+459.6))/(gas_sg))

    return bubble_point


def Rs_lasater(fluid_model)->float:

    pressure  = fluid_model.P * 14.503773800722
    bubble_point = PB_lasater(fluid_model)
    gas_sg = fluid_model.Dg

    temperature_c = fluid_model.T
    temperature_F = temperature_c*(9/5) + 32


    if pressure > bubble_point:
        RS = fluid_model.RGO*5.614583333333333
    else:

    
        def equation(RGO):
            api = fluid_model.API

            pf = (pressure * gas_sg) / (temperature_F+459.6)


            if pf > 3.183021628577:
                bracket = [0.6000000000001,1]
                def equation_2(y_g):
                    return (0.83918 * (10 ** (1.08000 * y_g)) * (y_g ** 0.31109) - pf)

            else:
                bracket = [0,0.6]
                def equation_2(y_g):
                    return (0.83918 * (10 ** (1.17664 * y_g)) * (y_g ** 0.57246) - pf)
            

            Yg_test = root_scalar(equation_2, bracket=bracket, method='brentq').root

    
            def calculate_mo(api):

                mo = (558.16 
                    + 1.1025 * api 
                    - 0.50033 * api**2 
                    + 8.32591e-3 * api**3 
                    - 3.8688e-5 * api**4)
                return mo
            
            oil_sg = fluid_model.Do
            return ((( (RGO/379.3)) / ( ((RGO/379.3)) + ((350*oil_sg)/calculate_mo(api)) ) ) - Yg_test )
        
        RS  = fsolve(equation, fluid_model.RGO)[0]

    return RS

def compressibility_vasquez(fluid_model):

    pressure_bar = fluid_model.P 
    pressure_psia =  pressure_bar * 14.503773800722

    api = fluid_model.API
    temperature_c = fluid_model.T
    temperature_f = temperature_c *(9/5) + 32
    temperature_r = temperature_c  *(9/5) + 491.67
    gas_sg = fluid_model.Dg


    def dgn(dg,api):

        value = dg*(1 + (5.912e-5)*api* 60 * np.log10(217.557/144.7) )

        return value

    if  pressure_psia > PB_lasater(fluid_model):
        RS = fluid_model.RGO*5.614583333333333

        co_1 =  1433
        co_2 = 5 * RS
        co_3 = 17.2 * temperature_f 
        co_4 = 1180 * dgn(gas_sg,api)
        co_5 = 12.61 * api
        co_6 = (10**5) * pressure_psia

        co = (- co_1 + co_2 + co_3 - co_4 + co_5 ) / co_6

    else:
    
        if  api > 30 :
            C1_value_bo = 4.67e-4
            C2_value_bo = 1.1e-5
            C3_value_bo = 1.337e-9
            C1_value_rs = 0.0178
            C2_value_rs = 1.1870
            C3_value_rs = 23.931    
        else:
            C1_value_bo = 4.677e-4
            C2_value_bo = 1.751e-5
            C3_value_bo = -1.811e-9
            C1_value_rs = 0.0362
            C2_value_rs = 1.0937
            C3_value_rs = 25.7240


        dgn_value = dgn(gas_sg,api)

        Rs_value = (C1_value_rs*dgn_value*(pressure_psia**C2_value_rs)) * np.exp(C3_value_rs * (api/temperature_r))

        

        bo_value = 1 + C1_value_bo*Rs_value + (temperature_r -520) * (api/dgn_value) * (C2_value_bo+C3_value_bo*Rs_value) 

        def z( Model  ) -> float:

            A = 1.39*(Model.T_pr - 0.92)**(1/2) - 0.36*Model.T_pr - 0.101
            B = (0.62 - 0.23*Model.T_pr)* Model.P_pr + ((0.066 / (Model.T_pr - 0.86)) - 0.037)*Model.P_pr**2 + ((0.32/(10**(9* (Model.T_pr - 1)))))*Model.P_pr**6
            C = 0.132 - 0.32*(np.log10(Model.T_pr))
            D = np.power(10,(0.3106 - 0.49*Model.T_pr + 0.1824*Model.T_pr**2))
            Z = A + ((1 - A) / np.exp(B)) + C*Model.P_pr**D
            
            return Z

        z_value = z(fluid_model)
        bg_value = 0.005035*((z_value*temperature_r)/pressure_psia)
        

        dbo_dp = api*C1_value_rs*C2_value_rs*C3_value_bo*pressure_psia**C2_value_rs*(temperature_r - 520)*np.exp(api*C3_value_rs/temperature_r)/pressure_psia + C1_value_bo*C1_value_rs*C2_value_rs*pressure_psia**C2_value_rs*dgn_value*np.exp(api*C3_value_rs/temperature_r)/pressure_psia

        drs_dp = C1_value_rs*C2_value_rs*pressure_psia**C2_value_rs*dgn_value*np.exp(api*C3_value_rs/temperature_r)/pressure_psia


        co = -( 1 / bo_value ) * (dbo_dp)  + ((bg_value/bo_value) * (drs_dp))
    
    return co



def dead_viscosity_beggs( fluid_model ) -> float:


    temperature_c = fluid_model.T
    temperature_r = temperature_c *(9/5) + 491.67
    T = temperature_r

    Z = 3.0324 - 0.02023 * fluid_model.API
    Y = 10**Z
    X = Y*(T-460)**(-1.163)
    dead_viscosity = (10**X) - 1


    return dead_viscosity

def oil_viscosity_paper( fluid_model ) -> float:

    pressure_bar  =  fluid_model.P
    pressure_psia  =  pressure_bar*14.503773800722
    bubble_point = PB_lasater(fluid_model)

    if pressure_psia > bubble_point:
         
        a = -3.9*(10**-5)*pressure_psia-5
        m = 2.6*pressure_psia**(1.187)*(10**a)

        def viscosity_bubble_point(fluid_model):
            Rs = Rs_lasater(fluid_model)
            a = 10.715*(Rs+100)**(-0.515)
            b = 5.44*(Rs+150)**(-0.338)
            viscosity_bubble = a*dead_viscosity_beggs(fluid_model)**b
            return viscosity_bubble

        viscosity = viscosity_bubble_point(fluid_model)*(pressure_psia/bubble_point)**m
    else:

        Rs = Rs_lasater(fluid_model)
        a = 10.715*(Rs+100)**(-0.515)
        b = 5.44*(Rs+150)**(-0.338)

        viscosity = a*dead_viscosity_beggs(fluid_model)**b
    
    return viscosity


def gas_oil_interfacial_tension(fluid_model) :

    api = fluid_model.API
    pressure  = fluid_model.P * 14.503773800722
    temperature_c = fluid_model.T
    temperature_f = temperature_c*(9/5) + 32


    sigma_68 = 39 - 0.2571*api
    sigma_100 = 37.5 - 0.2571*api

    if temperature_f <  68 : 
        sigma_od = sigma_68
    elif (68 < temperature_f < 100):
        sigma_od = sigma_68  + ((temperature_f-68)*(sigma_100-sigma_68))/(100-68)
    else:
        sigma_od = sigma_100

    tension = sigma_od*(1 - 0.024*pressure**0.45)

    if tension < 1 :
        tension = 1
    
    return tension*0.001 # n/m


def oil_density(fluid_model):

    oil_density = (62.4*fluid_model.Do + 0.0136*Rs_lasater(fluid_model)*fluid_model.Dg) / (Bo_standing(fluid_model))


    return oil_density