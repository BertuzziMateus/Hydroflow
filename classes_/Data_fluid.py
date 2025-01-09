class Fluid_model:
    def __init__(self,
                T: float, # ºC
                P: float, # bar
                Dg: float,
                Do: float,
                API: float,
                RGL: float,
                BSW: float,
                rate: float, # m^3 /s
                ) -> None:
        self.T = T # ºC
        self.P = P # bar

        self.RGL = RGL
        rgo = RGL/(1-BSW)
        self.RGO = rgo
        self.BSW = BSW
        self.rate = rate
            
        Ma = 0.0289655* Dg #kg/mol

    
        if (Do or API) != 0 :
            if API == 0 : 
                API = (141.5 / Do) - 131.5
            if Do == 0 : 
                Do = 141.5 / (API + 131.5)


        if Dg < 0.75:

            P_pc = 677 + 15*Dg - 37.5*Dg**2 #psia
            T_pc = 168 + 325*Dg - 12.5*Dg**2 #rankine

        else:
            P_pc = 706 - 51.7*Dg - 11.1*Dg**2 #psia
            T_pc = 187 + 330*Dg - 71.5*Dg**2 #rankine

        T_pr = ( T*(9/5) + 491.67 ) / T_pc # rankine / rankine
        P_pr = (P*14.503773800722)/P_pc #psia/psia

        self.Dg = Dg
        self.Do = Do
        self.API = API
        self.P_pc = P_pc
        self.T_pc = T_pc
        self.P_pr = P_pr
        self.T_pr = T_pr
        self.Ma = Ma
    pass
