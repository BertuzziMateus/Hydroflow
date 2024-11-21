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
 
    st.title("Bem vindo a PRESfil")
    st.divider()
    st.markdown(
        """
        <div style="text-align: justify;">

        Bem-vindo ao Simulador de Escoamento de Hidrocarbonetos! Eu fui desenvolvido para ajudar na análise de produção de sistemas de tubulação na indústria de petróleo e gás, permitindo que você explore diferentes condições de escoamento e entenda o comportamento do fluido ao longo do sistema. 
        
        Para começar, você precisa fornecer algumas informações essenciais. 
        
        Primeiramente, insira as propriedades do fluido, como pressão, temperatura, as gravidades especificas, grau API, relação gás-líquido (RGL) e percentual de água (BSW). Em seguida, configure os trechos de tubulação, especificando o diâmetro hidráulico, rugosidade, comprimento, ângulo de inclinação e orientação do fluxo. Caso necessário, você também pode definir um perfil térmico, optando por uma condição adiabática ou informando as temperaturas externas dos trechos.

        Além disso, você pode escolher o modelo de escoamento que melhor se adapta ao seu sistema, incluindo o método de fluxo drift-flux, o que me permite ajustar os cálculos para refletir a realidade das condições de campo. E se houver uma bomba no sistema, basta informar a sua localização para que eu simule o impacto do bombeamento no comportamento do fluido.

        Ao finalizar o preenchimento dos dados, eu vou gerar gráficos detalhados que mostram variáveis importantes como pressão, temperatura, densidade e velocidade ao longo do comprimento da tubulação. Esses gráficos vão ajudar você a analisar o escoamento de maneira visual e a identificar pontos críticos ou ajustes necessários no sistema.

        Comigo, você terá uma ferramenta robusta e flexível para simular o escoamento de hidrocarbonetos em condições específicas. Estou aqui para apoiar suas operações de produção e contribuir para uma análise mais precisa e confiável.
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.divider()
    st.subheader("Vamos ver um exemplo de como inserir os dados no problema proposto abaixo.")
    st.image('620 m.png')

    st.divider()
    
    P = st.number_input('Pressão do fluido (bar)',230.0,230.0,step=0.01,format="%.2f")
    T = st.number_input('Temperatura do fluido (°C)',80.0,80.0,step=0.1,format="%.2f")
    Dg = st.number_input('Dg',0.8436,0.8436,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.8346,0.8346,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('Grau API',0.0,50.0,step=0.1)
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',157.0,157.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.2,0.2,step=0.1,format="%.3f" )
    rate = st.number_input('Vazão requerida (m³/dia)',3200.0,3200.0,step=0.1,format="%.0f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C 
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 


    st.divider()
    st.subheader('Modelos desejados na simulação')
    
    col1,col2 = st.columns(2)
    with col1:
        op1 = st.checkbox("PRESfil 1",value=True)
    with col2:
        op2 = st.checkbox("PRESfil 2 (driftflux)",value=True)

    

    opcoes = []
    if op1 == True:
        opcoes.append('PRESfil 1')
    if op2 == True:
        opcoes.append('PRESfil 2')

    st.divider()
    st.subheader('Perfil de temperatura')
    adiabatico_condição = st.checkbox("Adiabático",value=False)
    st.divider()
    
    st.subheader('Prencha abaixo as informações sobre os trechos')
    trechos = st.slider('Quantidade de trechos',1,5,value=3)
    trechos = np.zeros(trechos)
    colunas = st.columns(len(trechos))




    trecho = {}
    DH = {}
    rug_abs = {}
    comprimento = {}
    angle = {}
    temp = {}
    T1 = {}
    T2 = {}
    Altura = {}
    TEC = {}
    orientação = {}



    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = []
        DH[f'Diâmetro hidráulico (in) {i+1}'] = []
        rug_abs[f'Rugosidade absoluta (in) {i+1}'] = []
        comprimento[f'Comprimento (m) {i+1}'] = []
        angle[f'Ângulo (°) {i+1}'] = []
        orientação[f'Orientação do fluxo {i+1}'] = []

        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = []
            T1[f'Temperatura externa inicial (ºC) {i+1}'] = []
            T2[f'Temperatura externa final (ºC) {i+1}'] = []
            Altura[f'Altura (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []




    keys_trecho = list(trecho.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_compr = list(comprimento.keys())
    keys_ang = list(angle.keys())
    keys_T1 = list(T1.keys())
    keys_T2 = list(T2.keys())
    keys_Altura = list(Altura.keys())
    keys_TEC = list(TEC.keys())
    keys_ori = list(orientação.keys())



    for i in range(len(trechos)):
        with colunas[i]:
            st.header(keys_trecho[i])
            DH[f'Diâmetro hidráulico (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',4.0,4.0,step=0.01,)
            rug_abs[f'Rugosidade absoluta (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0005,0.0005,step=0.01,format="%.4f")
            if i == 0:
                comprimento[f'Comprimento (m) {i+1}'] = st.number_input(f'{keys_compr[i] }',580.0,580.0, step=0.01)
                angle[f'Ângulo (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',15.0,15.0,step=0.01)
                orientação[f'Orientação do trecho {i+1}'] = st.selectbox(f'{keys_ori[i]}',['Ascendente'])
                if adiabatico_condição == False:
                    T1[f'Temperatura externa inicial (ºC) {i+1}'] = st.number_input(f'{keys_T1 [i] }',4.0 , 4.0,step=0.01)
                    T2[f'Temperatura externa final (ºC) {i+1}'] = st.number_input(f'{keys_T2 [i] }',80.0,80.0, step=0.01)
                    Altura[f'Altura (m) {i+1}'] = st.number_input(f'{keys_Altura [i] }',150.0,150.0,step=0.01)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',2.0,2.0,step=0.01)
            if i == 1:
                comprimento[f'Comprimento (m) {i+1}'] = st.number_input(f'{keys_compr[i] }',864.0,864.0, step=0.01)
                angle[f'Ângulo (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',10.0,10.0,step=0.01)
                orientação[f'Orientação do trecho {i+1}'] = st.selectbox(f'{keys_ori[i]}',['Ascendente'])
                if adiabatico_condição == False:
                    T1[f'Temperatura externa inicial (ºC) {i+1}'] = st.number_input(f'{keys_T1 [i] }',22.0 , 22.0,step=0.01)
                    T2[f'Temperatura externa final (ºC) {i+1}'] = st.number_input(f'{keys_T2 [i] }',4.0,4.0, step=0.01)
                    Altura[f'Altura (m) {i+1}'] = st.number_input(f'{keys_Altura [i] }',1650.0,1650.0,step=0.01)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',1.0,1.0,step=0.01)
            if i == 2:
                comprimento[f'Comprimento (m) {i+1}'] = st.number_input(f'{keys_compr[i] }', 1500.0,1500.0,step=0.01)
                angle[f'Ângulo (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',90.0,90.0,step=0.01)
                orientação[f'Orientação do trecho {i+1}'] = st.selectbox(f'{keys_ori[i]}',['Ascendente'])
                if adiabatico_condição == False:
                    T1[f'Temperatura externa inicial (ºC) {i+1}'] = st.number_input(f'{keys_T1 [i] }',22.0 , 22.0,step=0.01)
                    T2[f'Temperatura externa final (ºC) {i+1}'] = st.number_input(f'{keys_T2 [i] }',5.5,5.5, step=0.01)
                    Altura[f'Altura (m) {i+1}'] = st.number_input(f'{keys_Altura [i] }',1500.0,1500.0,step=0.01)
                    TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',1.0,1.0,step=0.01)



    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = pipe(
            Dh = DH[f'Diâmetro hidráulico (in) {i+1}'] * 0.0254, 
            e =  rug_abs[f'Rugosidade absoluta (in) {i+1}'] * 0.0254, 
            L =  comprimento[f'Comprimento (m) {i+1}']  , 
            angle = angle[f'Ângulo (°) {i+1}'],
            direction = orientação[f'Orientação do trecho {i+1}']
            )
        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = Extern_Temperature(
                T1[f'Temperatura externa inicial (ºC) {i+1}'],
                T2[f'Temperatura externa final (ºC) {i+1}'],
                Altura[f'Altura (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )
    

    lines = []
    temps = []
    for i in range(len(trechos)):
        lines.append(trecho[f'Trecho {i+1}'])
        if adiabatico_condição == False:
            temps.append(temp[f'Trecho {i+1}'])
        else:
            temps = None

    pump_line = st.selectbox('Caso necessário em qual trecho está localizada a bomba?',keys_trecho[1])

    for i in range(len(trechos)):
        if pump_line == keys_trecho[i]:
            pump_line = i
       
    st.divider()

    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #4CAF50;
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

    if st.button("Simular"):
        variables = [] 
        pressoes = []
        temperaturas = []
        HLS = []
        VSMS = []
        Densidades = []
        Viscosidades = []
        Zs  = []
        grav = []
        fric = []
        ace = []


        for i in range(len(opcoes)):
            variables.append([])
            pressoes.append([])
            temperaturas.append([])
            HLS.append([])
            VSMS.append([])
            Densidades.append([])
            Viscosidades.append([])
            Zs.append([])
            grav.append([])
            fric.append([])
            ace.append([])
        
        with st.container():
            with st.spinner('Simulando...'):
                try:
                    for i in range(len(opcoes)):
                        if opcoes[i] == 'PRESfil 1':
                            T,P,var,pump = simulation_1(fluid,lines,temps,pump_line)
                            variables[i].append([T,P,var,pump])
                        
                        elif opcoes[i] == 'PRESfil 2':
                            T,P,var,pump = simulation_2(fluid,lines,temps,pump_line)
                            variables[i].append([T,P,var,pump])
                        

                    
                    comp = np.arange(0,len(variables[i][0][2][0]),1)

                    for i in range(len(variables)):
                        pressoes[i].append(variables[i][0][2][0])
                        temperaturas[i].append(variables[i][0][2][1])
                        HLS[i].append(variables[i][0][2][2])
                        VSMS[i].append(variables[i][0][2][3])
                        Densidades[i].append(variables[i][0][2][6])
                        Viscosidades[i].append(variables[i][0][2][7])
                        Zs[i].append(variables[i][0][2][8])
                        grav[i].append(variables[i][0][2][9])
                        fric[i].append(variables[i][0][2][10])
                        ace[i].append(variables[i][0][2][11])


                    custom_style = {
                        'font.family': 'serif',  # Fonte tradicional para trabalhos acadêmicos
                        'font.serif': ['Times New Roman'],  # Escolha comum para trabalhos acadêmicos
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 10,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 12,  # Tamanho do título do gráfico
                        'axes.titleweight': 'bold',  # Título em negrito para destaque
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 10,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 10,  # Tamanho do texto dos ticks no eixo y
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

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressão", "Temperatura","HL","Vsm","Densidade","Z"])
                    
                    fig1, ax1 = plt.subplots()
                    for i in range(len(pressoes)):
                        ax1.plot(comp,pressoes[i][0][::-1],label=f'Pressão do fluido com o modelo {opcoes[i]}')
                    ax1.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax1.set_ylabel(f'Pressão [$bar$]')
                    ax1.set_title(f'Pressão x Comprimento')
                    ax1.grid(alpha=0.5)
                    ax1.legend()
                    tab1.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    for i in range(len(temperaturas)):
                        ax2.plot(comp,temperaturas[i][0][::-1],label=f'Temperatura do fluido com o modelo {opcoes[i]}')
                    ax2.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax2.set_ylabel(f'Temperatura [$ºC$]')
                    ax2.set_title(f'Temperatura x Comprimento')
                    ax2.grid(alpha=0.5)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    for i in range(len(HLS)):
                        ax3.plot(comp,HLS[i][0][::-1],label=f'HL do fluido com o modelo {opcoes[i]}')
                    ax3.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'HL x Comprimento')
                    ax3.grid(alpha=0.5)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    for i in range(len(VSMS)):
                        ax4.plot(comp,VSMS[i][0][::-1],label=f'Velocidade da mistura com o modelo {opcoes[i]}')
                    ax4.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax4.set_ylabel(f'Velocidade da mistura [$m/s$]')
                    ax4.set_title(f'Velocidade x Comprimento')
                    ax4.grid(alpha=0.5)
                    ax4.legend()

                    tab4.pyplot(fig4)

                    fig5, ax5 = plt.subplots()
                    for i in range(len(Densidades)):
                        ax5.plot(comp,Densidades[i][0][::-1],label=f'Densidade do fluido com modelo {opcoes[i]}')
                    ax5.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax5.set_ylabel(f'Densidade [Kg/m³]')
                    ax5.set_title(f'Densidade x Comprimento')
                    ax5.grid(alpha=0.5)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    for i in range(len(Zs)):
                        ax7.plot(comp,Zs[i][0][::-1],label=f'Z do fluido com modelo {opcoes[i]}')
                    ax7.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Fator Z x Comprimento')
                    ax7.grid(alpha=0.5)
                    ax7.legend()
                    tab7.pyplot(fig7)

                    resultados_1= []
                    resultados_2= []
    
                    for i in range(len(opcoes)):
                        P = round(pressoes[i][0][::-1][0],2)
                        T = round(temperaturas[i][0][::-1][0],2)
                        Bomba = round(variables[i][0][3],2)
                        grav_med = (sum(grav[i][0])/(len(variables[0][0][2][0])))/100000
                        fric_med = (sum(fric[i][0])/(len(variables[0][0][2][0])))/100000
                        ac_med = (sum(ace[i][0])/(len(variables[0][0][2][0])))/100000
                        total_med = sum((grav_med,fric_med,ac_med))
                        resultados_1.append([P,T,Bomba])
                        resultados_2.append([grav_med,fric_med,ac_med,total_med])
                    colunas_1 = ["Pressão (bar)", "Temperatura (ºC)","Pressão necessária na bomba (bar)"]
                    colunas_2 = ["Gravitacional (bar/m)","Friccional (bar/m)","Aceleração (bar/m)","Total (bar/m)"]
                    indices_1 = []
                    indices_2 = []
                    for i in range(len(opcoes)):
                        indices_1.append(f"{opcoes[i]}")
                        indices_2.append(f"{opcoes[i]}")

                    df_resultados_1 = pd.DataFrame(resultados_1,columns=colunas_1,index=indices_1)
                    df_resultados_2 = pd.DataFrame(resultados_2,columns=colunas_2,index=indices_2)
                    st.subheader("Tabela de resultados principais na chegada do fluido ao separador")
                    st.dataframe(df_resultados_1.style.format("{:.2f}"))
                    st.subheader("Tabela da perda de carga médio ao longo do escoamento")
                    st.dataframe(df_resultados_2.style.format("{:.4f}"))


                except:
                    st.error("Erro ao simular")





    pass

def page2():
    
    st.title('Preencha abaixo as informações sobre o fluido a ser modelado')


    P = st.number_input('Pressão do fluido (bar)',0.00,700.00,step=0.01,format="%.2f")
    T = st.number_input('Temperatura do fluido (°C)',0.0,150.0,step=0.1,format="%.2f")
    Dg = st.number_input('Dg',0.0,1.0,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.0,1.0,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('Grau API',0.0,50.0,step=0.1)
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',1.0,500.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.0,1.0,step=0.1,format="%.3f" )
    rate = st.number_input('Vazão requerida (m³/dia)',0.0,10000.0,step=0.1,format="%.2f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C 
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 


    st.divider()
    st.subheader('Modelos desejados na simulação')
    
    col1,col2 = st.columns(2)
    with col1:
        Homo = st.checkbox("Homogêneo")
        BB = st.checkbox("Beggs e Brill")
        bhagwat =st.checkbox("Bhagwat")
    with col2:
        HB = st.checkbox("Hagedorn")
        ben = st.checkbox("Bendisken")
    

    opcoes = []
    if Homo == True:
        opcoes.append('Homogeneous')
    if BB == True:
        opcoes.append('Beggs_Brill')
    if HB == True:
        opcoes.append('Hagedorn')
    if ben == True:
        opcoes.append('Bendisken')
    if bhagwat == True:
        opcoes.append("Bhagwat")

    st.divider()
    st.subheader('Perfil de temperatura')
    adiabatico_condição = st.checkbox("Adiabático")
    st.divider()
    
    st.subheader('Prencha abaixo as informações sobre os trechos')
    trechos = st.slider('Quantidade de trechos',1,5)
    trechos = np.zeros(trechos)
    colunas = st.columns(len(trechos))




    trecho = {}
    DH = {}
    rug_abs = {}
    comprimento = {}
    angle = {}
    temp = {}
    T1 = {}
    T2 = {}
    Altura = {}
    TEC = {}
    orientação = {}



    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = []
        DH[f'Diâmetro hidráulico (in) {i+1}'] = []
        rug_abs[f'Rugosidade absoluta (in) {i+1}'] = []
        comprimento[f'Comprimento (m) {i+1}'] = []
        angle[f'Ângulo (°) {i+1}'] = []
        orientação[f'Orientação do fluxo {i+1}'] = []

        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = []
            T1[f'Temperatura externa inicial (ºC) {i+1}'] = []
            T2[f'Temperatura externa final (ºC) {i+1}'] = []
            Altura[f'Altura (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []




    keys_trecho = list(trecho.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_compr = list(comprimento.keys())
    keys_ang = list(angle.keys())
    keys_T1 = list(T1.keys())
    keys_T2 = list(T2.keys())
    keys_Altura = list(Altura.keys())
    keys_TEC = list(TEC.keys())
    keys_ori = list(orientação.keys())



    for i in range(len(trechos)):
        with colunas[i]:
            st.header(keys_trecho[i])
            DH[f'Diâmetro hidráulico (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',0.000000000001,10.0,step=0.01,)
            rug_abs[f'Rugosidade absoluta (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0000001,10.0,step=0.01,format="%.4f")
            comprimento[f'Comprimento (m) {i+1}'] = st.number_input(f'{keys_compr[i] }', step=0.01)
            angle[f'Ângulo (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',0.0,90.0,step=0.01)
            orientação[f'Orientação do trecho {i+1}'] = st.selectbox(f'{keys_ori[i]}',['Ascendente','Descendente'])
            if adiabatico_condição == False:
                T1[f'Temperatura externa inicial (ºC) {i+1}'] = st.number_input(f'{keys_T1 [i] }', 1.0 , 150.0,step=0.01)
                T2[f'Temperatura externa final (ºC) {i+1}'] = st.number_input(f'{keys_T2 [i] }', step=0.01)
                Altura[f'Altura (m) {i+1}'] = st.number_input(f'{keys_Altura [i] }',1.0,1000000.0,step=0.01)
                TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',step=0.01)


    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = pipe(
            Dh = DH[f'Diâmetro hidráulico (in) {i+1}'] * 0.0254, 
            e =  rug_abs[f'Rugosidade absoluta (in) {i+1}'] * 0.0254, 
            L =  comprimento[f'Comprimento (m) {i+1}']  , 
            angle = angle[f'Ângulo (°) {i+1}'],
            direction = orientação[f'Orientação do trecho {i+1}']
            )
        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = Extern_Temperature(
                T1[f'Temperatura externa inicial (ºC) {i+1}'],
                T2[f'Temperatura externa final (ºC) {i+1}'],
                Altura[f'Altura (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )
    

    lines = []
    temps = []
    for i in range(len(trechos)):
        lines.append(trecho[f'Trecho {i+1}'])
        if adiabatico_condição == False:
            temps.append(temp[f'Trecho {i+1}'])
        else:
            temps = None

    pump_line = st.selectbox('Caso necessário em qual trecho está localizada a bomba?',trecho)

    for i in range(len(trechos)):
        if pump_line == keys_trecho[i]:
            pump_line = i
       
    st.divider()

    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #4CAF50;
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

    if st.button("Simular"):
        variables = [] 
        pressoes = []
        temperaturas = []
        HLS = []
        VSMS = []
        Densidades = []
        Viscosidades = []
        Zs  = []
        grav = []
        fric = []
        ace = []

        for i in range(len(opcoes)):
            variables.append([])
            pressoes.append([])
            temperaturas.append([])
            HLS.append([])
            VSMS.append([])
            Densidades.append([])
            Viscosidades.append([])
            Zs.append([])
            grav.append([])
            fric.append([])
            ace.append([])
        
        with st.container():
            with st.spinner('Simulando...'):
                try:
                    for i in range(len(opcoes)):
                        T,P,var,pump = single_simulation(fluid,lines,temps,pump_line,opcoes[i])
                        variables[i].append([T,P,var,pump])

                    comp = np.arange(0,len(variables[0][0][2][0]),1)
    
                    for i in range(len(variables)):
                        pressoes[i].append(variables[i][0][2][0])
                        temperaturas[i].append(variables[i][0][2][1])
                        HLS[i].append(variables[i][0][2][2])
                        VSMS[i].append(variables[i][0][2][3])
                        Densidades[i].append(variables[i][0][2][6])
                        Viscosidades[i].append(variables[i][0][2][7])
                        Zs[i].append(variables[i][0][2][8])
                        grav[i].append(variables[i][0][2][9])
                        fric[i].append(variables[i][0][2][10])
                        ace[i].append(variables[i][0][2][11])
                        



                    custom_style = {
                        'font.family': 'serif',  # Fonte tradicional para trabalhos acadêmicos
                        'font.serif': ['Times New Roman'],  # Escolha comum para trabalhos acadêmicos
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 10,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 12,  # Tamanho do título do gráfico
                        'axes.titleweight': 'bold',  # Título em negrito para destaque
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 10,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 10,  # Tamanho do texto dos ticks no eixo y
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

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressão", "Temperatura","HL","Vsm","Densidade","Z"])
                    

                    fig1, ax1 = plt.subplots()
                    for i in range(len(pressoes)):
                        ax1.plot(comp,pressoes[i][0][::-1],label=f'Pressão do fluido com o modelo {opcoes[i]}')
                    ax1.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax1.set_ylabel(f'Pressão [$bar$]')
                    ax1.set_title(f'Pressão x Comprimento')
                    ax1.grid(alpha=0.5)
                    ax1.legend()
                    tab1.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    for i in range(len(temperaturas)):
                        ax2.plot(comp,temperaturas[i][0][::-1],label=f'Temperatura do fluido com o modelo {opcoes[i]}')
                    ax2.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax2.set_ylabel(f'Temperatura [$ºC$]')
                    ax2.set_title(f'Temperatura x Comprimento')
                    ax2.grid(alpha=0.5)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    for i in range(len(HLS)):
                        ax3.plot(comp,HLS[i][0][::-1],label=f'HL do fluido com o modelo {opcoes[i]}')
                    ax3.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'HL x Comprimento')
                    ax3.grid(alpha=0.5)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    for i in range(len(VSMS)):
                        ax4.plot(comp,VSMS[i][0][::-1],label=f'Velocidade da mistura com o modelo {opcoes[i]}')
                    ax4.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax4.set_ylabel(f'Velocidade da mistura [$m/s$]')
                    ax4.set_title(f'Velocidade x Comprimento')
                    ax4.grid(alpha=0.5)
                    ax4.legend()

                    tab4.pyplot(fig4)

                    fig5, ax5 = plt.subplots()
                    for i in range(len(Densidades)):
                        ax5.plot(comp,Densidades[i][0][::-1],label=f'Densidade do fluido com modelo {opcoes[i]}')
                    ax5.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax5.set_ylabel(f'Densidade [Kg/m³]')
                    ax5.set_title(f'Densidade x Comprimento')
                    ax5.grid(alpha=0.5)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    for i in range(len(Zs)):
                        ax7.plot(comp,Zs[i][0][::-1],label=f'Z do fluido com modelo {opcoes[i]}')
                    ax7.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Fator Z x Comprimento')
                    ax7.grid(alpha=0.5)
                    ax7.legend()
                    tab7.pyplot(fig7)

                    resultados_1= []
                    resultados_2= []
    
                    for i in range(len(opcoes)):
                        P = round(pressoes[i][0][::-1][0],2)
                        T = round(temperaturas[i][0][::-1][0],2)
                        Bomba = round(variables[i][0][3],2)
                        grav_med = (sum(grav[i][0])/(len(variables[0][0][2][0])))/100000
                        fric_med = (sum(fric[i][0])/(len(variables[0][0][2][0])))/100000
                        ac_med = (sum(ace[i][0])/(len(variables[0][0][2][0])))/100000
                        total_med = sum((grav_med,fric_med,ac_med))
                        resultados_1.append([P,T,Bomba])
                        resultados_2.append([grav_med,fric_med,ac_med,total_med])
                    colunas_1 = ["Pressão (bar)", "Temperatura (ºC)","Pressão necessária na bomba (bar)"]
                    colunas_2 = ["Gravitacional (bar/m)","Friccional (bar/m)","Aceleração (bar/m)","Total (bar/m)"]
                    indices_1 = []
                    indices_2 = []
                    for i in range(len(opcoes)):
                        indices_1.append(f"{opcoes[i]}")
                        indices_2.append(f"{opcoes[i]}")

                    df_resultados_1 = pd.DataFrame(resultados_1,columns=colunas_1,index=indices_1)
                    df_resultados_2 = pd.DataFrame(resultados_2,columns=colunas_2,index=indices_2)
                    st.subheader("Tabela de resultados principais na chegada do fluido ao separador")
                    st.dataframe(df_resultados_1.style.format("{:.2f}"))
                    st.subheader("Tabela da perda de carga médio ao longo do escoamento")
                    st.dataframe(df_resultados_2.style.format("{:.4f}"))

                except:
                    st.error("Erro ao simular")

    pass

def page3():
    
    st.title('Preencha abaixo as informações sobre o fluido a ser modelado')


    P = st.number_input('Pressão do fluido (bar)',0.00,700.00,step=0.01,format="%.2f")
    T = st.number_input('Temperatura do fluido (°C)',0.0,150.0,step=0.1,format="%.2f")
    Dg = st.number_input('Dg',0.0,1.0,step=0.1,format="%.3f")
    Do = st.number_input('Do',0.0,1.0,step=0.1,format="%.3f")
    if Do == 0.0:
        API = st.number_input('Grau API',0.0,50.0,step=0.1)
    elif Do != 0 :
        API = 0 
    RGL = st.number_input('RGL (sm³/sm³)',1.0,500.0,step=0.1,format="%.3f")
    BSW = st.number_input('BSW',0.0,1.0,step=0.1,format="%.3f" )
    rate = st.number_input('Vazão requerida (m³/dia)',0.0,10000.0,step=0.1,format="%.0f")


    fluid = Fluid_model(
        P = P, #bar  
        T = T ,#C 
        Dg = Dg,
        Do = Do,
        API = API,
        RGL = RGL, # sM^3/sM^3 
        BSW = BSW, # %
        rate = rate/86400 # m^3 /s
        ) 


    st.divider()
    st.subheader('Modelos desejados na simulação')
    
    col1,col2 = st.columns(2)
    with col1:
        op1 = st.checkbox("PRESfil 1")
    with col2:
        op2 = st.checkbox("PRESfil 2 (driftflux)")

    

    opcoes = []
    if op1 == True:
        opcoes.append('PRESfil 1')
    if op2 == True:
        opcoes.append('PRESfil 2')

    st.divider()
    st.subheader('Perfil de temperatura')
    adiabatico_condição = st.checkbox("Adiabático")
    st.divider()
    
    st.subheader('Prencha abaixo as informações sobre os trechos')
    trechos = st.slider('Quantidade de trechos',1,5)
    trechos = np.zeros(trechos)
    colunas = st.columns(len(trechos))




    trecho = {}
    DH = {}
    rug_abs = {}
    comprimento = {}
    angle = {}
    temp = {}
    T1 = {}
    T2 = {}
    Altura = {}
    TEC = {}
    orientação = {}



    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = []
        DH[f'Diâmetro hidráulico (in) {i+1}'] = []
        rug_abs[f'Rugosidade absoluta (in) {i+1}'] = []
        comprimento[f'Comprimento (m) {i+1}'] = []
        angle[f'Ângulo (°) {i+1}'] = []
        orientação[f'Orientação do fluxo {i+1}'] = []

        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = []
            T1[f'Temperatura externa inicial (ºC) {i+1}'] = []
            T2[f'Temperatura externa final (ºC) {i+1}'] = []
            Altura[f'Altura (m) {i+1}'] = []
            TEC[f'TEC (W/M*ºC) {i+1}'] = []




    keys_trecho = list(trecho.keys())
    keys_DH = list(DH.keys())
    keys_rug = list(rug_abs.keys())
    keys_compr = list(comprimento.keys())
    keys_ang = list(angle.keys())
    keys_T1 = list(T1.keys())
    keys_T2 = list(T2.keys())
    keys_Altura = list(Altura.keys())
    keys_TEC = list(TEC.keys())
    keys_ori = list(orientação.keys())



    for i in range(len(trechos)):
        with colunas[i]:
            st.header(keys_trecho[i])
            DH[f'Diâmetro hidráulico (in) {i+1}']  = st.number_input(f'{keys_DH[i] }',0.000000000001,10.0,step=0.01,)
            rug_abs[f'Rugosidade absoluta (in) {i+1}'] = st.number_input(f'{keys_rug[i] }',0.0000001,10.0,step=0.01,format="%.4f")
            comprimento[f'Comprimento (m) {i+1}'] = st.number_input(f'{keys_compr[i] }', step=0.01)
            angle[f'Ângulo (°) {i+1}'] = st.number_input(f'{keys_ang[i] }',0.0,90.0,step=0.01)
            orientação[f'Orientação do trecho {i+1}'] = st.selectbox(f'{keys_ori[i]}',['Ascendente','Descendente'])
            if adiabatico_condição == False:
                T1[f'Temperatura externa inicial (ºC) {i+1}'] = st.number_input(f'{keys_T1 [i] }', 1.0 , 150.0,step=0.01)
                T2[f'Temperatura externa final (ºC) {i+1}'] = st.number_input(f'{keys_T2 [i] }', step=0.01)
                Altura[f'Altura (m) {i+1}'] = st.number_input(f'{keys_Altura [i] }',1.0,1000000.0,step=0.01)
                TEC[f'TEC (W/M*ºC) {i+1}'] = st.number_input(f'{keys_TEC [i] }',step=0.01)


    for i in range(len(trechos)):
        trecho[f'Trecho {i+1}'] = pipe(
            Dh = DH[f'Diâmetro hidráulico (in) {i+1}'] * 0.0254, 
            e =  rug_abs[f'Rugosidade absoluta (in) {i+1}'] * 0.0254, 
            L =  comprimento[f'Comprimento (m) {i+1}']  , 
            angle = angle[f'Ângulo (°) {i+1}'],
            direction = orientação[f'Orientação do trecho {i+1}']
            )
        if adiabatico_condição == False:
            temp[f'Trecho {i+1}'] = Extern_Temperature(
                T1[f'Temperatura externa inicial (ºC) {i+1}'],
                T2[f'Temperatura externa final (ºC) {i+1}'],
                Altura[f'Altura (m) {i+1}'],
                TEC[f'TEC (W/M*ºC) {i+1}']
                )
    

    lines = []
    temps = []
    for i in range(len(trechos)):
        lines.append(trecho[f'Trecho {i+1}'])
        if adiabatico_condição == False:
            temps.append(temp[f'Trecho {i+1}'])
        else:
            temps = None

    pump_line = st.selectbox('Caso necessário em qual trecho está localizada a bomba?',trecho)

    for i in range(len(trechos)):
        if pump_line == keys_trecho[i]:
            pump_line = i

       
    st.divider()

    st.markdown("""
        <style>
        .stButton > button {
            font-size: 11px !important;
            padding: 10px 327px;
            background-color: #4CAF50;
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

    if st.button("Simular"):
        variables = [] 
        pressoes = []
        temperaturas = []
        HLS = []
        VSMS = []
        Densidades = []
        Viscosidades = []
        Zs  = []
        grav = []
        fric = []
        ace = []


        for i in range(len(opcoes)):
            variables.append([])
            pressoes.append([])
            temperaturas.append([])
            HLS.append([])
            VSMS.append([])
            Densidades.append([])
            Viscosidades.append([])
            Zs.append([])
            grav.append([])
            fric.append([])
            ace.append([])
            
        with st.container():
            with st.spinner('Simulando...'):
                try:
                    for i in range(len(opcoes)):
                        if opcoes[i] == 'PRESfil 1':
                            T,P,var,pump = simulation_1(fluid,lines,temps,pump_line)
                            variables[i].append([T,P,var,pump])
                        
                        elif opcoes[i] == 'PRESfil 2':
                            T,P,var,pump = simulation_2(fluid,lines,temps,pump_line)
                            variables[i].append([T,P,var,pump])

                    comp = np.arange(0,len(variables[i][0][2][0]),1)/10

    
                    for i in range(len(variables)):
                        pressoes[i].append(variables[i][0][2][0])
                        temperaturas[i].append(variables[i][0][2][1])
                        HLS[i].append(variables[i][0][2][2])
                        VSMS[i].append(variables[i][0][2][3])
                        Densidades[i].append(variables[i][0][2][6])
                        Viscosidades[i].append(variables[i][0][2][7])
                        Zs[i].append(variables[i][0][2][8])
                        grav[i].append(variables[i][0][2][9])
                        fric[i].append(variables[i][0][2][10])
                        ace[i].append(variables[i][0][2][11])

                    custom_style = {
                        'font.family': 'serif',  # Fonte tradicional para trabalhos acadêmicos
                        'font.serif': ['Times New Roman'],  # Escolha comum para trabalhos acadêmicos
                        'font.size': 12,  # Tamanho adequado para leitura de gráficos
                        'axes.labelsize': 10,  # Tamanho dos rótulos dos eixos
                        'axes.titlesize': 12,  # Tamanho do título do gráfico
                        'axes.titleweight': 'bold',  # Título em negrito para destaque
                        'axes.linewidth': 1.5,  # Espessura das bordas dos gráficos
                        'xtick.labelsize': 10,  # Tamanho do texto dos ticks no eixo x
                        'ytick.labelsize': 10,  # Tamanho do texto dos ticks no eixo y
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

                    tab1,tab2,tab3,tab4,tab5,tab7 = st.tabs(["Pressão", "Temperatura","HL","Vsm","Densidade","Z"])
     
                    fig1, ax1 = plt.subplots()
                    for i in range(len(pressoes)):
                        ax1.plot(comp,pressoes[i][0][::-1],label=f'Pressão do fluido com o modelo {opcoes[i]}')
                    ax1.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax1.set_ylabel(f'Pressão [$bar$]')
                    ax1.set_title(f'Pressão x Comprimento')
                    ax1.grid(alpha=0.5)
                    ax1.legend()
                    tab1.pyplot(fig1)

                    fig2, ax2 = plt.subplots()
                    for i in range(len(temperaturas)):
                        ax2.plot(comp,temperaturas[i][0][::-1],label=f'Temperatura do fluido com o modelo {opcoes[i]}')
                    ax2.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax2.set_ylabel(f'Temperatura [$ºC$]')
                    ax2.set_title(f'Temperatura x Comprimento')
                    ax2.grid(alpha=0.5)
                    ax2.legend()
                    tab2.pyplot(fig2)

                    fig3, ax3 = plt.subplots()
                    for i in range(len(HLS)):
                        ax3.plot(comp,HLS[i][0][::-1],label=f'HL do fluido com o modelo {opcoes[i]}')
                    ax3.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax3.set_ylabel(f'Hl')
                    ax3.set_title(f'HL x Comprimento')
                    ax3.grid(alpha=0.5)
                    ax3.legend()
                    tab3.pyplot(fig3)

                    fig4, ax4 = plt.subplots()
                    for i in range(len(VSMS)):
                        ax4.plot(comp,VSMS[i][0][::-1],label=f'Velocidade da mistura com o modelo {opcoes[i]}')
                    ax4.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax4.set_ylabel(f'Velocidade da mistura [$m/s$]')
                    ax4.set_title(f'Velocidade x Comprimento')
                    ax4.grid(alpha=0.5)
                    ax4.legend()
                    tab4.pyplot(fig4)

                    fig5, ax5 = plt.subplots()
                    for i in range(len(Densidades)):
                        ax5.plot(comp,Densidades[i][0][::-1],label=f'Densidade do fluido com modelo {opcoes[i]}')
                    ax5.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax5.set_ylabel(f'Densidade [Kg/m³]')
                    ax5.set_title(f'Densidade x Comprimento')
                    ax5.grid(alpha=0.5)
                    ax5.legend()
                    tab5.pyplot(fig5)

                    fig7, ax7 = plt.subplots()
                    for i in range(len(Zs)):
                        ax7.plot(comp,Zs[i][0][::-1],label=f'Z do fluido com modelo {opcoes[i]}')
                    ax7.set_xlabel(f'Comprimento da tubulação [$m$]')
                    ax7.set_ylabel(f'Z')
                    ax7.set_title(f'Fator Z x Comprimento')
                    ax7.grid(alpha=0.5)
                    ax7.legend()
                    tab7.pyplot(fig7) 
                    
                    resultados_1= []
                    resultados_2= []
    
                    for i in range(len(opcoes)):
                        P = round(pressoes[i][0][::-1][0],2)
                        T = round(temperaturas[i][0][::-1][0],2)
                        Bomba = round(variables[i][0][3],2)
                        grav_med = (sum(grav[i][0])/(len(variables[0][0][2][0])))/100000
                        fric_med = (sum(fric[i][0])/(len(variables[0][0][2][0])))/100000
                        ac_med = (sum(ace[i][0])/(len(variables[0][0][2][0])))/100000
                        total_med = sum((grav_med,fric_med,ac_med))
                        resultados_1.append([P,T,Bomba])
                        resultados_2.append([grav_med,fric_med,ac_med,total_med])
                    colunas_1 = ["Pressão (bar)", "Temperatura (ºC)","Pressão necessária na bomba (bar)"]
                    colunas_2 = ["Gravitacional (bar/m)","Friccional (bar/m)","Aceleração (bar/m)","Total (bar/m)"]
                    indices_1 = []
                    indices_2 = []
                    for i in range(len(opcoes)):
                        indices_1.append(f"{opcoes[i]}")
                        indices_2.append(f"{opcoes[i]}")

                    df_resultados_1 = pd.DataFrame(resultados_1,columns=colunas_1,index=indices_1)
                    df_resultados_2 = pd.DataFrame(resultados_2,columns=colunas_2,index=indices_2)
                    st.subheader("Tabela de resultados principais na chegada do fluido ao separador")
                    st.dataframe(df_resultados_1.style.format("{:.2f}"))
                    st.subheader("Tabela da perda de carga médio ao longo do escoamento")
                    st.dataframe(df_resultados_2.style.format("{:.4f}"))


                except:
                    st.error("Erro ao simular")

    pass


pg = st.navigation([
    st.Page(page1, title="Como usar o programa", icon=":material/favorite:"),
    st.Page(page2, title="Simulação de um modelo", icon=":material/favorite:"),
    st.Page(page3,title='Simulação PRESFil',icon=":material/favorite:"),
])

pg.run()
