from conversions import *


def Water_density_sc( fluid_model ) -> float: #lb/scf
    bsw = fluid_model.BSW*100
    return (62.368 + 0.438603*bsw + (1.60074e-3)*bsw)#*16.01846337396

def Rsw_pure( fluid_model ) -> float: # scf/bbl
    pressure = Bar_to_psia(fluid_model)
    A0 = 8.15839
    A1 = -6.12265e-2
    A2 = 1.91663e-4
    A3 = -2.1654e-7

    B0 = 1.01021e-2
    B1 = -7.44241e-5
    B2 = 3.05553e-7
    B3 = -2.94883e-10

    C0 = -9.02505
    C1 = 0.130237
    C2 = -8.53425e-4
    C3 = 2.34122e-6
    C4 = -2.37049e-9

    T = C_to_F(fluid_model)
    
    A = A0 + A1 * T + A2 * T**2 + A3 * T**3
    B = B0 + B1 * T + B2 * T**2 + B3 * T**3
    C = (C0 + C1 * T + C2 * T**2 + C3 * T**3 + C4 * T**4) * 1e-7

    rw = A + B*pressure + C*pressure**2
      
    return rw #* 0.17810776923 ? -> sm3/m3

def Rsw_brine( fluid_model ) -> float:# scf/stb
    bsw = fluid_model.BSW*100
    T = C_to_F(fluid_model)
    K = -0.0840655*bsw*(T**-0.285854)
    rsw_s = (10**K)*Rsw_pure(fluid_model)
    return rsw_s  #* 0.17810776923 ? -> sm3/m3

def Bw( fluid_model ) -> float: # bbl/stb
    pressure = Bar_to_psia(fluid_model)
    temperature = C_to_F(fluid_model)
    d_vwt = -1.0001e-2 + (1.33391e-4)*temperature + (5.50654e-7)*temperature**2
    d_vwp =  -(3.58922e-7 + (1.95301e-9)*temperature)*pressure - ( 2.25341e-10 + (1.72834e-13)*temperature )*pressure**2
    return (( 1 + d_vwt)*(1+d_vwp ))

def Water_viscosity( fluid_model ) -> float: #cP
    
    pressure = Bar_to_psia(fluid_model)

    S = fluid_model.BSW*100
    T = C_to_F(fluid_model)

    D = 1.12166 - (2.63951e-2)*S + (6.794961e-4)*(S**2)+ (5.47119e-5)*(S**3) - (1.55586e-6)*(S**4)

    uwt = (109.574 - 8.40564*S  + 0.313314*(S**2) + (8.72213e-3)*(S**3))*(T**-D)

    u = 0.9994 + (4.0295e-5)*pressure + (3.1062e-9)*(pressure**2 )

    return u*uwt

def Water_density( fluid_model ) -> float: #lb/scf
    return (Water_density_sc(fluid_model)/Bw(fluid_model))#*16.01846337396

