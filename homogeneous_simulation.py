from infos_simulation import *


def homogeneous_simulation( fluid, line, temp) -> tuple:

    step = 1
    i = 0
    vars = [[],[],[],[],[],[],[],[],[],[],[],[]]
    fluid_simulation = copy(fluid)

    while round(i,3) != line.L:

        fluid_simulation.T_pr = ( fluid_simulation.T*(9/5) + 491.67 ) / fluid.T_pc # rankine / rankine
        fluid_simulation.P_pr = (fluid_simulation.P*14.503773800722)/fluid.P_pc #psia/psia

        if temp != None:

            if (line.angle/(np.pi / 180)) == 90 or 0:
                H = line.L - round(i,3)
            else:
                H = round((line.L - round(i,3))*np.sin(line.angle),3)

            mix_velocity, liquid_velocity, gas_velocity, mix_rho, liquid_rho, gas_rho, mix_viscosity, liquid_viscosity, gasviscosity, waterviscosity, sigma_gl, fwc, λl,z_fluid, liquid_cp, flow_liquid_mass, flow_oil_mass , flow_gas_mass = flow_infos(fluid_simulation,line)
            
            flow_info = Flow_info(

                Vsl = liquid_velocity,
                Liquid_rho = liquid_rho,
                Liquid_viscosity = liquid_viscosity,
                Gas_liquid_sigma = sigma_gl,
                Vsg = gas_velocity,
                Gas_rho = gas_rho ,
                Gas_viscosity = gasviscosity ,
                Vm = mix_velocity ,
                Mix_rho = mix_rho ,
                Mix_viscosity = mix_viscosity ,
                Pressure = fluid_simulation.P*100000,
                Z = z_fluid,
                flow_liquid_mass = flow_liquid_mass,
                flow_oil_mass = flow_oil_mass,
                flow_gas_mass = flow_gas_mass,
                MM = fluid_simulation.Ma,
                Temperature = fluid_simulation.T,
                )
        
            t_inf = (round((temp.a*H) + temp.T1,2))
            mass_flow = flow_liquid_mass*λl + flow_gas_mass*( 1 - λl)
            cp_mix = ( ( liquid_cp* λl ) + cp_gas(fluid_simulation)*( 1 - λl) )*1000
            if line.direction == "Descendente":
                angle_temp = line.angle*-1
            else:
                angle_temp = line.angle
            term1_temp =  (mass_flow*9.81*np.sin(angle_temp) ) / (temp.TEC)
            term2_temp = np.exp( ( (-temp.TEC) / (mass_flow*cp_mix)* (step) ))
            term3_temp = ( (t_inf) - ( term1_temp) - (fluid_simulation.T) )
            fluid_simulation.T = ( t_inf - term1_temp - (term2_temp*term3_temp) )

            presure_fluid = fluid_simulation.P*100000
            lose_pressure = presure_fluid - total_gradient_homogeneous(flow_info,line)*step
            fluid_simulation.P = lose_pressure/100000
                
            vars[0].append(fluid_simulation.P)
            vars[1].append(fluid_simulation.T)
            vars[2].append(flow_info.λl)
            vars[3].append(flow_info.vm)
            vars[4].append(flow_info.vsg)
            vars[5].append(flow_info.vsl)
            vars[6].append(flow_info.mix_rho)
            vars[7].append(flow_info.mix_viscosity)
            vars[8].append(flow_info.z)
            vars[9].append(gravitational_gradient_homo(flow_info,line))
            vars[10].append(frictional_gradient_homo(flow_info,line))
            vars[11].append(kinetic_dl_t(flow_info,line)*total_gradient_homogeneous(flow_info,line))

        elif temp == None:
            
            if (line.angle/(np.pi / 180)) == 90 or 0:
                H = line.L - round(i,3)
            else:
                H = round((line.L - round(i,3))*np.sin(line.angle),3)

            mix_velocity, liquid_velocity, gas_velocity, mix_rho, liquid_rho, gas_rho, mix_viscosity, liquid_viscosity, gasviscosity, waterviscosity, sigma_gl, fwc, λl,z_fluid, liquid_cp, flow_liquid_mass, flow_oil_mass , flow_gas_mass = flow_infos(fluid_simulation,line)
            
            flow_info = Flow_info(

                Vsl = liquid_velocity,
                Liquid_rho = liquid_rho,
                Liquid_viscosity = liquid_viscosity,
                Gas_liquid_sigma = sigma_gl,
                Vsg = gas_velocity,
                Gas_rho = gas_rho ,
                Gas_viscosity = gasviscosity ,
                Vm = mix_velocity ,
                Mix_rho = mix_rho ,
                Mix_viscosity = mix_viscosity ,
                Pressure = fluid_simulation.P*100000,
                Z = z_fluid,
                flow_liquid_mass = flow_liquid_mass,
                flow_oil_mass = flow_oil_mass,
                flow_gas_mass = flow_gas_mass,
                MM = fluid_simulation.Ma,
                Temperature = fluid_simulation.T,
                )
                

            presure_fluid = fluid_simulation.P*100000
            lose_pressure = presure_fluid - total_gradient_homogeneous(flow_info,line)*step
            fluid_simulation.P = lose_pressure/100000
                
            vars[0].append(fluid_simulation.P)
            vars[1].append(fluid_simulation.T)
            vars[2].append(flow_info.λl)
            vars[3].append(flow_info.vm)
            vars[4].append(flow_info.vsg)
            vars[5].append(flow_info.vsl)
            vars[6].append(flow_info.mix_rho)
            vars[7].append(flow_info.mix_viscosity)
            vars[8].append(flow_info.z)
            vars[9].append(gravitational_gradient_homo(flow_info,line))
            vars[10].append(frictional_gradient_homo(flow_info,line))
            vars[11].append(kinetic_dl_t(flow_info,line)*total_gradient_homogeneous(flow_info,line))

        print(fluid_simulation.P,λl,fluid_simulation.T)
        old_pressure = presure_fluid
 
        if fluid_simulation.P < 0 :
            fluid_simulation.P = 0
            break
        if old_pressure < lose_pressure:
            fluid_simulation.P = 0
            break
        if np.isnan(fluid_simulation.P ) == True:
            fluid_simulation.P = 0

        i+= step

    return (fluid_simulation.T,fluid_simulation.P,vars)