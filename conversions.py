def C_to_F( Model  ) -> float:
    return (Model.T*(9/5) + 32)

def C_to_R( Model  ) -> float:
    return (Model.T*(9/5) + 491.67)

def C_to_K( Model ) -> float:
    return (Model.T + 273.15 )

def Bar_to_psia( Model  ) -> float:
    return (Model.P*14.503773773020924)

def Bar_to_pa( Model  ) -> float:
    return (Model.P*100000)
