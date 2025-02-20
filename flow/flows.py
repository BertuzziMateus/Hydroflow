
def Standard_coditions_flow_phase( pvt ) -> list:

    oil_flow_sc = pvt.rate * (1 - pvt.BSW)  #m³std/s
    water_flow_sc = pvt.rate * pvt.BSW  #m³std/s

    if pvt.BSW == 0 :
        gas_flow_sc = (oil_flow_sc )* (pvt.RGO)  #m³std/s
    elif pvt.BSW > 0:
        gas_flow_sc = (pvt.rate)*pvt.RGL  #m³std/s


    return [ water_flow_sc, oil_flow_sc, gas_flow_sc ]

def Situ_flow_phase( pvt ) -> list:

    water_sc,oil_sc,gas_sc = Standard_coditions_flow_phase(pvt) 
    water_flow = water_sc * (pvt.Bw) 
    oil_flow = oil_sc * (pvt.Bo) 

    if pvt.BSW == 0 :
        gas_flow = (pvt.RGO - pvt.Rs)*pvt.Bg*oil_sc
    elif pvt.BSW > 0:
        gas_flow = ( gas_sc - oil_sc*pvt.Rs - water_sc*pvt.Rsw)*pvt.Bg

    return [ water_flow, oil_flow, gas_flow ]

def Liquid_flow( pvt ) -> float:
    return  (Situ_flow_phase(pvt)[0] + Situ_flow_phase(pvt)[1])

def Gas_flow( pvt ) -> list:
    if Situ_flow_phase(pvt)[2] < 0:
        flow = 0
    else:
        flow = Situ_flow_phase(pvt)[2]
    return flow

def Mix_flow( pvt ) -> float:
    return  ( Liquid_flow(pvt) + Gas_flow(pvt) )

def Fractions( pvt  ) -> list:
    
    water_flow = Situ_flow_phase(pvt)[0]
    liquid_flow = Liquid_flow(pvt)
    
    fwc = water_flow / liquid_flow
    λl = liquid_flow / (liquid_flow + Gas_flow(pvt))

    return [fwc, λl ]

def Densitys( pvt ) -> list:
    
    fractions = Fractions(pvt)

    liquid_density = ( pvt.oil_rho*( 1 - fractions[0] ) + pvt.water_rho*fractions[0] )

    mix_density = ( (fractions[1] * liquid_density)  + ( (1 - fractions[1])*pvt.gas_rho) )

    return [ mix_density, liquid_density, pvt.gas_rho ]

def Viscosity( pvt ) -> list:

    fractions = Fractions(pvt)
    liquid_viscosity = ( pvt.oil_viscosity*( 1 - fractions[0] ) + pvt.water_viscosity*fractions[0] )
    mix_viscosity = ( fractions[1] * liquid_viscosity  + ( (1 - fractions[1])*pvt.gas_viscosity))

    return [ mix_viscosity, liquid_viscosity, pvt.gas_viscosity, pvt.water_viscosity]

def Velocity_phase( pvt, pipe ) -> list:

    mix_velocity = Mix_flow( pvt ) / pipe.area
    liquid_velocity = Liquid_flow( pvt ) / pipe.area
    gas_velocity = Gas_flow( pvt ) / pipe.area
    if gas_velocity < 0 :
        gas_velocity = 0

    return [ mix_velocity, liquid_velocity, gas_velocity]

def Gas_liquid_sigma( pvt ) -> float:
    fwc,_ = Fractions(pvt)
    return ( pvt.sigma_og * (1 - fwc) + pvt.sigma_wg*fwc)

def Mass_flow_fractions( pvt ) -> list:
    fwc = Fractions(pvt)[0]
    mass_flow_gas = pvt.gas_rho* Gas_flow(pvt) # kg /s
    mass_flow_oil = pvt.oil_rho*(1-fwc)*Situ_flow_phase(pvt)[1] # kg /s
    mass_flow_water = pvt.water_rho*(fwc)*Situ_flow_phase(pvt)[0] # kg /s
    mass_flow_liquid = mass_flow_oil + mass_flow_water # kg /s
    return [ mass_flow_liquid, mass_flow_oil, mass_flow_gas]



