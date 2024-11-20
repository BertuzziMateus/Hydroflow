import numpy as np

class pipe:

    def __init__(self,
                Dh : float,
                e : float,
                angle : float,
                L : float,
                direction : str
                ) -> None:
        self.Dh = Dh
        self.e = e
        self.direction = direction
        self.angle = round((angle)* (np.pi / 180),2)
        self.area = (np.pi * (Dh**2 )) /4
        self.e_Dh = e / Dh 
        self.L = L
        
        pass