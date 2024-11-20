from infos_simulation import *
from HB_simulation import *
from briggs_simulation import *
from bendisken_simulation import *


def pump_value_1(fluid, lines, temps, line_pump) -> float:

    incre = 0
    codition  = True
    fluid_simulation = copy(fluid)

    for i in range(len(lines)):
        line = lines[i]
        if temps != None:
            temp = temps[i]
        else:
            temp = None
        if round(line.angle*(180/np.pi)) == 90:
            temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
        else:
            temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)

        fluid_simulation.T,fluid_simulation.P = temperature,pressure
        
        if pressure <= 0 :
            break

    if pressure > 0 :
        pass
    else:
        incre = 50
        while codition == True:
            fluid_simulation = copy(fluid)
            for i in range(len(lines)):
                line = lines[i]
                if temps != None:
                    temp = temps[i]
                else:
                    temp = None

                if i == line_pump:
                    fluid_simulation.P = fluid_simulation.P + incre
                if round(line.angle*(180/np.pi)) == 90:
                    temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
                else:
                    temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)

                fluid_simulation.T,fluid_simulation.P = temperature,pressure

                if pressure == 0:
                    incre += 50
                    if line_pump > i:
                        raise ValueError("Your fluid don't came to the pump")
                    break

            if pressure > 1:
                codition  = False
                
        while pressure > 5:
            fluid_simulation = copy(fluid)
            for i, line in enumerate(lines):
                temp = temps[i] if temps is not None else None
                if i == line_pump:
                    fluid_simulation.P += incre

                if round(line.angle * (180 / np.pi)) == 90:
                    temperature, pressure, var = HB_simulation(fluid_simulation, line, temp)
                else:
                    temperature, pressure, var = briggs_simulation(fluid_simulation, line, temp)
                
                fluid_simulation.T, fluid_simulation.P = temperature, pressure

            if pressure > 50:
                incre -= 25
            elif pressure > 25:
                incre -= 10
            elif pressure > 15:
                incre -= 1
            elif pressure > 10:
                incre -= 0.5
            elif pressure > 5:
                incre -= 0.1
            else:
                break

    return incre

def simulation_1(fluid, lines, temps,line_pump)-> tuple:

    incre = round(pump_value_1(fluid,lines,temps,line_pump))
    if incre != 0:
        incre += 0.5
    fluid_simulation = copy(fluid)
    vars = [[],[],[],[],[],[],[],[],[],[],[],[]]
    
    for i in range(len(lines)):
        line = lines[i]
        if temps != None:
            temp = temps[i]
        else:
            temp = None

        if i == line_pump:
            fluid_simulation.P = fluid_simulation.P + incre

        if round(line.angle*(180/np.pi)) == 90:
            temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(var[0][j]) # PRESSÃO 
                vars[1].append(var[1][j]) # TEMPERATURA
                vars[2].append(var[2][j]) # HL
                vars[3].append(var[3][j]) # VM
                vars[4].append(var[4][j]) # VSG
                vars[5].append(var[5][j]) # VSL
                vars[6].append(var[6][j]) # M_DENSIDADE
                vars[7].append(var[7][j]) # M_VISC
                vars[8].append(var[8][j]) # Z
                vars[9].append(var[9][j]) # grav
                vars[10].append(var[10][j]) # fric
                vars[11].append(var[11][j]) # acel
        else:
            temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(var[0][j]) # PRESSÃO 
                vars[1].append(var[1][j]) # TEMPERATURA
                vars[2].append(var[2][j]) # HL
                vars[3].append(var[3][j]) # VM
                vars[4].append(var[4][j]) # VSG
                vars[5].append(var[5][j]) # VSL
                vars[6].append(var[6][j]) # M_DENSIDADE
                vars[7].append(var[7][j]) # M_VISC
                vars[8].append(var[8][j]) # Z
                vars[9].append(var[9][j]) # grav
                vars[10].append(var[10][j]) # fric
                vars[11].append(var[11][j]) # acel


        fluid_simulation.T,fluid_simulation.P = temperature,pressure

        

    return (temperature,pressure,vars,incre)



def pump_value_2(fluid, lines, temps, line_pump) -> float:

    incre = 0
    codition  = True
    fluid_simulation = copy(fluid)

    for i in range(len(lines)):
        line = lines[i]
        if temps != None:
            temp = temps[i]
        else:
            temp = None
        if round(line.angle*(180/np.pi)) == 90:
            temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
        else:
            temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)

        fluid_simulation.T,fluid_simulation.P = temperature,pressure

    if pressure > 0 :
        pass
    else:
        incre = 50
        while codition == True:
            fluid_simulation = copy(fluid)
            for i in range(len(lines)):
                line = lines[i]
                if temps != None:
                    temp = temps[i]
                else:
                    temp = None

                if i == line_pump:
                    fluid_simulation.P = fluid_simulation.P + incre
                if round(line.angle*(180/np.pi)) == 90:
                    temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
                else:
                    temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)

                fluid_simulation.T,fluid_simulation.P = temperature,pressure


            if np.isnan(pressure) == True:
                raise ValueError(f'Your fluid does not came to the pump')
            if pressure == 0:
                incre += 50
            else:
                codition  = False

        while codition ==  False:
            fluid_simulation = copy(fluid)
            for i in range(len(lines)):
                line = lines[i]
                if temps != None:
                    temp = temps[i]
                else:
                    temp = None

                if i == line_pump:
                    fluid_simulation.P = fluid_simulation.P + incre
                if round(line.angle*(180/np.pi)) == 90:
                    temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
                else:
                    temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)

                fluid_simulation.T,fluid_simulation.P = temperature,pressure

            if pressure > 50: 
                incre -= 25
            if pressure > 25: 
                incre -= 10
            elif pressure > 15: 
                incre -= 1
            elif pressure > 10: 
                incre -= 0.5
            elif pressure > 5: 
                incre -= 0.1

            if pressure == 0 or np.isnan(pressure) == True:
                incre += 7
            elif pressure <= 5 and pressure > 1: 
                codition  = True        
    
    return incre

def simulation_2(fluid, lines, temps,line_pump)-> tuple:
    
    incre = round(pump_value_2(fluid,lines,temps,line_pump))
    if incre != 0:
        incre += 0.5
    fluid_simulation = copy(fluid)
    vars = [[],[],[],[],[],[],[],[],[],[],[],[]]
    
    for i in range(len(lines)):
        line = lines[i]
        if temps != None:
            temp = temps[i]
        else:
            temp = None

        if i == line_pump:
            fluid_simulation.P = fluid_simulation.P + incre

        if round(line.angle*(180/np.pi)) == 90:
            temperature,pressure,var =   HB_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(var[0][j]) # PRESSÃO 
                vars[1].append(var[1][j]) # TEMPERATURA
                vars[2].append(var[2][j]) # HL
                vars[3].append(var[3][j]) # VM
                vars[4].append(var[4][j]) # VSG
                vars[5].append(var[5][j]) # VSL
                vars[6].append(var[6][j]) # M_DENSIDADE
                vars[7].append(var[7][j]) # M_VISC
                vars[8].append(var[8][j]) # Z
                vars[9].append(var[9][j]) # grav
                vars[10].append(var[10][j]) # fric
                vars[11].append(var[11][j]) # acel
        else:
            temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(var[0][j]) # PRESSÃO 
                vars[1].append(var[1][j]) # TEMPERATURA
                vars[2].append(var[2][j]) # HL
                vars[3].append(var[3][j]) # VM
                vars[4].append(var[4][j]) # VSG
                vars[5].append(var[5][j]) # VSL
                vars[6].append(var[6][j]) # M_DENSIDADE
                vars[7].append(var[7][j]) # M_VISC
                vars[8].append(var[8][j]) # Z
                vars[9].append(var[9][j]) # grav
                vars[10].append(var[10][j]) # fric
                vars[11].append(var[11][j]) # acel


        fluid_simulation.T,fluid_simulation.P = temperature,pressure

        

    return (temperature,pressure,vars,incre)
