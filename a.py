import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

def compute_Psi(x):
    # Verificação de inicialização única
    if not hasattr(compute_Psi, 'spline'):
        # Dados originais (mantidos dentro da função conforme estrutura original)
        x_data = np.array([
            0.010144927536231885, 0.01238471673254282, 0.013965744400527011, 0.015415019762845851, 
            0.016732542819499343, 0.018050065876152835, 0.018972332015810278, 0.02002635046113307, 
            0.020948616600790518, 0.02200263504611331, 0.022661396574440055, 0.023583662714097498, 
            0.024374176548089595, 0.02516469038208169, 0.025955204216073783, 0.02700922266139658, 
            0.028063241106719372, 0.029117259552042165, 0.030434782608695657, 0.03122529644268775, 
            0.0321475625823452, 0.03333333333333334, 0.03425559947299078, 0.035441370223978926, 
            0.03689064558629777, 0.03833992094861661, 0.03978919631093544, 0.04110671936758894, 
            0.043214756258234524, 0.044927536231884065, 0.04729907773386035, 0.05006587615283268, 
            0.05349143610013176, 0.057180500658761534, 0.06047430830039526, 0.06416337285902504, 
            0.06679841897233202, 0.0702239789196311, 0.07312252964426878, 0.07536231884057971, 
            0.0772068511198946, 0.07997364953886694, 0.08274044795783927, 0.0855072463768116, 
            0.08906455862977604
        ])
        
        y_data = np.array([
            1, 1.0062355658198614, 1.0166281755196305, 1.0290993071593533, 1.0457274826789837, 
            1.0623556581986142, 1.0810623556581986, 1.097690531177829, 1.1163972286374133, 
            1.1351039260969977, 1.153810623556582, 1.1766743648960738, 1.197459584295612, 
            1.2265588914549652, 1.2556581986143187, 1.295150115473441, 1.3325635103926097, 
            1.3699769053117783, 1.405311778290993, 1.4302540415704388, 1.4551963048498844, 
            1.482217090069284, 1.503002309468822, 1.5279445727482677, 1.5528868360277137, 
            1.5757505773672054, 1.590300230946882, 1.6090069284064663, 1.6318706697459584, 
            1.6505773672055426, 1.6672055427251733, 1.6859122401847575, 1.7066974595842956, 
            1.7316397228637412, 1.746189376443418, 1.7648960739030022, 1.7711316397228636, 
            1.7836027713625864, 1.7939953810623557, 1.8023094688221708, 1.810623556581986, 
            1.810623556581986, 1.8147806004618938, 1.8251732101616627, 1.831408775981524
        ])
        
        # Pré-processamento (ordenação e remoção de duplicatas)
        sorted_idx = np.argsort(x_data)
        x_sorted = x_data[sorted_idx]
        y_sorted = y_data[sorted_idx]
        
        # Remover duplicatas mantendo a correspondência com y
        unique_mask = np.append(True, np.diff(x_sorted) > 1e-20)
        x_unique = x_sorted[unique_mask]
        y_unique = y_sorted[unique_mask]
        
        # Armazenar parâmetros
        compute_Psi.x_min = x_unique[0]
        compute_Psi.x_max = x_unique[-1]
        compute_Psi.x_data = x_unique
        compute_Psi.y_data = y_unique
        
        # Criar spline
        compute_Psi.spline = UnivariateSpline(x_unique, y_unique, k=3, s=0.001)
    
    # Verificação de limites dinâmicos
    if x < compute_Psi.x_min:
        return 1.0
    elif x > compute_Psi.x_max:
        return 1.83
    return compute_Psi.spline(x)

# Testes (mantendo a estrutura original)
x_values = np.linspace(0, 0.1, 1000)
psi_values = [compute_Psi(x) for x in x_values]

print("Resultados da interpolação:")
for x, psi in zip(x_values, psi_values):
    print(f"x = {x:.6f}, Psi = {psi:.6f}")

# Plotagem com dados processados
plt.plot(x_values, psi_values, label="Interpolação Spline", color='b')
plt.scatter(compute_Psi.x_data, compute_Psi.y_data, color='r', label="Pontos Originais")
plt.xlabel("x")
plt.ylabel("Psi")
plt.legend()
plt.title("Interpolação Spline de Psi(x)")
plt.grid()
plt.show()
