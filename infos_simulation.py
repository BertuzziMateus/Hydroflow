from classes_.Data_PVT import PVT
from classes_.Data_flow import *
from PVT_phases.Water_phase import *
from PVT_phases.Oil_phase_standing import *
from PVT_phases.Oil_phase_inidia_case import *
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
    rs = Rs_lasater(fluid)*0.17810760667903525  # sm^3 / m^3
    rsw = Rsw_pure(fluid)*0.17810760667903525  # sm^3 / m^3
    water_rho = Water_density(fluid)*16.01846337396014 # Kg / m^3
    oil_rho = oil_density(fluid)*16.01846337396014 # Kg / m^3
    gas_rho = Gas_density(fluid) # Kg / m^3
    water_viscosity = Water_viscosity(fluid) / 1000  # Pa.s 
    oil_viscosity = oil_viscosity_paper(fluid) / 1000 # Pa.s 
    gas_viscosity = gas_viscosity_lee(fluid) / 1000 # Pa.s 
    Z = z_hall(fluid)
    sigma_o_g = gas_oil_interfacial_tension(fluid) # N/m
    sigma_w_g = gas_water_interfacial_tension(fluid) # N/m
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
        pressure = 0, 
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
    flow_liquid_mass, flow_oil_mass , flow_gas_mass = Mass_flow_fractions(pvt,line)
    
    return(
        mix_velocity, liquid_velocity, gas_velocity,
        mix_rho, liquid_rho, gas_rho,
        mix_viscosity, liquid_viscosity, gasviscosity, waterviscosity,
        sigma_gl, fwc, λl,
        pvt.Z,
        liquid_cp,
        flow_liquid_mass, flow_oil_mass , flow_gas_mass
        )
