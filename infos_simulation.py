from classes_.Data_PVT import PVT
from classes_.Data_flow import *
from PVT_phases.Water_phase import *
from PVT_phases.Oil_phase_standing import *
from PVT_phases.Gas_phase import *
from flow.flows import *
from models.homogeneous import * 
from models.Temperature import *
from models.Briggs import *
from models.HB import *
from models.Bendisken import *
from copy import copy
from models.bhagwat import *


def fluid_pvt(fluid) -> tuple:

    bg = Bg(fluid)
    bo = Bo_standing(fluid)
    bw = Bw(fluid)
    rs = Rs_standing(fluid)*0.17810760667903525  # sm^3 / m^3
    rsw = Rsw_brine(fluid)*0.17810760667903525  # sm^3 / m^3
    water_rho = Water_density(fluid)*16.0185 # Kg / m^3
    oil_rho = Oil_Density_standing(fluid)*16.0185 # Kg / m^3
    gas_rho = Gas_density(fluid)*16.0185 # Kg / m^3
    water_viscosity = Water_viscosity(fluid) / 1000 #Cp
    oil_viscosity = Oil_Viscosity_standing(fluid) / 1000 #Cp
    gas_viscosity = Gas_Viscosity(fluid) / 1000 #Cp
    Z = z(fluid)
    sigma_o_g =  0.00841 # N/m
    sigma_w_g = 0.004 # N/m
    return (bg, bo, bw, rs, rsw, water_rho, oil_rho,
            gas_rho, water_viscosity, oil_viscosity,
            gas_viscosity, Z, sigma_o_g, sigma_w_g)

def flow_infos(fluid, line ) -> tuple:
    bg, bo, bw, rs, rsw, water_rho, oil_rho,gas_rho, water_viscosity, oil_viscosity,gas_viscosity, z_fluid, sigma_o_g, sigma_w_g = fluid_pvt(fluid)
    pvt = PVT(
        Bw = bw,
        Bo = bo,
        Bg = bg,  
        Rs = rs,  
        Rsw = rsw,
        water_rho = water_rho,
        oil_rho = oil_rho,
        gas_rho =  gas_rho,
        water_viscosity = water_viscosity,
        oil_viscosity = oil_viscosity,
        gas_viscosity = gas_viscosity,
        Z = z_fluid,
        sigma_og = sigma_o_g, 
        sigma_wg = sigma_w_g,
        pressure = fluid.P*100000, # Pascal
        temperature = fluid.T + 273.15, # Kelvin
        RGL = fluid.RGL,
        BSW = fluid.BSW,
        flow_rate = fluid.rate, # m^3 /s
        )
    mix_velocity, liquid_velocity, gas_velocity = Velocity_phase(pvt,line)
    mix_rho, liquid_rho, gas_rho = Densitys(pvt)
    mix_viscosity, liquid_viscosity, gasviscosity, waterviscosity = Viscosity(pvt)
    sigma_gl = Gas_liquid_sigma(pvt)
    fwc, λl = Fractions(pvt)
    liquid_cp = cp_oil(fluid)* (1 - fwc) + cp_water(fluid)*fwc
    flow_liquid_mass, flow_oil_mass , flow_gas_mass = Mass_flow_fractions(pvt)
    
    return(
        mix_velocity, liquid_velocity, gas_velocity,
        mix_rho, liquid_rho, gas_rho,
        mix_viscosity, liquid_viscosity, gasviscosity, waterviscosity,
        sigma_gl, fwc, λl,
        pvt.Z,
        liquid_cp,
        flow_liquid_mass, flow_oil_mass , flow_gas_mass
        )
