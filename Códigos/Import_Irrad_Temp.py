import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# lendo a planilha de irradiância
Irrad = pd.read_csv('Irrad_13d.csv', sep=';', encoding='ISO-8859-1')
Irrad.plot()
plt.legend()
plt.xlabel("Horário (h)")
plt.ylabel(" Irradiância (W/m²)")
plt.xticks(np.arange(0, 25, 3))
plt.grid(True)
plt.xlim(0, 24)
#plt.show()

# lendo a planilha de temperatura
Temp = pd.read_csv('Temp_13d.csv', sep=';', encoding='ISO-8859-1')
Temp.plot()
#plt.legend(loc= (1.04,0.25))
plt.legend(bbox_to_anchor=(0, 1.03, 1, 0.1), loc="upper left", mode="expand", borderaxespad=0, ncol=7)
plt.xlabel("Horário (h)")
plt.ylabel(" Temperatura (°C)")
plt.xticks(np.arange(0, 25, 3))
plt.xlim(0, 24)
plt.grid(True)
plt.show()

# ------------------------------------------Curva de EficiÊncia do Inversor---------------------------------------------
inv = pd.read_csv('inversor.csv', sep=';', encoding='ISO-8859-1')
x = inv['X0']
y = inv['Y0']
plt.plot(x, y)
plt.xlabel("Potência nominal (%)")
plt.ylabel(" Eficiência de conversão (%)")
#plt.xticks(np.arange(0, 25, 3))
plt.xlim(0, 100)
plt.grid(True)
plt.show()