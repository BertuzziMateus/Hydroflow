from infos_simulation import *
from HB_simulation import *
from briggs_simulation import *
from bendisken_simulation import *
from bhagwat_simulation import *

def pump_value(fluid, lines, temps, line_pump, inclined:str,vertical:str,horizontal:str)-> float:

    fluid_simulation = copy(fluid)
    temps = None
    lines_copy = copy(lines)

    if line_pump == 0:
        lines = lines[::-1] 
        if (vertical in ['Bendisken', 'Bhagwat'] and 
            horizontal in ['Bendisken', 'Bhagwat'] and 
            inclined in ['Bendisken', 'Bhagwat']):
            fluid_simulation.P = 25
        else:        
            fluid_simulation.P = 15
        for line in lines:
            if line.angle == 0 : 
                if horizontal == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_simulation,line,temps)
                elif horizontal  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_simulation,line,temps)
                    pressure *= 1.025
                elif horizontal == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_simulation,line,temps)
                elif horizontal == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_simulation,line,temps)
            elif round(line.angle*(180/np.pi)) == 90:
                if vertical == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_simulation,line,temps)
                elif vertical  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_simulation,line,temps)
                    pressure *= 1.025
                elif vertical == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_simulation,line,temps)
                elif vertical == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_simulation,line,temps)
            else:
                if inclined == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_simulation,line,temps)
                elif inclined  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_simulation,line,temps)
                    pressure *= 1.025
                elif inclined == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_simulation,line,temps)
                elif inclined == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_simulation,line,temps)

            fluid_simulation.P,fluid_simulation.T = pressure,temperature

        pump = fluid_simulation.P - fluid.P

        if pump < 0 :
            pump = 0
    else:
        line = 0 
        while line != line_pump:
            if lines[line].angle == 0 : 
                if horizontal == 'Beggs_Brill':
                    temperature,pressure,vars = briggs_simulation(fluid_simulation,lines[line],temps)
                elif horizontal  ==  'Hagedorn':
                    temperature,pressure,vars = HB_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bendisken':
                    temperature,pressure,vars = bendisken_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bhagwat':
                    temperature,pressure,vars = bhagwat_simulation(fluid_simulation,lines[line],temps)
            elif round(lines[line].angle*(180/np.pi)) == 90:
                if horizontal == 'Beggs_Brill':
                    temperature,pressure,vars = briggs_simulation(fluid_simulation,lines[line],temps)
                elif horizontal  ==  'Hagedorn':
                    temperature,pressure,vars = HB_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bendisken':
                    temperature,pressure,vars = bendisken_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bhagwat':
                    temperature,pressure,vars = bhagwat_simulation(fluid_simulation,lines[line],temps)
            else:
                if horizontal == 'Beggs_Brill':
                    temperature,pressure,vars = briggs_simulation(fluid_simulation,lines[line],temps)
                elif horizontal  ==  'Hagedorn':
                    temperature,pressure,vars = HB_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bendisken':
                    temperature,pressure,vars = bendisken_simulation(fluid_simulation,lines[line],temps)
                elif horizontal == 'Bhagwat':
                    temperature,pressure,vars = bhagwat_simulation(fluid_simulation,lines[line],temps)
            fluid_simulation.P,fluid_simulation.T = pressure,temperature
            if fluid_simulation.P == 0 :
                raise ValueError('Your fluid do not came to the pump')
            lines_copy.pop(0)
            line += 1
        fluid_pump  = copy(fluid)
        if (vertical in ['Bendisken', 'Bhagwat'] and 
            horizontal in ['Bendisken', 'Bhagwat'] and 
            inclined in ['Bendisken', 'Bhagwat']):
            fluid_pump.P = 25
        else:        
            fluid_pump.P = 15
        lines_copy = lines_copy[::-1]
        for line in lines_copy:
            if line.angle == 0 : 
                if horizontal == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_pump,line,temps)
                elif horizontal  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_pump,line,temps)
                    #pressure *= 1.025
                elif horizontal == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_pump,line,temps)
                elif horizontal == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_pump,line,temps)
            elif round(line.angle*(180/np.pi)) == 90:
                if vertical == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_pump,line,temps)
                elif vertical  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_pump,line,temps)
                    #pressure *= 1.025
                elif vertical == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_pump,line,temps)
                elif vertical == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_pump,line,temps)
            else:
                if inclined == 'Beggs_Brill':
                    pressure,temperature = briggs_simulation_pump(fluid_pump,line,temps)
                elif inclined  ==  'Hagedorn':
                    pressure,temperature = HB_simulation_pump(fluid_pump,line,temps)
                    #pressure *= 1.025
                elif inclined == 'Bendisken':
                    pressure,temperature = bendisken_simulation_pump(fluid_pump,line,temps)
                elif inclined == 'Bhagwat':
                    pressure,temperature = bhagwat_simulation_pump(fluid_pump,line,temps)
            fluid_pump.P,fluid_pump.T = pressure,temperature    
        pump = fluid_pump.P - fluid_simulation.P
        if pump < 0 :
            pump = 0

    return pump






def simulation(fluid, lines, temps,line_pump,inclined:str,vertical:str,horizontal:str)-> tuple:
    
    incre = round(pump_value(fluid,lines,temps,line_pump,inclined,vertical,horizontal)*1.05)
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
            if vertical == 'Beggs_Brill': 
                temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
            elif vertical  ==  'Hagedorn':
                temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
            elif vertical == 'Bendisken':
                temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
            elif vertical == 'Bhagwat':
                temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(round(var[0][j], 3)) # pressure 
                vars[1].append(round(var[1][j], 3)) # TEMP
                vars[2].append(round(var[2][j], 3)) # HL
                vars[3].append(round(var[3][j], 3)) # VM
                vars[4].append(round(var[4][j], 3)) # VSG
                vars[5].append(round(var[5][j], 3)) # VSL
                vars[6].append(round(var[6][j], 3)) # M_DENSIty
                vars[7].append(round(var[7][j], 3)) # M_VISC
                vars[8].append(round(var[8][j], 3)) # Z
                vars[9].append(round(var[9][j], 3)) # grav
                vars[10].append(round(var[10][j], 3)) # fri
        elif line.angle == 0:
            if horizontal == 'Beggs_Brill':
                temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
            elif horizontal  ==  'Hagedorn':
                temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
            elif horizontal == 'Bendisken':
                temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
            elif horizontal == 'Bhagwat':
                temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(round(var[0][j], 3)) # pressure 
                vars[1].append(round(var[1][j], 3)) # TEMP
                vars[2].append(round(var[2][j], 3)) # HL
                vars[3].append(round(var[3][j], 3)) # VM
                vars[4].append(round(var[4][j], 3)) # VSG
                vars[5].append(round(var[5][j], 3)) # VSL
                vars[6].append(round(var[6][j], 3)) # M_DENSIty
                vars[7].append(round(var[7][j], 3)) # M_VISC
                vars[8].append(round(var[8][j], 3)) # Z
                vars[9].append(round(var[9][j], 3)) # grav
                vars[10].append(round(var[10][j], 3)) # fri
        else:
            if inclined == 'Beggs_Brill':
                temperature,pressure,var = briggs_simulation(fluid_simulation,line,temp)
            elif inclined  ==  'Hagedorn':
                temperature,pressure,var = HB_simulation(fluid_simulation,line,temp)
            elif inclined == 'Bendisken':
                temperature,pressure,var = bendisken_simulation(fluid_simulation,line,temp)
            elif inclined == 'Bhagwat':
                temperature,pressure,var = bhagwat_simulation(fluid_simulation,line,temp)
            for j in range(len(var[0])):
                vars[0].append(round(var[0][j], 3)) # pressure 
                vars[1].append(round(var[1][j], 3)) # TEMP
                vars[2].append(round(var[2][j], 3)) # HL
                vars[3].append(round(var[3][j], 3)) # VM
                vars[4].append(round(var[4][j], 3)) # VSG
                vars[5].append(round(var[5][j], 3)) # VSL
                vars[6].append(round(var[6][j], 3)) # M_DENSIty
                vars[7].append(round(var[7][j], 3)) # M_VISC
                vars[8].append(round(var[8][j], 3)) # Z
                vars[9].append(round(var[9][j], 3)) # grav
                vars[10].append(round(var[10][j], 3)) # fri



        fluid_simulation.T,fluid_simulation.P = temperature,pressure

        

    return (temperature,pressure,vars,incre)
