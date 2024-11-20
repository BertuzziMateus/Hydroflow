class Extern_Temperature:
    def __init__(self,
                 T1: float,
                 T2: float,
                 H : float,
                 TEC :float,)-> None:
          self.T1 = T1
          self.T2 = T2
          self.H = H
          a = (T2 - T1)  / (H)
          self.a = a
          self.TEC = TEC # W/M*K
    pass
