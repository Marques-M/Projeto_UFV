# -------------------------------------------------PLOTANDO CIRCUITO----------------------------------------------------
def Plot_circuit(dss):
    dss.text("Buscoords IEEE34_BusXY.csv")
    dss.text("plot circuit Power max=2000 dots=n labels=n  C1=Blue 1ph=3")

# ---------------------------------------PLOTANDO AS TENSÕES E PERDAS DO SISTEMA----------------------------------------
def Plot_Monitores(dss, plt, np, monitores):
    for monitor in monitores:
        # TENSÕES
        dss.monitors_write_name(monitor)
        num_fases = dss.monitors_numchannels()

        if "barra_" in str(monitor):
            # COMANDOS PARA PLOTAR OS GRÁFICOS DE TENSÃO
            if num_fases == 12:
                Fase_A = dss.monitors_channel(1)
                Fase_B = dss.monitors_channel(3)
                Fase_C = dss.monitors_channel(5)

                plt.plot(list(range(1, len(Fase_A) + 1)), Fase_A, "g", label='Fase A')
                plt.plot(list(range(1, len(Fase_B) + 1)), Fase_B, "b", label='Fase B')
                plt.plot(list(range(1, len(Fase_C) + 1)), Fase_C, "r", label='Fase C')

            else:
                Fase_A = dss.monitors_channel(1)
                plt.plot(list(range(1, len(Fase_A) + 1)), Fase_A, "g", label='Fase A')

            plt.title("{}".format(monitor))
            plt.legend()
            plt.ylabel("Tensão (V)")
            plt.xlabel("Horário")
            plt.xlim(1, 24)
            plt.grid(True)
            #plt.savefig(r"C:\Users\mjmde\Dropbox\GFALEVALE\Matheus Marques\PIBIC\PIBIC 2020\pythonProject\Gráficos\TENSÃO\tensão_da_{}".format(monitor))
            plt.show()

        else:
            # PERDAS
            dss.monitors_write_name(monitor)
            Perdas_A = dss.monitors_channel(1)          #perdas da fase A
            Perdas_B = dss.monitors_channel(3)          #perdas da fase B
            Perdas_C = dss.monitors_channel(5)          #perdas da fase C

            # COMANDOS PARA PLOTAR OS GRÁFICOS DE PERDAS
            Perdas_totais_kW = np.array(Perdas_A) + np.array(Perdas_B) + np.array(Perdas_C)  #perdas totais em kW em cada hora
            plt.plot(list(range(1, len(Perdas_totais_kW) + 1)), Perdas_totais_kW, "b", label='Perdas Ativas')
            plt.title("{}".format(monitor))
            plt.legend()
            plt.ylabel("Potência (kW)")
            plt.xlabel("Horário")
            plt.xlim(1, 24)
            plt.grid(True)
            #plt.savefig(r"C:\Users\mjmde\Dropbox\GFALEVALE\Matheus Marques\PIBIC\PIBIC 2020\pythonProject\Gráficos\PERDAS\perdas_da_{}".format(monitor))
            plt.show()

# ----------------------------------------------PERFIL DE TENSÃO DA REDE------------------------------------------------
def Plot_Profile(dss, dia):
    dss.text("Plot profile{} phases=all".format(dia))

# ---------------------------------------------PLOTAR OS MONITORES DE CADA----------------------------------------------
def Plot_PV(dss, dia):
    #dss.text("Plot monitor object = variaveis{} channels = (2)".format(dia))
    dss.text("Plot monitor object = PV_{}_P channels = (1 3 5 7)".format(dia))
# ------------------------------PLOTAR POTÊNCIA ATIVA E REATIVA FORNECIDA PELA SUBESTAÇÃO-------------------------------
def Plot_P_Q(dss, plt, pt, qt):
    plt.plot(list(range(1, len(pt) + 1)), pt, "g", label='P')
    plt.plot(list(range(1, len(qt) + 1)), qt, "b", label='Q')
    plt.title("Daily active and reative power at feeder")
    plt.legend()
    plt.ylabel("kW, kvar")
    plt.xlabel("Hour")
    plt.xlim(1, 24)
    plt.grid(True)
    plt.show()
