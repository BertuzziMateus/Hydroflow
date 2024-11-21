from infos_simulation import *




def bendisken_simulation( fluid, line, temp, ) -> tuple:
    

    fluid_simulation = copy(fluid)
    step = 1
    i = 0
    vars = [[],[],[],[],[],[],[],[],[],[],[],[]]

    while round(i,3) != line.L+step:

        fluid_simulation.T_pr = ( fluid_simulation.T*(9/5) + 491.67 ) / fluid.T_pc # rankine / rankine
        fluid_simulation.P_pr = (fluid_simulation.P*14.503773800722)/fluid.P_pc #psia/psia


        if temp != None:

            if (line.angle/(np.pi / 180)) == 90 or 0:
                H = line.L - round(i,3)
            else:
                H = (line.L - round(i,3))*np.sin(line.angle)

            
            t_inf = (round((temp.a*H) + temp.T1,3))
            
            mix_velocity, liquid_velocity, gas_velocity, mix_rho, liquid_rho, gas_rho, mix_viscosity, liquid_viscosity, gas_viscosity, water_viscosity, sigma_gl, fwc, λl,z_fluid,liquid_cp, flow_liquid_mass, flow_oil_mass , flow_gas_mass = flow_infos(fluid_simulation,line)
            
            

            flow_info = Flow_info(

                Vsl = liquid_velocity,
                Liquid_rho = liquid_rho,
                Liquid_viscosity = liquid_viscosity,
                Gas_liquid_sigma = sigma_gl,
                Vsg = gas_velocity,
                Gas_rho = gas_rho ,
                Gas_viscosity = gas_viscosity ,
                Vm = mix_velocity ,
                Mix_rho = mix_rho ,
                Mix_viscosity = mix_viscosity ,
                Pressure = fluid_simulation.P,
                Z = z_fluid,
                flow_liquid_mass = flow_liquid_mass,
                flow_oil_mass = flow_oil_mass,
                flow_gas_mass = flow_gas_mass,
                MM = fluid_simulation.Ma,
                Temperature = fluid_simulation.T,
                )
            
            PB = (Pb_standing(fluid)/14.504)
            if fluid_simulation.P > PB:
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
                Hl  = λl

                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - total_gradient_homogeneous(flow_info,line)*step
                fluid_simulation.P = lose_pressure/100000
                
                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(flow_info.vm)
                vars[4].append(flow_info.vsg)
                vars[5].append(flow_info.vsl)
                vars[6].append(flow_info.mix_rho)
                vars[7].append(flow_info.mix_viscosity)
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_homo(flow_info,line))
                vars[10].append(frictional_gradient_homo(flow_info,line))
                vars[11].append(kinetic_dl_t(flow_info,line)*total_gradient_homogeneous(flow_info,line))
               


            else:

                vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos(flow_info,line)

                if Hl < 0 :
                    raise('erro')
                mass_flow = flow_liquid_mass*Hl + flow_gas_mass*( 1 - Hl)
                cp_mix = ( ( liquid_cp* Hl ) + cp_gas(fluid_simulation)*( 1 - Hl) )*1000
                
                if line.direction == "Descendente":
                    angle_temp = line.angle*-1
                else:
                    angle_temp = line.angle
                
                term1_temp =  (mass_flow*9.81*np.sin(angle_temp) ) / (temp.TEC)
                term2_temp = np.exp( ( (-temp.TEC) / (mass_flow*cp_mix)* (step) ))
                term3_temp = ( (t_inf) - ( term1_temp) - (fluid_simulation.T) )

                fluid_simulation.T = ( t_inf - term1_temp - (term2_temp*term3_temp) )

                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - (totaL_gradient_bendi(flow_info,line))*step 
                fluid_simulation.P = lose_pressure/100000
                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(vm)
                vars[4].append(vsg)
                vars[5].append(vsl)
                vars[6].append(mix_rho)
                vars[7].append(mix_viscosity)
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_Ben(flow_info,line))
                vars[10].append(frictional_gradient_Ben(flow_info,line))
                vars[11].append(kinetic_gradient_Ben(flow_info,line))



        elif temp == None:
            
            if (line.angle/(np.pi / 180)) == 90 or 0:
                H = line.L - round(i,3)
            else:
                H = (line.L - round(i,3))*np.sin(line.angle)

            
           
            mix_velocity, liquid_velocity, gas_velocity, mix_rho, liquid_rho, gas_rho, mix_viscosity, liquid_viscosity, gas_viscosity, water_viscosity, sigma_gl, fwc, λl,z_fluid,liquid_cp, flow_liquid_mass, flow_oil_mass , flow_gas_mass = flow_infos(fluid_simulation,line)
            
            

            flow_info = Flow_info(

                Vsl = liquid_velocity,
                Liquid_rho = liquid_rho,
                Liquid_viscosity = liquid_viscosity,
                Gas_liquid_sigma = sigma_gl,
                Vsg = gas_velocity,
                Gas_rho = gas_rho ,
                Gas_viscosity = gas_viscosity ,
                Vm = mix_velocity ,
                Mix_rho = mix_rho ,
                Mix_viscosity = mix_viscosity ,
                Pressure = fluid_simulation.P,
                Z = z_fluid,
                flow_liquid_mass = flow_liquid_mass,
                flow_oil_mass = flow_oil_mass,
                flow_gas_mass = flow_gas_mass,
                MM = fluid_simulation.Ma,
                Temperature = fluid_simulation.T,
                )
            
            PB = (Pb_standing(fluid)/14.504)
            if fluid_simulation.P > PB:

                Hl  = λl
                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - total_gradient_homogeneous(flow_info,line)*step
                fluid_simulation.P = lose_pressure/100000
                
                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(flow_info.vm)
                vars[4].append(flow_info.vsg)
                vars[5].append(flow_info.vsl)
                vars[6].append(flow_info.mix_rho)
                vars[7].append(flow_info.mix_viscosity)
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_homo(flow_info,line))
                vars[10].append(frictional_gradient_homo(flow_info,line))
                vars[11].append(kinetic_dl_t(flow_info,line)*total_gradient_homogeneous(flow_info,line))
            


            else:

                vsg,vsl,vm,Hl,mix_rho,mix_viscosity,C0,vd = drift_infos(flow_info,line)

                if Hl < 0 :
                    raise('erro')

                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - (totaL_gradient_bendi(flow_info,line))*step 
                fluid_simulation.P = lose_pressure/100000
                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(vm)
                vars[4].append(vsg)
                vars[5].append(vsl)
                vars[6].append(mix_rho)
                vars[7].append(mix_viscosity)
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_Ben(flow_info,line))
                vars[10].append(frictional_gradient_Ben(flow_info,line))
                vars[11].append(kinetic_gradient_Ben(flow_info,line))

            



        print(fluid_simulation.P,Hl,fluid_simulation.T)

        if fluid_simulation.P < 0 :
            fluid_simulation.P = 0
            break
        
        if np.isnan(fluid_simulation.P) == True:
            fluid_simulation.P = 0
            break


        i+= step


    


    return (fluid_simulation.T,fluid_simulation.P,vars)