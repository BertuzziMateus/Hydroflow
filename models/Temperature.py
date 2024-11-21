
def cp_gas(fluid) -> float: #[kJ/kMol K]

    temperature  =  fluid.T +273.15
    Cp_metano = 4.568 - (8.975e-3)*temperature + (3.631e-5)*temperature**2  - (3.407e-8)*temperature**3 + (1.091e-11)*temperature**4 #[kJ/kMol K]
    Cp_etano =  4.221 - (8.782e-3)*temperature + (5.795e-5)*temperature**2  - (6.651e-8)*temperature**3 + (2.487e-11)*temperature**4 #[kJ/kMol K]
    metano_mass = 16.04/1000
    etano_mass =  30.07/1000
    a = (fluid.Ma - metano_mass) / (etano_mass - metano_mass)
    b = (Cp_etano-Cp_metano)

    cp_g = (a*b) + Cp_metano

    return cp_g

def cp_oil(fluid) -> float: #[kJ/kMol K]

    temperature  =  fluid.T +273.15
    cp_o =  ( (-1.39e-6*temperature + 1.847e-3)*(fluid.API) + (6.312e-4)*temperature  + 0.352)

    return cp_o*4.1868

def cp_water(fluid)->float: #[J/kMol K]
    temperature  =  fluid.T +273.15
    return (4.395 - (4.186e-3)*temperature + (1.405e-5)*temperature**2  - (1.564e-8)*temperature**3 + (6.320e-12)*temperature**4)


