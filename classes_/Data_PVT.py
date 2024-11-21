
class PVT:

    def __init__(self,
                Bw : float,
                Bo : float,
                Bg : float,
                Rs : float,
                Rsw : float,
                water_rho: float, 
                oil_rho: float, 
                gas_rho: float, 
                water_viscosity: float, 
                gas_viscosity:  float,
                oil_viscosity: float,
                sigma_og : float,
                sigma_wg : float,
                pressure : float,
                temperature: float,
                Z :float,
                RGL : float,
                BSW : float, 
                flow_rate: float, 
                ) -> None:
        
        self.Bw = Bw
        self.Bo = Bo
        self.Bg = Bg 
        self.Rs = Rs 
        self.Rsw = Rsw 
        self.water_rho =  water_rho
        self.oil_rho = oil_rho
        self.gas_rho = gas_rho
        self.water_viscosity = water_viscosity
        self.gas_viscosity = gas_viscosity
        self.oil_viscosity = oil_viscosity
        self.sigma_og = sigma_og
        self.sigma_wg = sigma_wg
        self.pressure = pressure
        self.temperature = temperature
        self.RGL = RGL
        rgo = RGL/(1-BSW)
        self.RGO  = rgo
        self.BSW = BSW 
        self.rate = flow_rate
        self.Z = Z

        pass