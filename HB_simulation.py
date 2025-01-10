from infos_simulation import *

def HB_simulation( fluid, line, temp,) -> tuple:
    

    fluid_simulation = copy(fluid)
    step = 1
    i = 0
    vel = 0
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
                if line.direction == "Downhill":
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
                Hl  = HL_HB(flow_info,line)
                mass_flow = flow_liquid_mass*Hl + flow_gas_mass*( 1 - Hl)
                cp_mix = ( ( liquid_cp* Hl ) + cp_gas(fluid_simulation)*( 1 - Hl) )*1000

                if line.direction == "Downhill":
                    angle_temp = line.angle*-1
                else:
                    angle_temp = line.angle
                term1_temp =  (mass_flow*9.81*np.sin(angle_temp) ) / (temp.TEC)
                term2_temp = np.exp( ( (-temp.TEC) / (mass_flow*cp_mix)* (step) ))
                term3_temp = ( (t_inf) - ( term1_temp) - (fluid_simulation.T) )

                fluid_simulation.T = ( t_inf - term1_temp - (term2_temp*term3_temp) )
                
                if i == 0:
                    kinectic_Hb = 0
                else:
                    dif = ((mix_velocity**2 - vel**2))
                    kinectic_Hb  = (mix_slip_density_HB(flow_info,line)*dif)*step
                    kinectic_Hb = 0

                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - (gravitational_gradient_HB(flow_info,line)+friction_gradient_HB(flow_info,line))*step  - kinectic_Hb
                fluid_simulation.P = lose_pressure/100000

                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(flow_info.vm)
                vars[4].append(flow_info.vsg)
                vars[5].append(flow_info.vsl)
                vars[6].append(mix_slip_density_HB(flow_info,line))
                vars[7].append(slip_viscosity_Hb(flow_info,line))
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_HB(flow_info,line))
                vars[10].append(friction_gradient_HB(flow_info,line))
                vars[11].append(kinectic_Hb)

                vel = flow_info.vm

                

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
                Hl  = HL_HB(flow_info,line)
                
                if i == 0:
                    kinectic_Hb = 0
                else:
                    dif = ((mix_velocity**2 - vel**2))
                    kinectic_Hb  = (mix_slip_density_HB(flow_info,line)*dif)*step
                    kinectic_Hb = 0

                presure_fluid = fluid_simulation.P*100000
                lose_pressure = presure_fluid - (gravitational_gradient_HB(flow_info,line)+friction_gradient_HB(flow_info,line))*step  - kinectic_Hb
                fluid_simulation.P = lose_pressure/100000

                vars[0].append(fluid_simulation.P)
                vars[1].append(fluid_simulation.T)
                vars[2].append(Hl)
                vars[3].append(flow_info.vm)
                vars[4].append(flow_info.vsg)
                vars[5].append(flow_info.vsl)
                vars[6].append(mix_slip_density_HB(flow_info,line))
                vars[7].append(slip_viscosity_Hb(flow_info,line))
                vars[8].append(flow_info.z)
                vars[9].append(gravitational_gradient_HB(flow_info,line))
                vars[10].append(friction_gradient_HB(flow_info,line))
                vars[11].append(kinectic_Hb)
                
                vel = flow_info.vm


                
        if fluid_simulation.P < 15 :
            fluid_simulation.P = 0
            break
        if np.isnan(fluid_simulation.P ) == True:
            fluid_simulation.P = 0
            break

        print(fluid_simulation.P,Hl,fluid_simulation.T,i)

        i+= step

    return (fluid_simulation.T,fluid_simulation.P,vars)


def HB_simulation_pump( fluid, line, temp) -> tuple:
    

    fluid_simulation = copy(fluid)
    step = 1
    i = 0
    vel = 0


    while round(i,3) != line.L+step:

        fluid_simulation.T_pr = ( fluid_simulation.T*(9/5) + 491.67 ) / fluid.T_pc # rankine / rankine
        fluid_simulation.P_pr = (fluid_simulation.P*14.503773800722)/fluid.P_pc #psia/psia


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
            lose_pressure = presure_fluid + total_gradient_homogeneous(flow_info,line)*step
            fluid_simulation.P = lose_pressure/100000

        else:
            Hl  = HL_HB(flow_info,line)
            
            if i == 0:
                kinectic_Hb = 0
            else:
                dif = ((mix_velocity**2 - vel**2))
                kinectic_Hb  = (mix_slip_density_HB(flow_info,line)*dif)*step
                kinectic_Hb = 0

            presure_fluid = fluid_simulation.P*100000
            lose_pressure = presure_fluid + (gravitational_gradient_HB(flow_info,line)+friction_gradient_HB(flow_info,line))*step  + kinectic_Hb
            fluid_simulation.P = lose_pressure/100000

            vel = flow_info.vm


        print(fluid_simulation.P,Hl,fluid_simulation.T,i)

        i+= step

    return (fluid_simulation.P,fluid_simulation.T)