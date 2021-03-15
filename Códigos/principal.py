import Funcoes
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Plotar
import py_dss_interface
import PV_System

# ----------------------------------INICIALIZANDO O OPEN DSS E COMPILANDO ARQUIVO---------------------------------------
dss = py_dss_interface.DSSDLL()
dss_file = r"C:\Users\mjmde\Dropbox\MEU_DROPBOX\PIBIC\PIBIC_2020\Projeto_2021\34_barras\ieee34Mod1.dss"
dss.text("Compile [{}]".format(dss_file))

# -----------------------------------------------ATIVANDO ENERGYMETER---------------------------------------------------
dss.text("New Energymeter.M1  Line.L1")
dss.text("New monitor.M1 element = line.L1 terminal = 1 mode = 1 ppolar = no")

# ------------------------------------DECLARANDO OS MONITORES DE TENSÃO E PERDAS----------------------------------------
monitores = Funcoes.Declarando_monitores(dss)

# -----------------------------------------------LOADSHAPE DAS CARGAS---------------------------------------------------
dss.text("New LoadShape.DIA npts=24	interval=1 mult= [0.14594594594594595, 0.14594594594594595, 0.14594594594594595,"
         " 0.22702702702702704, 0.2594594594594595, 0.3216216216216216, 0.42702702702702705, 0.5864864864864865, "
         "0.5864864864864865, 0.5864864864864865, 0.5378378378378378, 0.3783783783783784, 0.5567567567567567, "
         "0.6432432432432432, 0.6378378378378379, 0.5837837837837838, 0.4864864864864865, 0.44324324324324327, 1.0, "
         "0.8378378378378378, 0.7027027027027027, 0.4864864864864865, 0.21621621621621623, 0.13513513513513514]")
dss.text("Batchedit load..* daily = DIA")       # COMANDO QUE APLICA ESSE LOADSHAPE EM TODAS AS CARGAS DA REDE

# ------------------------------------CLASSIFICAÇÃO DAS BARRAS PELO NÚMERO DE FASES-------------------------------------
#Funcoes.Classificacao_barras(dss)

# ---------------------------------------------------DEFININDO UFV------------------------------------------------------

# -------------------------Obtenção e tratamento dos dados de Irradiância e temperatura---------------------------------
# lendo o arquivo das irradiâncias
Curva_Irrad = pd.read_csv(r'C:\Users\mjmde\Dropbox\MEU_DROPBOX\PIBIC\PIBIC_2020\Projeto_2021\Irrad_13d.csv', sep=';',
                          encoding='ISO-8859-1')
# lendo o arquivo das temperaturas
Curva_Temp = pd.read_csv(r"C:\Users\mjmde\Dropbox\MEU_DROPBOX\PIBIC\PIBIC_2020\Projeto_2021\Temp_13d.csv", sep=';',
                          encoding='ISO-8859-1')

# lendo o cabeçalho das colunas, obtendo os dias referentes aos dados de irradiância e temperatura (pq são iguais nos
# dois aquivos)
Dia_da_curva = Curva_Irrad.columns

# declaração de variaveis necessárias
perdas = dict()
Curva_Irrad_corrigida = list()
Curva_Temp_corrigida = list()

for dia in Dia_da_curva:

    Curva_Temp_corrigida.clear()
    Curva_Irrad_corrigida.clear()

    #tratamento dos dados de Irradiância
    Curva_I = Curva_Irrad[dia].to_dict().values()
    for x in Curva_I:
        item = x
        if x in ['(', ')', 'dict_values']:
            item = Curva_I.replace(x, "")
        Curva_Irrad_corrigida.append(item)

    # tratamento dos dados de Irradiância
    Curva_T = Curva_Temp[dia].to_dict().values()
    for z in Curva_T:
        item1 = z
        if z in ['(', ')', 'dict_values']:
            item1 = Curva_T.replace(z, "")
        Curva_Temp_corrigida.append(item1)

    PV_System.define_pvsystem_with_transformer(dss, dia, Curva_Irrad_corrigida, Curva_Temp_corrigida)

# ------------------------------------------------MODO DE SOLUÇÃO---------------------------------------------------
    Funcoes.Modo_de_Solucao(dss)
    perdas[dia] = dss.circuit_losses()

# ----------------------------------------------PLOTANDO MONITORES------------------------------------------------------
    Plotar.Plot_PV(dss, dia)

print("here")