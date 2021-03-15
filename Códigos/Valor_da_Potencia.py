import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import py_dss_interface
import Funcoes


# ----------------------------------------------Curva resultante Kagan--------------------------------------------------
y = np.array([270,270,270,270,420,480,595,790,1085,1085,1085,995,700,1030,1190,1180,1080,900,820,1850,1550,1300,900,400,
              250])
x = np.array([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24])
fun_kag = np.poly1d(np.polyfit(x, y, 10))

y_min_kagan = min(y)
y_max_kagan = max(y)
y_pu_kagan = list()
for n in range(0, 25):
    y_pu_kagan.append(y[n]/y_max_kagan) # curva em PU

plt.legend()
plt.ylabel("Potência (pu)")
plt.xlabel("Horário (h)")
plt.plot(x, y_pu_kagan)
plt.xticks(np.arange(0, 25, 3))
plt.xlim((0, 24))
plt.grid(True)
plt.show()

# ----------------------------------INICIALIZANDO O OPEN DSS E COMPILANDO ARQUIVO---------------------------------------
dss = py_dss_interface.DSSDLL()
dss_file = r"C:\Users\mjmde\Dropbox\MEU_DROPBOX\PIBIC\PIBIC_2020\Projeto_2021\34_barras\ieee34Mod1.dss"
dss.text("Compile [{}]".format(dss_file))

# -------------------------------------------ATIVANDO ENERGYMETER-------------------------------------------------------
dss.text("New Energymeter.M1  Line.L1")
dss.text("New monitor.M1 element = line.L1 terminal = 1 mode = 1 ppolar = no")

# -----------------------------------------------LOADSHAPE DAS CARGAS---------------------------------------------------
dss.text("New LoadShape.DIA npts=24	interval=1 mult= [0.14594594594594595, 0.14594594594594595, 0.14594594594594595, "
         "0.22702702702702704, 0.2594594594594595, 0.3216216216216216, 0.42702702702702705, 0.5864864864864865, "
         "0.5864864864864865, 0.5864864864864865, 0.5378378378378378, 0.3783783783783784, 0.5567567567567567, "
         "0.6432432432432432, 0.6378378378378379, 0.5837837837837838, 0.4864864864864865, 0.44324324324324327, 1.0, "
         "0.8378378378378378, 0.7027027027027027, 0.4864864864864865, 0.21621621621621623, 0.13513513513513514]")
dss.text("Batchedit load..* daily = DIA")       # COMANDO QUE APLICA ESSE LOADSHAPE EM TODAS AS CARGAS DA REDE

# ------------------------------------------------MODO DE SOLUÇÃO---------------------------------------------------
Funcoes.Modo_de_Solucao(dss)

# ------------------------------------------Valor da Potência da UFV----------------------------------------------------
energia_sistema = dss.meters_registervalues()[0]
Potencia_UFV = energia_sistema/24
print("here")