import numpy as np 
    
class Flow_info:

    def __init__(self,
                Vsl : float,
                Liquid_rho : float,
                Liquid_viscosity : float,
                Gas_liquid_sigma : float,
                Vsg : float,
                Gas_rho : float,
                Gas_viscosity : float,
                Vm : float,
                Mix_rho : float,
                Mix_viscosity : float,
                Pressure : float,
                Z: float,
                flow_liquid_mass: float, 
                flow_oil_mass: float, 
                flow_gas_mass: float,
                MM = float,
                Temperature = float,
                ) -> None:
            self.vsl = Vsl
            self.vm = Vm
            self.vsg = Vsg
            λl = Vsl / Vm
            self.λl = λl
            self.liquid_rho = Liquid_rho
            self.liquid_viscosity = Liquid_viscosity
            self.gas_rho = Gas_rho
            self.gas_viscosity = Gas_viscosity
            self.mix_rho = Mix_rho
            self.mix_viscosity = Mix_viscosity
            self.gas_liquid_sigma = Gas_liquid_sigma
            self.pressure = Pressure
            self.z = Z
            self.flow_liquid_mass =  flow_liquid_mass
            self.flow_oil_mass = flow_oil_mass
            self.flow_gas_mass = flow_gas_mass
            self.MM = MM
            self.T = Temperature
            pass
