from bhagwat_simulation import *
from bendisken_simulation import *
from briggs_simulation import *
from HB_simulation import *
from homogeneous_simulation import *
from copy import copy


def single_pump_value_teste(fluid, lines, temps, line_pump, mode:str)-> float:

    fluid_simulation = copy(fluid)
    temps = None
    lines_copy = copy(lines)

    if line_pump == 0:
        lines = lines[::-1]
        if (mode in ['Bendisken', 'Bhagwat']): 
            fluid_simulation.P = 25
        else:
            fluid_simulation.P = 15

        for line in lines:
            if mode == 'Homogeneous':
                pressure,temperature = homogeneous_simulation_pump(fluid_simulation,line,temps)
            if mode == 'Beggs_Brill':
                pressure,temperature = briggs_simulation_pump(fluid_simulation,line,temps)
            if mode  ==  'Hagedorn':
                pressure,temperature = HB_simulation_pump(fluid_simulation,line,temps)
                pressure *= 1.025
            if mode ==  'Bendisken':
                pressure,temperature = bendisken_simulation_pump(fluid_simulation,line,temps)
            if mode == 'Bhagwat':
                pressure,temperature = bhagwat_simulation_pump(fluid_simulation,line,temps)
            fluid_simulation.P,fluid_simulation.T = pressure,temperature

        pump = fluid_simulation.P - fluid.P

        if pump < 0 :
            pump = 0
    else:
        line = 0 
        while line != line_pump:
            if mode == 'Homogeneous':
                temperature,pressure,vars = homogeneous_simulation(fluid_simulation,lines[line],temps)
            if mode == 'Beggs_Brill':
                temperature,pressure,vars = briggs_simulation(fluid_simulation,lines[line],temps)
            if mode  == 'Hagedorn':
                temperature,pressure,vars = HB_simulation(fluid_simulation,lines[line],temps)
            if mode == 'Bendisken':
                temperature,pressure,vars = bendisken_simulation(fluid_simulation,lines[line],temps)
            if mode == 'Bhagwat':
                temperature,pressure,vars = bhagwat_simulation(fluid_simulation,lines[line],temps)
            fluid_simulation.P,fluid_simulation.T = pressure,temperature
            if fluid_simulation.P == 0 :
                raise ValueError('Your fluid do not came to the pump')

            lines_copy.pop(0)
            line += 1
        fluid_pump  = copy(fluid)
        if (mode in ['Bendisken', 'Bhagwat']):
            fluid_pump.P = 25
        else:        
            fluid_pump.P = 15
        lines_copy = lines_copy[::-1]
        for line in lines_copy:
            if mode == 'Homogeneous':
                pressure,temperature = homogeneous_simulation_pump(fluid_pump,line,temps)
            if mode == 'Beggs_Brill':
                pressure,temperature = briggs_simulation_pump(fluid_pump,line,temps)
            if mode == 'Hagedorn':
                pressure,temperature = HB_simulation_pump(fluid_pump,line,temps)
                #pressure *= 1.025
            if mode == 'Bendisken':
                pressure,temperature = bendisken_simulation_pump(fluid_pump,line,temps)
            if mode == 'Bhagwat':
                pressure,temperature = bhagwat_simulation_pump(fluid_pump,line,temps)
            fluid_pump.P,fluid_pump.T = pressure,temperature    
        pump = fluid_pump.P - fluid_simulation.P
        if pump < 0 :
            pump = 0


    return pump


def single_simulation(fluid, lines, temps,line_pump, mode:str)-> tuple:

    incre = round(single_pump_value_teste(fluid,lines,temps,line_pump,mode)*1.05)
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