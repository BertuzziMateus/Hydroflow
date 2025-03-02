import matplotlib.pyplot as plt
from classes_.Data_fluid import *
from classes_.Data_PVT import *
from PVT_phases.Gas_phase import *
from PVT_phases.Oil_phase_standing import *
from PVT_phases.Water_phase import *

x = []
y = []
P = 350
while P >= 1 :
    fluid = Fluid_model(
        P = P, #bar  
        T = 86,#C 
        Dg = 0.71,
        Do = 0,
        API = 19.20,
        RGL = 90.7993,# sM^3/sM^3 
        BSW = 0, # %
        rate = 1092.04/86400 # m^3 /s
        ) 
    pvt = PVT(
            Bw = Bw(fluid), #  bbl/STb
            Bo = Bo_standing(fluid), # bbl/STb
            Bg = Bg(fluid), # scf/cf
            Rs = Rs_standing(fluid)*0.17810760667903525,  # sm^3 / m^3 - #scf/STb
            Rsw = Rsw_pure(fluid)*0.17810760667903525, # sm^3 / m^3 - #scf/STb
            water_rho = Water_density(fluid)*16.0185, # Kg / m^3 - #lb/scf
            oil_rho = Oil_Density_standing(fluid)*16.0185, # Kg / m^3 - #lb/ft**3
            gas_rho = Gas_density(fluid)*16.0185, # Kg / m^3 - #lb/ft**3
            water_viscosity = Water_viscosity(fluid)/1000, # Pa.s - #cP
            oil_viscosity = Oil_Viscosity_standing(fluid)/1000, # Pa.s - #cP
            gas_viscosity = Gas_Viscosity(fluid)/1000 , # Pa.s #cP
            Z = z(fluid),
            sigma_og = 0.00841, # N/m
            sigma_wg = 0.004,# N/m
            pressure = fluid.P*100000, # Pascal
            temperature = fluid.T + 273.15, # Kelvin
            BSW = fluid.BSW,
            RGL = fluid.RGL,
            flow_rate = 0)



    x.append(P)
    y.append(pvt.Bo)
    if P == 1:
        print(Pb_standing(fluid))
        print(pvt.oil_rho)
        print(pvt.Rs)
        print(pvt.Bo,'bo')
        print(pvt.Z)
        print(pvt.oil_viscosity,'vis')
        print(pvt.water_viscosity)

    P -= 1
#     print(Pb_standing(fluid))


plt.plot(x,y,c='k')
plt.xlabel('Pressão ($bar$)')
plt.ylabel('Densidade do óleo ($Kg/m³$)')
plt.grid(alpha=0.5)
plt.show()
