import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from classes_.Data_fluid import *
from classes_.Data_pipe import *
from classes_.Data_temperature import *
from single_simulation_code import *
import pandas as pd
from presfil_simulation_code import*

def page1():
 
    st.title("Welcome to the Hydroflow!")
    st.divider()
    st.markdown(
        """
        <div style="text-align: justify;">
       
        I was developed to assist in the analysis of pipeline systems in the oil and gas industry, allowing you to explore different flow conditions and understand the behavior of the fluid throughout the system.

        To get started, you need to provide some essential information.

        First, enter the fluid properties, such as pressure, temperature, specific gravity, API gravity, gas-to-liquid ratio (GLR), and water cut (BSW). Next, configure the pipeline sections by specifying the hydraulic diameter, roughness, length, inclination angle, and flow orientation. If necessary, you can also define a thermal profile, choosing between an adiabatic condition or inputting the external temperatures of the sections.

        Additionally, you can select the flow model that best suits your system, including the drift-flux flow method, which allows me to adjust the calculations to reflect real-field conditions. If a pump is present in the system, simply specify its location, and I will simulate the impact of pumping on the fluid's behavior.

        Once you complete the data input, I will generate detailed graphs showing important variables such as pressure, temperature, density, and velocity along the pipeline length. These graphs will help you visually analyze the flow and identify critical points or necessary adjustments to the system.
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.divider()
    st.subheader("Let's look at an example of how to input the data into the proposed problem below.")
    st.image('case1.png')
    st.divider()
    

    P = st.number_input('Fluid pressure (bar)',230.0,230.0,step=0.1,format="%.3f")
    T = st.number_input('Fluid temperature (°C)',80.0,80.0,step=0.1,format="%.3f")
    Dg = st.number_input('Dg',0.8436,0.8436,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.8346,0.8346,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('API',0.0,50.0,step=0.1,format="%.3f")
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',157.0,157.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.2,0.2,step=0.1,format="%.3f" )
    rate = st.number_input('Required flow (m³/day)',3200.0,3200.0,step=0.1,format="%.3f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C z
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 

    copy_fluid = copy(fluid)

    st.divider()

    st.subheader('Fill in the information about the pipe sections below')
    sections = st.slider('How many sections?',1,5,value=3)
    sections = np.zeros(sections)
    colums = st.columns(len(sections))


    st.divider()


    section = {}
    DH = {}
    rug_abs = {}
    length = {}
    angle = {}
    direction_flow = {}


    for i in range(len(sections)):
        section[f'Section {i+1}'] = []
        DH[f'Hydraulic diameter (in) {i+1}'] = []
        rug_abs[f'Absolute roughness (in) {i+1}'] = []
        length[f'Length of the pipe (m) {i+1}'] = []
        angle[f'Angle (°) {i+1}'] = []
        direction_flow[f'Direction of flow {i+1}'] = []

    keys_section = list(section.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_len = list(length.keys())
    keys_ang = list(angle.keys())
    keys_direction = list(direction_flow.keys())



    for i in range(len(sections)):
        with colums[i]:
            if i == 0 : 
                st.header(keys_section[i])
                DH[f'Hydraulic diameter (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',4.0,4.0,step=0.01,format="%.3f")
                rug_abs[f'Absolute roughness (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0001,0.0001,step=0.01,format="%.4f")
                length[f'Length of the pipe (m) {i+1}'] = st.number_input(f'{keys_len[i] }', 580,580,step=1)
                angle[f'Angle (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',15.0,15.0,step=0.01,format="%.3f")
                direction_flow[f'Direction of flow {i+1}'] = st.selectbox(f'{keys_direction[i]}',['Uphill'])
            if i == 1:
                st.header(keys_section[i])
                DH[f'Hydraulic diameter (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',4.0,4.0,step=0.01,format="%.3f")
                rug_abs[f'Absolute roughness (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0001,0.0001,step=0.01,format="%.4f")
                length[f'Length of the pipe (m) {i+1}'] = st.number_input(f'{keys_len[i] }', 867,867,step=1)
                angle[f'Angle (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',10.0,10.0,step=0.01,format="%.3f")
                direction_flow[f'Direction of flow {i+1}'] = st.selectbox(f'{keys_direction[i]}',['Uphill'])
            if i == 2:
                st.header(keys_section[i])
                DH[f'Hydraulic diameter (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',4.0,4.0,step=0.01,format="%.3f")
                rug_abs[f'Absolute roughness (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0001,0.0001,step=0.01,format="%.4f")
                length[f'Length of the pipe (m) {i+1}'] = st.number_input(f'{keys_len[i] }', 1500,1500,step=1)
                angle[f'Angle (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',90.0,90.0,step=0.01,format="%.3f")
                direction_flow[f'Direction of flow {i+1}'] = st.selectbox(f'{keys_direction[i]}',['Uphill'])


    for i in range(len(sections)):
        section[f'Section {i+1}'] = pipe(
        Dh = DH[f'Hydraulic diameter (in) {i+1}'] * 0.0254, 
        e =  rug_abs[f'Absolute roughness (in) {i+1}'] * 0.0254, 
        L =  length[f'Length of the pipe (m) {i+1}']  , 
        angle = angle[f'Angle (°) {i+1}'],
        direction = direction_flow[f'Direction of flow {i+1}']
        )

    st.subheader('Models used in your simulation')
    
    col1,col2,col3 = st.columns(3)
    with col1:
        vertical = st.selectbox('For the vertical pipe section',['Hagedorn'])
    with col2:
        horizontal = st.selectbox('For the horizontal pipe section',['Beggs_Brill'])
    with col3:
        inclined = st.selectbox('For the inclined pipe section',['Beggs_Brill'])

    st.divider()


    st.subheader('Temperature profile ')
    adiabatic = st.checkbox("Adiabatic", value=False)

    if adiabatic == False:
        colums = st.columns(len(sections))
        temp = {}
        infinity_ti = {}
        infinity_tf = {}
        vertical_height = {}
        TEC = {}
        
        for i in range(len(sections)):
            infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = []
            infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = []
            vertical_height[f'Vertical height (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []
            


        keys_Ti = list(infinity_ti.keys())
        keys_Tf = list(infinity_tf.keys())
        keys_height = list(vertical_height.keys())
        keys_TEC = list(TEC.keys())

        for i in range(len(sections)):
            with colums[i]:
                if i == 0:
                    st.header(keys_section[i])  
                    temp[f'Section {i+1}'] = []
                    infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Ti [i] }',4.0,4.0, step=0.01,format="%.3f")
                    infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Tf [i] }',80.0,80.0, step=0.01,format="%.3f")
                    vertical_height[f'Vertical height (m) {i+1}'] = st.number_input(f'{keys_height [i] }',150,150,step=1)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',4.0,4.0,step=0.01, format="%.3f")
                if i == 1:
                    st.header(keys_section[i])  
                    temp[f'Section {i+1}'] = []
                    infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Ti [i] }',22.0,22.0, step=0.01,format="%.3f")
                    infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Tf [i] }',4.0,4.0, step=0.01,format="%.3f")
                    vertical_height[f'Vertical height (m) {i+1}'] = st.number_input(f'{keys_height [i] }',1650,1650,step=1)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',0.6,0.6,step=0.01, format="%.3f")
                if i == 2:
                    st.header(keys_section[i])  
                    temp[f'Section {i+1}'] = []
                    infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Ti [i] }',22.0,22.0, step=0.01,format="%.3f")
                    infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Tf [i] }',5.5,5.5, step=0.01,format="%.3f")
                    vertical_height[f'Vertical height (m) {i+1}'] = st.number_input(f'{keys_height [i] }',1500,1500,step=1)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',0.6,0.6,step=0.01, format="%.3f")
                
        for i in range(len(sections)):
            temp[f'Section {i+1}'] = Extern_Temperature(
                infinity_ti[f'Initial infinite temperature (ºC) {i+1}'],
                infinity_tf[f'Final infinite temperature (ºC) {i+1}'],
                vertical_height[f'Vertical height (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )  
    else:
        pass
    

    lines = []
    temps = []
    for i in range(len(sections)):
        lines.append(section[f'Section {i+1}'])
        if adiabatic == False:
            temps.append(temp[f'Section {i+1}'])
        else:
            temps = None

    st.divider()

    st.subheader('Which section is it located the pump')


    pump_line = st.selectbox('If a pump is necessary, which section is it located in?',keys_section[1])

    for i in range(len(sections)):
        if pump_line == keys_section[i]:
            pump_line = i

       
    st.divider()


    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #1D2D50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            white-space: nowrap;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("Simulation"):
        variables = []
        pressures = []
        temperatures = []
        HLS = []
        VSMS = []
        densities = []
        viscosities = []
        Zs  = []
        grav = []
        fric = []
        ace = []

           
        with st.container():
            with st.spinner('Simulating...'):
                try:
                    T,P,var,pump = simulation(fluid,lines,temps,pump_line,inclined,vertical,horizontal)
                    variables.append(var)
                    comp = np.arange(0,len(variables[0][0]),1)

                    for i in range(len(variables[0][0])):
                        pressures.append(variables[0][0][i])
                        temperatures.append(variables[0][1][i])
                        HLS.append(variables[0][2][i])
                        VSMS.append(variables[0][3][i])
                        densities.append(variables[0][6][i])
                        viscosities.append(variables[0][7][i])
                        Zs.append(variables[0][8][i])
                        grav.append(variables[0][9][i])
                        fric.append(variables[0][10][i])
                        #ace.append(variables[0][11][i])

                    bubble_points = []
                    for i in range(len(variables[0][0])):
                        copy_fluid.T = temperatures[i]
                        bubble_points.append(Pb_standing(copy_fluid)*0.0689475729)

                    custom_style = {
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 12,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 14,  # Tamanho do título do gráfico
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 12,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 12,  # Tamanho do texto dos ticks no eixo y
                        'lines.linewidth': 2,  # Espessura das linhas dos gráficos
                        'lines.markersize': 6,  # Tamanho dos marcadores
                        'legend.fontsize': 10,  # Tamanho da legenda
                        'legend.frameon': False,  # Remove a moldura ao redor da legenda
                        'legend.loc': 'best',  # Melhor posição automática para a legenda
                        'figure.figsize': (8, 6),  # Tamanho padrão da figura (polegadas)
                        'savefig.dpi': 600,  # Alta resolução para exportação (publicação)
                        'savefig.bbox': 'tight',  # Salva a imagem sem cortar parte do gráfico
                        }
                
                    plt.rcParams.update(custom_style)

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressure", "Temperature","HL","Vsm","Densities","Z"])

                    fig1, ax1 = plt.subplots()
                    ax1.plot(comp, bubble_points, lw =2 , ls='--',c='#F08080' ,label='Bubble pressure',zorder=2)
                    ax1.scatter(comp[-1],pressures[-1],c='#1D2D50',zorder=4,label='Separator')
                    ax1.scatter(comp[0],pressures[0],c='#87CEEB',zorder=5,label='Reservoir')
                    ax1.plot(comp,pressures,label=f'Pressure',c='k',zorder=3)
                    ax1.set_xlabel(f'Lenght pipe [$m$]')
                    ax1.set_ylabel(f'Pressure [$bar$]')
                    ax1.set_title(f'Fluid pressure across the pipe')
                    ax1.grid(alpha=0.5,zorder=1)
                    ax1.margins(x=0.1, y=0.1)
                    ax1.legend()
                    tab1.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    ax2.plot(comp,temperatures,label=f'Temperature',c='k',zorder=2)
                    ax2.scatter(comp[-1],temperatures[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax2.scatter(comp[0],temperatures[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax2.set_xlabel(f'Lenght pipe [$m$]')
                    ax2.set_ylabel(f'Temperature [$ºC$]')
                    ax2.set_title(f'Fluid temperature across the pipe')
                    ax2.grid(alpha=0.5,zorder=1)
                    ax2.margins(x=0.1, y=0.1)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    ax3.plot(comp,HLS,label=f'Fluid holdup',c='k',zorder=2)
                    ax3.scatter(comp[-1],HLS[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax3.scatter(comp[0],HLS[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax3.set_xlabel(f'Lenght pipe [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'Fluid Holdup across the pipe')
                    ax3.grid(alpha=0.5,zorder=1)
                    ax3.margins(x=0.1, y=0.1)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    ax4.plot(comp,VSMS,label=f'Fluid velocity',c='k',zorder=2)
                    ax4.scatter(comp[-1],VSMS[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax4.scatter(comp[0],VSMS[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax4.set_xlabel(f'Lenght pipe [$m$]')
                    ax4.set_ylabel(f'Fluid velocity [$m/s$]')
                    ax4.set_title(f'Fluid velocity across the pipe')
                    ax4.grid(alpha=0.5,zorder=1)
                    ax4.margins(x=0.1, y=0.1)
                    ax4.legend()
                    tab4.pyplot(fig4)

                    fig5, ax5 = plt.subplots()
                    ax5.plot(comp,densities,label=f'Fluid density',c='k',zorder=2)
                    ax5.scatter(comp[-1],densities[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax5.scatter(comp[0],densities[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax5.set_xlabel(f'Lenght pipe [$m$]')
                    ax5.set_ylabel(f'Density [Kg/m³]')
                    ax5.set_title(f'Fluid density across the pipe')
                    ax5.grid(alpha=0.5,zorder=1)
                    ax5.margins(x=0.1, y=0.1)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    ax7.plot(comp,Zs,label=f'Factor Z of the fluid',c='k',zorder=2)
                    ax7.scatter(comp[-1],Zs[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax7.scatter(comp[0],Zs[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax7.set_xlabel(f'Lenght of the pipe [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Factor Z across the pipe')
                    ax7.grid(alpha=0.5,zorder=1)
                    ax7.margins(x=0.1, y=0.1)
                    ax7.legend()
                    tab7.pyplot(fig7) 
                    
                    st.divider()

                    
    
                    results1 = [P,T,pump]
                    colums = ['Values']
                    index1 = ["Pressure at separator (bar)", "Temperature at separator (ºC)","Pump increment (bar)"]
                    df_results_1 = pd.DataFrame(results1,index=index1,columns=colums)


                    grav_med = (sum(grav)/(len(variables[0][0])))/100000
                    fric_med = (sum(fric)/(len(variables[0][0])))/100000
                    total_med = sum((grav_med,fric_med))
                    results_2 = [grav_med,fric_med,total_med]
                    index_2 = ["Gravitational lose (bar/m)","Friccional lose (bar/m)","Total lose (bar/m)"]

                    df_results_2 = pd.DataFrame(results_2,index=index_2,columns=colums)

                    st.subheader('Tables with the main results')

                    col1,col2 = st.columns(2)
                    with col1:
                        st.dataframe(df_results_1.style.format("{:.3f}"))
                    with col2:
                        st.dataframe(df_results_2.style.format("{:.3f}"))

                    st.divider()

                except:
                    st.error("Error when simulating")

    pass
    

def page2():

    st.title('Fill in the necessary information for the fluid below ')

    st.divider()

    P = st.number_input('Fluid pressure (bar)',0.00,1500.0,step=0.1,format="%.3f")
    T = st.number_input('Fluid temperature (°C)',0.0,150.0,step=0.1,format="%.3f")
    Dg = st.number_input('Dg',0.0,1.0,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.0,1.0,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('API',0.0,50.0,step=0.1,format="%.3f")
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',1.0,500.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.0,1.0,step=0.1,format="%.3f" )
    rate = st.number_input('Required flow (m³/day)',2.0,10000.0,step=0.1,format="%.3f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C z
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 

    copy_fluid = copy(fluid)

    st.divider()

    st.subheader('Fill in the information about the pipe sections below')
    sections = st.slider('How many sections?',1,5)
    sections = np.zeros(sections)
    colums = st.columns(len(sections))


    st.divider()


    section = {}
    DH = {}
    rug_abs = {}
    length = {}
    angle = {}
    direction_flow = {}


    for i in range(len(sections)):
        section[f'Section {i+1}'] = []
        DH[f'Hydraulic diameter (in) {i+1}'] = []
        rug_abs[f'Absolute roughness (in) {i+1}'] = []
        length[f'Length of the pipe (m) {i+1}'] = []
        angle[f'Angle (°) {i+1}'] = []
        direction_flow[f'Direction of flow {i+1}'] = []

    keys_section = list(section.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_len = list(length.keys())
    keys_ang = list(angle.keys())
    keys_direction = list(direction_flow.keys())



    for i in range(len(sections)):
        with colums[i]:
            st.header(keys_section[i])
            DH[f'Hydraulic diameter (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',1.5,10.0,step=0.01,format="%.3f")
            rug_abs[f'Absolute roughness (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0001,2.5,step=0.01,format="%.4f")
            length[f'Length of the pipe (m) {i+1}'] = st.number_input(f'{keys_len[i] }', step=1)
            angle[f'Angle (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',0.0,90.0,step=0.01,format="%.3f")
            direction_flow[f'Direction of flow {i+1}'] = st.selectbox(f'{keys_direction[i]}',['Uphill','Downhill'])

    for i in range(len(sections)):
        section[f'Section {i+1}'] = pipe(
        Dh = DH[f'Hydraulic diameter (in) {i+1}'] * 0.0254, 
        e =  rug_abs[f'Absolute roughness (in) {i+1}'] * 0.0254, 
        L =  length[f'Length of the pipe (m) {i+1}']  , 
        angle = angle[f'Angle (°) {i+1}'],
        direction = direction_flow[f'Direction of flow {i+1}']
        )
    
    st.subheader('Models used in your simulation, this model is used in all sections.')
    
    c1,c2 = st.columns(2)

    with c1:
        Homo = st.checkbox("Homogeneous")
        BB = st.checkbox("Beggs and Brill")
        HB = st.checkbox("Hagedorn")
    with c2:
        ben = st.checkbox("Bendisken")
        bha = st.checkbox("Bhagwat")

         
    options = []

    if Homo == True:
        options.append('Homogeneous')
    if BB == True:
        options.append('Beggs_Brill')
    if HB == True:
        options.append('Hagedorn')
    if ben == True:
        options.append('Bendisken')
    if bha == True:
        options.append('Bhagwat')

    st.divider()

    st.subheader('Temperature profile ')
    adiabatic = st.checkbox("Adiabatic")

    if adiabatic == False:
        colums = st.columns(len(sections))
        temp = {}
        infinity_ti = {}
        infinity_tf = {}
        vertical_height = {}
        TEC = {}
        
        for i in range(len(sections)):
            infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = []
            infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = []
            vertical_height[f'Vertical height (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []
            


        keys_Ti = list(infinity_ti.keys())
        keys_Tf = list(infinity_tf.keys())
        keys_height = list(vertical_height.keys())
        keys_TEC = list(TEC.keys())

        for i in range(len(sections)):
            with colums[i]:
                st.header(keys_section[i])  
                temp[f'Section {i+1}'] = []
                infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Ti [i] }', step=0.01,format="%.3f")
                infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Tf [i] }', step=0.01,format="%.3f")
                vertical_height[f'Vertical height (m) {i+1}'] = st.number_input(f'{keys_height [i] }',1,1000000,step=1)
                TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',step=0.01, format="%.3f")

        for i in range(len(sections)):
            temp[f'Section {i+1}'] = Extern_Temperature(
                infinity_ti[f'Initial infinite temperature (ºC) {i+1}'],
                infinity_tf[f'Final infinite temperature (ºC) {i+1}'],
                vertical_height[f'Vertical height (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )  
    else:
        pass
    

    lines = []
    temps = []
    for i in range(len(sections)):
        lines.append(section[f'Section {i+1}'])
        if adiabatic == False:
            temps.append(temp[f'Section {i+1}'])
        else:
            temps = None

    st.divider()

    st.subheader('Which section is it located the pump')

    pump_line = st.selectbox('If a pump is necessary, which section is it located in?',section)

    for i in range(len(sections)):
        if pump_line == keys_section[i]:
            pump_line = i


    st.divider()

    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #1D2D50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            white-space: nowrap;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("Simulation"):
        variables = []
        pressures = []
        temperatures = []
        HLS = []
        VSMS = []
        densities = []
        viscosities = []
        Zs  = []
        grav = []
        fric = []
        ace = []

        
        for i in range(len(options)):
            variables.append([])
            pressures.append([])
            temperatures.append([])
            HLS.append([])
            VSMS.append([])
            densities.append([])
            viscosities.append([])
            Zs.append([])
            grav.append([])
            fric.append([])
            #ace.append([])
        
        with st.container():
            with st.spinner('Simulating...'):
                try:
                    lastest_pressures = []
                    lastest_tempertarutes = []
                    pumps = []
                    for i in range(len(options)):
                        T,P,var,pump = single_simulation(fluid,lines,temps,pump_line,options[i])
                        variables[i].append([T,P,var,pump])
                        lastest_pressures.append(P)
                        lastest_tempertarutes.append(T)
                        pumps.append(pump)
                        st.success(f'The {options[i]} model finished the simulation without errors')


                    comp = np.arange(0,len(variables[0][0][2][0]),1)
    
                    for i in range(len(variables)):
                        pressures[i].append(variables[i][0][2][0])
                        temperatures[i].append(variables[i][0][2][1])
                        HLS[i].append(variables[i][0][2][2])
                        VSMS[i].append(variables[i][0][2][3])
                        densities[i].append(variables[i][0][2][6])
                        viscosities[i].append(variables[i][0][2][7])
                        Zs[i].append(variables[i][0][2][8])
                        grav[i].append(variables[i][0][2][9])
                        fric[i].append(variables[i][0][2][10])
                        #ace[i].append(variables[i][0][2][11])
                        
                    bubble_points = []
                    for i in range(len(variables[0][0][2][1])):
                        copy_fluid.T = temperatures[0][0][i]
                        bubble_points.append(Pb_standing(copy_fluid)*0.0689475729)

                    custom_style = {
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 12,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 14,  # Tamanho do título do gráfico
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 12,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 12,  # Tamanho do texto dos ticks no eixo y
                        'lines.linewidth': 2,  # Espessura das linhas dos gráficos
                        'lines.markersize': 6,  # Tamanho dos marcadores
                        'legend.fontsize': 9,  # Tamanho da legenda
                        'legend.frameon': False,  # Remove a moldura ao redor da legenda
                        'legend.loc': 'best',  # Melhor posição automática para a legenda
                        'figure.figsize': (8, 6),  # Tamanho padrão da figura (polegadas)
                        'savefig.dpi': 600,  # Alta resolução para exportação (publicação)
                        'savefig.bbox': 'tight',  # Salva a imagem sem cortar parte do gráfico
                        }
                
                
                    plt.rcParams.update(custom_style)

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressure", "Temperature","HL","Vsm","Densities","Z"])
                    
                    colors ={
                        0:'k',
                        1:'r',
                        2:'g',
                        3:'b',
                        4:'y',
                        5:'c',
                    }

                    fig1, ax1 = plt.subplots()
                    for i in range(len(pressures)):
                        ax1.plot(comp,pressures[i][0],label=f'Pressure with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax1.plot(comp, bubble_points, lw =2 , ls='--',c='#F08080' ,label='Bubble pressure',zorder=2)
                    ax1.set_xlabel(f'Lenght pipe [$m$]')
                    ax1.set_ylabel(f'Pressure [$bar$]')
                    ax1.set_title(f'Fluid pressure across the pipe')
                    ax1.grid(alpha=0.5,zorder=1)
                    ax1.margins(x=0.1, y=0.1)
                    ax1.legend()
                    tab1.pyplot(fig1)


                    fig2, ax2 = plt.subplots()
                    for i in range(len(temperatures)):
                        ax2.plot(comp,temperatures[i][0],label=f'Temperature with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax2.set_xlabel(f'Lenght pipe [$m$]')
                    ax2.set_ylabel(f'Temperature [$ºC$]')
                    ax2.set_title(f'Fluid temperature across the pipe')
                    ax2.grid(alpha=0.5,zorder=1)
                    ax2.margins(x=0.1, y=0.1)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    for i in range(len(HLS)):
                        ax3.plot(comp,HLS[i][0],label=f'Fluid holdup with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax3.set_xlabel(f'Lenght pipe [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'Fluid Holdup across the pipe')
                    ax3.grid(alpha=0.5,zorder=1)
                    ax3.margins(x=0.1, y=0.1)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    for i in range(len(VSMS)):
                        ax4.plot(comp,VSMS[i][0],label=f'Fluid velocity with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax4.set_xlabel(f'Lenght pipe [$m$]')
                    ax4.set_ylabel(f'Fluid velocity [$m/s$]')
                    ax4.set_title(f'Fluid velocity across the pipe')
                    ax4.grid(alpha=0.5,zorder=1)
                    ax4.margins(x=0.1, y=0.1)
                    ax4.legend()
                    tab4.pyplot(fig4)

                  
                    fig5, ax5 = plt.subplots()
                    for i in range(len(densities)):
                        ax5.plot(comp,densities[i][0],label=f'Fluid density with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax5.set_xlabel(f'Lenght pipe [$m$]')
                    ax5.set_ylabel(f'Density [Kg/m³]')
                    ax5.set_title(f'Fluid density across the pipe')
                    ax5.grid(alpha=0.5,zorder=1)
                    ax5.margins(x=0.1, y=0.1)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    for i in range(len(Zs)):
                        ax7.plot(comp,Zs[i][0],label=f'Factor Z of the fluid with {options[i]} model.',c=colors[i] ,zorder=3)
                    ax7.set_xlabel(f'Lenght of the pipe [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Factor Z across the pipe')
                    ax7.grid(alpha=0.5,zorder=1)
                    ax7.margins(x=0.1, y=0.1)
                    ax7.legend()
                    tab7.pyplot(fig7) 

                    st.divider()

                    results_1= []
                    for i in range(len(options)):
                        results_1.append([lastest_pressures[i],lastest_tempertarutes[i],pumps[i]]) 
                    
                    index1 = []
                    colum1 = ["Pressure at separator (bar)", "Temperature at separator (ºC)","Pump increment (bar)"]
                    for index in options:
                        index1.append(index)   

                    df_results_1 = pd.DataFrame(results_1,index=index1,columns=colum1)


                    results_2 = []
                    for i in range(len(options)):
                        grav_med = (sum(grav[i][0])/len(grav[i][0]))/100000
                        fric_med = (sum(fric[i][0])/len(fric[i][0]))/100000
                        total_med = grav_med+fric_med
                        results_2.append([grav_med,fric_med,total_med])
                    colum2 = ["Gravitational lose (bar/m)","Friccional lose (bar/m)","Total lose (bar/m)"]

                    df_results_2 = pd.DataFrame(results_2,index=index1,columns=colum2)

                    st.subheader('Tables with the main results')

                    st.dataframe(df_results_1.style.format("{:.3f}"))
                    st.dataframe(df_results_2.style.format("{:.3f}"))


                    st.divider()

                except:
                    st.error("Erro ao simular")
    
    pass

def page3():
    
    st.title('Fill in the necessary information for the fluid below ')

    st.divider()

    P = st.number_input('Fluid pressure (bar)',0.00,700.00,step=0.1,format="%.3f")
    T = st.number_input('Fluid temperature (°C)',0.0,150.0,step=0.1,format="%.3f")
    Dg = st.number_input('Dg',0.0,1.0,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.0,1.0,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('API',0.0,50.0,step=0.1,format="%.3f")
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',1.0,500.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.0,1.0,step=0.1,format="%.3f" )
    rate = st.number_input('Required flow (m³/day)',50.0,10000.0,step=0.1,format="%.3f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C z
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 

    copy_fluid = copy(fluid)

    st.divider()

    st.subheader('Fill in the information about the pipe sections below')
    sections = st.slider('How many sections?',1,5)
    sections = np.zeros(sections)
    colums = st.columns(len(sections))


    st.divider()


    section = {}
    DH = {}
    rug_abs = {}
    length = {}
    angle = {}
    direction_flow = {}


    for i in range(len(sections)):
        section[f'Section {i+1}'] = []
        DH[f'Hydraulic diameter (in) {i+1}'] = []
        rug_abs[f'Absolute roughness (in) {i+1}'] = []
        length[f'Length of the pipe (m) {i+1}'] = []
        angle[f'Angle (°) {i+1}'] = []
        direction_flow[f'Direction of flow {i+1}'] = []

    keys_section = list(section.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_len = list(length.keys())
    keys_ang = list(angle.keys())
    keys_direction = list(direction_flow.keys())



    for i in range(len(sections)):
        with colums[i]:
            st.header(keys_section[i])
            DH[f'Hydraulic diameter (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',2.5,10.0,step=0.01,format="%.3f")
            rug_abs[f'Absolute roughness (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0001,2.5,step=0.01,format="%.4f")
            length[f'Length of the pipe (m) {i+1}'] = st.number_input(f'{keys_len[i] }', step=1)
            angle[f'Angle (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',0.0,90.0,step=0.01,format="%.3f")
            direction_flow[f'Direction of flow {i+1}'] = st.selectbox(f'{keys_direction[i]}',['Uphill','Downhill'])

    for i in range(len(sections)):
        section[f'Section {i+1}'] = pipe(
        Dh = DH[f'Hydraulic diameter (in) {i+1}'] * 0.0254, 
        e =  rug_abs[f'Absolute roughness (in) {i+1}'] * 0.0254, 
        L =  length[f'Length of the pipe (m) {i+1}']  , 
        angle = angle[f'Angle (°) {i+1}'],
        direction = direction_flow[f'Direction of flow {i+1}']
        )

    st.subheader('Models used in your simulation')
    
    col1,col2,col3 = st.columns(3)
    with col1:
        vertical = st.selectbox('For the vertical pipe section',['Hagedorn (recommended)', 'Beggs_Brill',])
    with col2:
        horizontal = st.selectbox('For the horizontal pipe section',['Beggs_Brill (recommended)','Bendisken','Bhagwat'])
    with col3:
        inclined = st.selectbox('For the inclined pipe section',['Beggs_Brill','Bendisken','Bhagwat'])
    
    if vertical == 'Hagedorn (recommended)':
        vertical = 'Hagedorn'
    if horizontal == 'Beggs_Brill (recommended)':
        horizontal = 'Beggs_Brill'


    st.divider()


    st.subheader('Temperature profile ')
    adiabatic = st.checkbox("Adiabatic")

    if adiabatic == False:
        colums = st.columns(len(sections))
        temp = {}
        infinity_ti = {}
        infinity_tf = {}
        vertical_height = {}
        TEC = {}
        
        for i in range(len(sections)):
            infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = []
            infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = []
            vertical_height[f'Vertical height (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []
            


        keys_Ti = list(infinity_ti.keys())
        keys_Tf = list(infinity_tf.keys())
        keys_height = list(vertical_height.keys())
        keys_TEC = list(TEC.keys())

        for i in range(len(sections)):
            with colums[i]:
                st.header(keys_section[i])  
                temp[f'Section {i+1}'] = []
                infinity_ti[f'Initial infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Ti [i] }', step=0.01,format="%.3f")
                infinity_tf[f'Final infinite temperature (ºC) {i+1}'] = st.number_input(f'{keys_Tf [i] }', step=0.01,format="%.3f")
                vertical_height[f'Vertical height (m) {i+1}'] = st.number_input(f'{keys_height [i] }',1,1000000,step=1)
                TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',step=0.01, format="%.3f")

        for i in range(len(sections)):
            temp[f'Section {i+1}'] = Extern_Temperature(
                infinity_ti[f'Initial infinite temperature (ºC) {i+1}'],
                infinity_tf[f'Final infinite temperature (ºC) {i+1}'],
                vertical_height[f'Vertical height (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )  
    else:
        pass
    

    lines = []
    temps = []
    for i in range(len(sections)):
        lines.append(section[f'Section {i+1}'])
        if adiabatic == False:
            temps.append(temp[f'Section {i+1}'])
        else:
            temps = None

    st.divider()

    st.subheader('Which section is it located the pump')

    pump_line = st.selectbox('If a pump is necessary, which section is it located in?',section)

    for i in range(len(sections)):
        if pump_line == keys_section[i]:
            pump_line = i

       
    st.divider()


    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #1D2D50;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            white-space: nowrap;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
        """, unsafe_allow_html=True)

    if st.button("Simulation"):
        variables = []
        pressures = []
        temperatures = []
        HLS = []
        VSMS = []
        densities = []
        viscosities = []
        Zs  = []
        grav = []
        fric = []
        ace = []

           
        with st.container():
            with st.spinner('Simulating...'):
                try:
                    T,P,var,pump = simulation(fluid,lines,temps,pump_line,inclined,vertical,horizontal)
                    variables.append(var)
                    comp = np.arange(0,len(variables[0][0]),1)

                    for i in range(len(variables[0][0])):
                        pressures.append(variables[0][0][i])
                        temperatures.append(variables[0][1][i])
                        HLS.append(variables[0][2][i])
                        VSMS.append(variables[0][3][i])
                        densities.append(variables[0][6][i])
                        viscosities.append(variables[0][7][i])
                        Zs.append(variables[0][8][i])
                        grav.append(variables[0][9][i])
                        fric.append(variables[0][10][i])
                        #ace.append(variables[0][11][i])

                    bubble_points = []
                    for i in range(len(variables[0][0])):
                        copy_fluid.T = temperatures[i]
                        bubble_points.append(Pb_standing(copy_fluid)*0.0689475729)

                    custom_style = {
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 12,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 14,  # Tamanho do título do gráfico
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 12,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 12,  # Tamanho do texto dos ticks no eixo y
                        'lines.linewidth': 2,  # Espessura das linhas dos gráficos
                        'lines.markersize': 6,  # Tamanho dos marcadores
                        'legend.fontsize': 10,  # Tamanho da legenda
                        'legend.frameon': False,  # Remove a moldura ao redor da legenda
                        'legend.loc': 'best',  # Melhor posição automática para a legenda
                        'figure.figsize': (8, 6),  # Tamanho padrão da figura (polegadas)
                        'savefig.dpi': 600,  # Alta resolução para exportação (publicação)
                        'savefig.bbox': 'tight',  # Salva a imagem sem cortar parte do gráfico
                        }
                
                    plt.rcParams.update(custom_style)

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressure", "Temperature","HL","Vsm","Densities","Z"])

                    fig1, ax1 = plt.subplots()
                    ax1.plot(comp, bubble_points, lw =2 , ls='--',c='#F08080' ,label='Bubble pressure',zorder=2)
                    ax1.scatter(comp[-1],pressures[-1],c='#1D2D50',zorder=4,label='Separator')
                    ax1.scatter(comp[0],pressures[0],c='#87CEEB',zorder=5,label='Reservoir')
                    ax1.plot(comp,pressures,label=f'Pressure',c='k',zorder=3)
                    ax1.set_xlabel(f'Lenght pipe [$m$]')
                    ax1.set_ylabel(f'Pressure [$bar$]')
                    ax1.set_title(f'Fluid pressure across the pipe')
                    ax1.grid(alpha=0.5,zorder=1)
                    ax1.margins(x=0.1, y=0.1)
                    ax1.legend()
                    tab1.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    ax2.plot(comp,temperatures,label=f'Temperature',c='k',zorder=2)
                    ax2.scatter(comp[-1],temperatures[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax2.scatter(comp[0],temperatures[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax2.set_xlabel(f'Lenght pipe [$m$]')
                    ax2.set_ylabel(f'Temperature [$ºC$]')
                    ax2.set_title(f'Fluid temperature across the pipe')
                    ax2.grid(alpha=0.5,zorder=1)
                    ax2.margins(x=0.1, y=0.1)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    ax3.plot(comp,HLS,label=f'Fluid holdup',c='k',zorder=2)
                    ax3.scatter(comp[-1],HLS[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax3.scatter(comp[0],HLS[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax3.set_xlabel(f'Lenght pipe [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'Fluid Holdup across the pipe')
                    ax3.grid(alpha=0.5,zorder=1)
                    ax3.margins(x=0.1, y=0.1)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    ax4.plot(comp,VSMS,label=f'Fluid velocity',c='k',zorder=2)
                    ax4.scatter(comp[-1],VSMS[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax4.scatter(comp[0],VSMS[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax4.set_xlabel(f'Lenght pipe [$m$]')
                    ax4.set_ylabel(f'Fluid velocity [$m/s$]')
                    ax4.set_title(f'Fluid velocity across the pipe')
                    ax4.grid(alpha=0.5,zorder=1)
                    ax4.margins(x=0.1, y=0.1)
                    ax4.legend()
                    tab4.pyplot(fig4)

                    fig5, ax5 = plt.subplots()
                    ax5.plot(comp,densities,label=f'Fluid density',c='k',zorder=2)
                    ax5.scatter(comp[-1],densities[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax5.scatter(comp[0],densities[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax5.set_xlabel(f'Lenght pipe [$m$]')
                    ax5.set_ylabel(f'Density [Kg/m³]')
                    ax5.set_title(f'Fluid density across the pipe')
                    ax5.grid(alpha=0.5,zorder=1)
                    ax5.margins(x=0.1, y=0.1)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    ax7.plot(comp,Zs,label=f'Factor Z of the fluid',c='k',zorder=2)
                    ax7.scatter(comp[-1],Zs[-1],c='#1D2D50',zorder=3,label='Separator')
                    ax7.scatter(comp[0],Zs[0],c='#87CEEB',zorder=4,label='Reservoir')
                    ax7.set_xlabel(f'Lenght of the pipe [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Factor Z across the pipe')
                    ax7.grid(alpha=0.5,zorder=1)
                    ax7.margins(x=0.1, y=0.1)
                    ax7.legend()
                    tab7.pyplot(fig7) 
                    
                    st.divider()

                    
    
                    results1 = [P,T,pump]
                    colums = ['Values']
                    index1 = ["Pressure at separator (bar)", "Temperature at separator (ºC)","Pump increment (bar)"]
                    df_results_1 = pd.DataFrame(results1,index=index1,columns=colums)


                    grav_med = (sum(grav)/(len(variables[0][0])))/100000
                    fric_med = (sum(fric)/(len(variables[0][0])))/100000
                    total_med = sum((grav_med,fric_med))
                    results_2 = [grav_med,fric_med,total_med]
                    index_2 = ["Gravitational lose (bar/m)","Friccional lose (bar/m)","Total lose (bar/m)"]

                    df_results_2 = pd.DataFrame(results_2,index=index_2,columns=colums)

                    st.subheader('Tables with the main results')

                    col1,col2 = st.columns(2)
                    with col1:
                        st.dataframe(df_results_1.style.format("{:.3f}"))
                    with col2:
                        st.dataframe(df_results_2.style.format("{:.3f}"))

                    st.divider()

                except:
                    st.error("Error when simulating")

    pass



pg = st.navigation([
    st.Page(page1, title="How to use the program", ),
    st.Page(page2, title="Single mode simulation",),
    st.Page(page3,title='Simulation by section',),
])
pg.run()