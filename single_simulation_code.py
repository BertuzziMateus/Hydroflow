from bhagwat_simulation import *
from bendisken_simulation import *
from briggs_simulation import *
from HB_simulation import *
from homogeneous_simulation import *
from copy import copy


def single_pump_value(fluid, lines, temps, line_pump, mode:str)-> float:

    incre = 0
    codition  = True
    fluid_simulation = copy(fluid)

    for i in range(len(lines)):
        line = lines[i]
        if temps != None:
            temp = temps[i]
        else:
            temp = None

        if mode == "Homogeneous":
            temperature,pressure,var = homogeneous_simulation(fluid_simulation,line,temp)
        elif mode == "Hagedorn":
            temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
        elif mode == "Beggs_Brill":
            temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
        elif mode == "Bendisken":
            temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
        elif mode == "Bhagwat":
            temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)

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
                    
                if mode == "Homogeneous":
                    temperature,pressure,var = homogeneous_simulation(fluid_simulation,line,temp)
                elif mode == "Hagedorn":
                    temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
                elif mode == "Beggs_Brill":
                    temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
                elif mode == "Bendisken":
                    temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
                elif mode == "Bhagwat":
                    temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)   

                fluid_simulation.T,fluid_simulation.P = temperature,pressure

                if pressure == 0:
                    incre += 50
                    if line_pump > i:
                        raise ValueError("Your fluid don't came to the pump")
                    break

            if pressure > 5:
                codition  = False

        while codition == False:
            fluid_simulation = copy(fluid)
            for i, line in enumerate(lines):
                temp = temps[i] if temps is not None else None
                if i == line_pump:
                    fluid_simulation.P += incre

                if mode == "Homogeneous":
                    temperature,pressure,var = homogeneous_simulation(fluid_simulation,line,temp)
                elif mode == "Hagedorn":
                    temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
                elif mode == "Beggs_Brill":
                    temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
                elif mode == "Bendisken":
                    temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
                elif mode == "Bhagwat":
                    temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)
                

                fluid_simulation.T,fluid_simulation.P = temperature,pressure

            if pressure > 50:
                incre -= 10
            elif pressure > 20:
                incre -= 1
            if pressure == 0 or np.isnan(pressure) == True:
                incre += 2
            elif pressure < 20:
                break

    return incre


def single_simulation(fluid, lines, temps,line_pump, mode:str)-> tuple:

    incre = single_pump_value(fluid,lines,temps,line_pump,mode)
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
            
        if mode == "Homogeneous":
            temperature,pressure,var = homogeneous_simulation(fluid_simulation,line,temp)
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
 
        if mode == "Hagedorn":
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

        if mode == "Beggs_Brill":
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
    

        if mode == "Bendisken":
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

        if mode == "Bhagwat":
            temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)
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