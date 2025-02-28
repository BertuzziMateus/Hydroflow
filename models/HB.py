import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import UnivariateSpline

g = 9.81


def liquid_velocity_number( Flow_info ) -> float:
    return ( (Flow_info.vsl)*( ( (Flow_info.liquid_rho) / (g *Flow_info.gas_liquid_sigma) )**(1/4)))

def gas_velocity_number( Flow_info) -> float:
    return ( (Flow_info.vsg)*( ( (Flow_info.liquid_rho) / (g *Flow_info.gas_liquid_sigma) )**(1/4)))

def diameter_tubing_number( Flow_info , tubing ) -> float:
    return ( (tubing.Dh)*( ( (Flow_info.liquid_rho*g) / (Flow_info.gas_liquid_sigma) )**(1/2)))

def liquid_viscosity_number( Flow_info  ) -> float:
    return ( (Flow_info.liquid_viscosity)*( ( (g) / ((Flow_info.liquid_rho)*(Flow_info.gas_liquid_sigma**3)))**(1/4)))

def psi( Flow_info, tubing  ) -> float:
    x = (gas_velocity_number(Flow_info)*liquid_viscosity_number(Flow_info)**0.380) / (diameter_tubing_number(Flow_info,tubing))**2.14
    if x < 0.012:
        Psi = 1
    elif x > 0.09:
        Psi = 1.83
    else:
        # Psi = (((2*10**8)*(x**6)) - ((5*10**7)*(x**5)) + ((7*10**6)*(x**4)) - ((504474)*(x**3)) + ((17852)*(x**2)) - ((277.15)*(x)) + (2.5222))
        x_data = np.array([0.010144927536231885, 0.01238471673254282, 0.013965744400527011, 0.015415019762845851, 0.016732542819499343, 0.018050065876152835, 0.018972332015810278, 0.02002635046113307, 0.020948616600790518, 0.02200263504611331, 0.022661396574440055, 0.023583662714097498, 0.024374176548089595, 0.02516469038208169, 0.025955204216073783, 0.02700922266139658, 0.028063241106719372, 0.029117259552042165, 0.030434782608695657, 0.03122529644268775, 0.0321475625823452, 0.03333333333333334, 0.03425559947299078, 0.035441370223978926, 0.03689064558629777, 0.03833992094861661, 0.03978919631093544, 0.04110671936758894, 0.043214756258234524, 0.044927536231884065, 0.04729907773386035, 0.05006587615283268, 0.05349143610013176, 0.057180500658761534, 0.06047430830039526, 0.06416337285902504, 0.06679841897233202, 0.0702239789196311, 0.07312252964426878, 0.07536231884057971, 0.0772068511198946, 0.07997364953886694, 0.08274044795783927, 0.0855072463768116, 0.08906455862977604])

        y_data = np.array([1, 1.0062355658198614, 1.0166281755196305, 1.0290993071593533, 1.0457274826789837, 1.0623556581986142, 1.0810623556581986, 1.097690531177829, 1.1163972286374133, 1.1351039260969977, 1.153810623556582, 1.1766743648960738, 1.197459584295612, 1.2265588914549652, 1.2556581986143187, 1.295150115473441, 1.3325635103926097, 1.3699769053117783, 1.405311778290993, 1.4302540415704388, 1.4551963048498844, 1.482217090069284, 1.503002309468822, 1.5279445727482677, 1.5528868360277137, 1.5757505773672054, 1.590300230946882, 1.6090069284064663, 1.6318706697459584, 1.6505773672055426, 1.6672055427251733, 1.6859122401847575, 1.7066974595842956, 1.7316397228637412, 1.746189376443418, 1.7648960739030022, 1.7711316397228636, 1.7836027713625864, 1.7939953810623557, 1.8023094688221708, 1.810623556581986, 1.810623556581986, 1.8147806004618938, 1.8251732101616627, 1.831408775981524])

        coefficients_new = np.polyfit(x_data, y_data, 10)
        polynomial_new = np.poly1d(coefficients_new)

        # Testando um valor específico
        Psi = polynomial_new(x)      

    return Psi

def nlc( Flow_info) -> float:
    x_test = liquid_viscosity_number(Flow_info)
    if x_test < (0.002):
        nlc = 0.001873
    elif x_test > (0.5):
        nlc = 0.0113
    else:
        x = [0.0019306977288832496, 0.0021928747399631828, 0.0025712141464285625, 0.003046989570903508, 0.0034607522259998465, 0.003930701333582669, 0.004512091314336601, 0.005179474679231213, 0.006073095888063095, 0.0071208946755741895, 0.008528557386046992, 0.010214487701467307, 0.011976805969762905, 0.013894954943731374, 0.01612030564540799, 0.018702058060188872, 0.021241683818230137, 0.02412617531084188, 0.027402363207662817, 0.031455446376766, 0.03572690471530962, 0.042337782801723636, 0.04859996367971544, 0.0551995432128157, 0.06336410689816542, 0.0735122045579249, 0.08261343710999333, 0.09284145445194744, 0.10214487701467312, 0.11479099863901436, 0.12764117205368128, 0.14192984638518655, 0.15781805330376297, 0.17179995331294348, 0.18901562029448687, 0.2124168381823014, 0.23871526106185034, 0.2682695795279725, 0.3014828921284107, 0.3424224355729867, 0.3848162970540386, 0.43245876173560044, 0.48599963679715436]
        y = [0.0019101354890282004, 0.0019101354890282004, 0.001947395440693419, 0.0019662970902942483, 0.001985382201533208, 0.002043756198667801, 0.002063593137139315, 0.0021242666839160085, 0.0021242666839160085, 0.002186724147886555, 0.002272866625333268, 0.0023396932090369305, 0.0024554655921590913, 0.0025521947061619595, 0.00265273430788889, 0.0027839965483518756, 0.002865851319896976, 0.003007658987541932, 0.0031871207644077167, 0.0033126722560456933, 0.00347658945685808, 0.003719789142440212, 0.0040186318667113355, 0.0042997493292655075, 0.004690271969670726, 0.00506708194446123, 0.005527297196227699, 0.0059139511158010525, 0.0063276528397919925, 0.006836007733167704, 0.0072439004163289515, 0.007825865375058938, 0.008373312239936237, 0.00870316539561667, 0.009222468126652231, 0.009585772411452392, 0.0100600943062436, 0.010355880133150332, 0.010763833359291333, 0.010973797475974866, 0.011080310447273338, 0.011187857246021206, 0.011296447906669511]

        spline = UnivariateSpline(np.log(x), np.log(y), k=3, s=0.001)
        def predict_y(x_value):
            return np.exp(spline(np.log(x_value)))

        nlc = predict_y(x_test)

    return nlc

def HL_HB( Flow_info, tubing ) -> float:
    
    x_test = (
        ((liquid_velocity_number(Flow_info))/(gas_velocity_number(Flow_info))**0.575)*
         (((Flow_info.pressure*0.0001450377)/(14.7))**0.10)*
         ((nlc(Flow_info))/(diameter_tubing_number(Flow_info,tubing)))
        )
   
    if x_test < 1.2077226551344623e-7:
        y_pred =  0.0
    elif x_test > 0.005858137524004617:
        y_pred = 1.0
    else:
        x = [1.2077226551344623e-7, 1.4585940117250354e-7, 1.7895022156272113e-7, 2.1954828787123655e-7, 2.6101572156825384e-7, 3.202318179734705e-7, 4.0543710976836477e-7, 4.820145070719145e-7, 5.64113015651022e-7, 6.498925074488289e-7, 7.973322752256328e-7, 9.93728532163703e-7, 0.0000012191736670684703, 0.0000014957650730192784, 0.0000017505293589026523, 0.0000020811625914767567, 0.000002435633966018562, 0.0000028956671139669238, 0.0000034971627752656786, 0.00000422360271238127, 0.000004865847234617288, 0.000005876593941670659, 0.0000068775173393231, 0.00000792331831506712, 0.000009272847441516206, 0.000011199027932724732, 0.0000133142571279698, 0.00001633483507981373, 0.000019727950393776196, 0.00002420358965939684, 0.000029231223567231827, 0.000034752304314023046, 0.0000406714463979415, 0.000048353312301890406, 0.000057486099404679175, 0.00006622748323302575, 0.00007629808911723947, 0.00008517808440132827, 0.00009813033437525335, 0.00011305211419439773, 0.00012821047148237337, 0.0001454013055383183, 0.00016489713677680354, 0.0001870070259446334, 0.0002120814735551935, 0.00023676469310632658, 0.0002643206828112887, 0.00029508379161267354, 0.00032942728183960697, 0.0003563793802936025, 0.00039785679149705895, 0.00043040745140336385, 0.0004656212440825166, 0.0005117011505108638, 0.0005535659885126732, 0.0006179930721303395, 0.0006791523583507204, 0.0007463642339279569, 0.000820227689468164, 0.0009156903425781838, 0.001006311047366872, 0.0011412401683967913, 0.00129426097961489, 0.0014677992676220704, 0.0016646060755636306, 0.0019177274523866814, 0.0022093386751530796, 0.0025856414783156983, 0.0030740074665268945, 0.003712548459377023, 0.004413760291083362, 0.005084920332036381, 0.005084920332036381, 0.005858137524004617]

        y = [0.002325581395348837, 0.002325581395348837, 0.004651162790697674, 0.004651162790697674, 0.0069767441860465115, 0.0069767441860465115, 0.009302325581395349, 0.011627906976744186, 0.011627906976744186, 0.01627906976744186, 0.018604651162790697, 0.023255813953488372, 0.030232558139534883, 0.03953488372093023, 0.046511627906976744, 0.053488372093023255, 0.06279069767441861, 0.06744186046511627, 0.07209302325581396, 0.08372093023255814, 0.09302325581395349, 0.10697674418604651, 0.11627906976744186, 0.12790697674418605, 0.14186046511627906, 0.15348837209302324, 0.16511627906976745, 0.17674418604651163, 0.18372093023255814, 0.19534883720930232, 0.20465116279069767, 0.21395348837209302, 0.22790697674418603, 0.2441860465116279, 0.26046511627906976, 0.2744186046511628, 0.29069767441860467, 0.30930232558139537, 0.32790697674418606, 0.3441860465116279, 0.3627906976744186, 0.38372093023255816, 0.4046511627906977, 0.4255813953488372, 0.4511627906976744, 0.4744186046511628, 0.49534883720930234, 0.5209302325581395, 0.541860465116279, 0.5604651162790698, 0.5837209302325581, 0.6046511627906976, 0.6255813953488372, 0.6441860465116279, 0.6674418604651162, 0.6930232558139535, 0.7186046511627907, 0.7395348837209302, 0.7651162790697674, 0.7883720930232558, 0.8093023255813954, 0.8302325581395349, 0.8488372093023255, 0.872093023255814, 0.8930232558139535, 0.9093023255813953, 0.9232558139534883, 0.9418604651162791, 0.9558139534883721, 0.9674418604651163, 0.9744186046511628, 0.9837209302325581, 0.9837209302325581, 0.9906976744186047]

        spline = UnivariateSpline(np.log(x), y, k=3, s=0.001)

        def predict_y(x_value):
            return spline(np.log(x_value))
        
        y_pred = predict_y(x_test)

    hl = y_pred*psi(Flow_info, tubing)

    if hl > 1:
        hl = 1
    elif hl < 0:
        hl = 0 

    return hl

def slip_viscosity_Hb( Flow_info, tubing) -> float:
    Hl = HL_HB(Flow_info,tubing)
    return  ( (Flow_info.liquid_viscosity**Hl) * ( (Flow_info.gas_viscosity)**(1-Hl) ) )

def reynolds_HB(Flow_info, tubing) -> float:

    a = slip_viscosity_Hb(Flow_info,tubing)
    
    reynolds = (Flow_info.mix_rho*Flow_info.vm*tubing.Dh) / (slip_viscosity_Hb(Flow_info,tubing)) 
    
    return  reynolds

def FD_HB(Flow_info, tubing) -> float:
    re = reynolds_HB(Flow_info,tubing)
    def f(F):
        return ((- 2*np.log10( ( (tubing.e/tubing.Dh) / (3.7) ) + ( 2.51 / ( re*np.sqrt(F) ) ))) - ( 1 / np.sqrt(F) )) 

    F = fsolve(f,0.001)[0]

    return F

def mix_slip_density_HB( Flow_info,  tubing) -> float:
    Hl = HL_HB(Flow_info,tubing)
    return ( ( Flow_info.liquid_rho * Hl ) + Flow_info.gas_rho*( 1 - Hl) )

def friction_gradient_HB( Flow_info, tubing) -> float:
    return ( FD_HB( Flow_info , tubing  ) * ( ( Flow_info.mix_rho**2 * Flow_info.vm**2 ) / (2*tubing.Dh*mix_slip_density_HB(Flow_info, tubing)) ) )

def gravitational_gradient_HB( Flow_info, tubing) -> float:
    if tubing.direction == "Descendente":
        angle = tubing.angle*-1
    else:
        angle = tubing.angle
    grav = mix_slip_density_HB(Flow_info, tubing) * g * np.sin(angle)
    return grav
