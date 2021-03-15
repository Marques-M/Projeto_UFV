# -----------------------------FUNÇÃO PARA IMPORTAR AS CURVAS DE IRRADIÂNCIA DO ARQUIVO CSV-----------------------------
def define_pvsystem_with_transformer(dss, Dia_da_curva, Curva_Irrad, Curva_temp):

    # Declarando a variavel 
    bus = 34
    kva = 861.21
    pmpp = 861.21

    #CURVA DE TEMPERATURA DO PAINEL
    dss.text("New XYCurve.MyPvsT npts=4  xarray=[5  25 45 65]  yarray=[1.15   1  1.01  .86]")
    #CURVA DE EFICIÊNCIA DO INVERSOR
    dss.text("New XYCurve.MyEff npts=4  xarray=[.2 .3 .5  1 ]  yarray=[0.985 .987 .987 .96]")
    #CURVA DE IRRADIÂNCIA NO INVERSOR
    dss.text("New Loadshape.MyIrrad{} npts=24 interval=1 mult= {}".format(Dia_da_curva, Curva_Irrad))
    #CURVA DE TEMPERATURA DO AMBIENTE
    dss.text("New Tshape.MyTemp{} npts=24 interval=1 temp= {}".format(Dia_da_curva, Curva_temp))

    #DEFININDO O PVSystem
    dss.text("New PVSystem.PV_{} phases=3 conn=wye  bus1= trafo_pv kV=0.80 kVA={} Pmpp={} pf=1 %cutin=0.00005 "
             "%cutout=0.00005 VarFollowInverter=yes effcurve=Myeff  P-TCurve=MyPvsT Daily=MyIrrad{}  "
             "TDaily=MyTemp{}".format(Dia_da_curva, kva, pmpp, Dia_da_curva, Dia_da_curva))

    dss.text("New Transformer.PV_{}	phases=3 xhl=5.750000 "
             "wdg=1	bus=trafo_pv kv= 0.80 kva=250000 conn=wye"
             " wdg=2 bus= {} kv= 2.4 kva=250000 conn=wye".format(Dia_da_curva, bus))


    dss.text("New monitor.PV_{}_V element=transformer.PV_{} terminal=2 mode=0".format(Dia_da_curva, Dia_da_curva)) # TENSÃO
    dss.text("New monitor.PV_{}_P element=transformer.PV_{} terminal=2 mode=1 ppolar=no".format(Dia_da_curva,
                                                                                                Dia_da_curva)) # POTENCIA
    dss.text("New monitor.PV_{}_M element=PVSystem.PV_{} terminal=1 mode=3".format(Dia_da_curva, Dia_da_curva))
    dss.text("New monitor.variaveis{} element= PVSystem.PV_{}	terminal=1 	mode=3".format(Dia_da_curva, Dia_da_curva))

    #dss.text("Plot monitor object = PV_{}_P channels = (1 3 5 7)".format(Dia_da_curva))

def add_bus_marker(dss, bus, color, size_marker=8, code=15):
    dss.text("AddBusMarker bus={} color={} size={} code={}".format(bus, color, size_marker, code))