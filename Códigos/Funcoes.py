# -------------------------------------DESCOBRIR A CARGA COM MAIOR POTÊNCIA ATIVA---------------------------------------
def Carga_max_W(dss):
        dss.loads_first()
        kW_carga_max = 0.0
        for _ in range(dss.loads_count()):
            kW_carga = dss.loads_read_kw()

            if kW_carga > kW_carga_max:
                kW_carga_max = kW_carga
                nome_da_carga = dss.loads_read_name()
            dss.loads_next()

        dss.circuit_setactiveelement(nome_da_carga)
        print("\nA MAIOR CARGA ATIVA É A {} COM UMA POTÊNCIA DE {} kW".format(nome_da_carga, kW_carga_max))

# ------------------------------------PEGAR DADOS DA SUBESTAÇÃO E SISTEMA ELÉTRICO--------------------------------------
def Dados_sub(dss, np, plt):

    dss.monitors_write_name('M1')

    # PEGANDO A POTÊNCIA ATIVA E REATIVA FORNECIDA PELA SUBESTAÇÃO
    pa = dss.monitors_channel(1)
    qa = dss.monitors_channel(2)
    pb = dss.monitors_channel(3)
    qb = dss.monitors_channel(4)
    pc = dss.monitors_channel(5)
    qc = dss.monitors_channel(6)

    pt = np.array(pa) + np.array(pb) + np.array(pc)     # POTÊNCIA ATIVA
    qt = np.array(qa) + np.array(qb) + np.array(qc)     # POTÊNCIA REATIVA

    dss.meters_first()

    P_mW = dss.circuit_totalpower()[0]                  # POTÊNCIA TOTAL ATIVA FORNECIDA PELA SUBESTAÇÃO
    Q_mVAR = dss.circuit_totalpower()[1]                # POTÊNCIA TOTAL REATIVA FORNECIDA PELA SUBESTAÇÃO
    print("\nA POTÊNCIA TOTAL FORNECIDA PELA SUBESTAÇÃO É DE {} mW E A REATIVA É DE {} mvar".format(P_mW, Q_mVAR))

    Perdas_mW = dss.circuit_losses()[0] / 10 ** 6       # PERDAS TOTAIS ATIVA
    Perdas_mVAR = dss.circuit_losses()[1] / 10 ** 6     # PERDAS TOTAIS REATIVA
    print("\nAS PERDAS ATIVAS É DE {} mW E A REATIVA É DE {} mvar".format(Perdas_mW, Perdas_mVAR))

    P_max = pt.max()                                    # POTENCIA MAXIMA FORNECIDA PELA SUBESTAÇÃO
    hora_de_pico_max = pt.argmax()                      # HORA CORRESPONDENTE
    print("\nO VALOR MAX DE POTENCIA FORNECIDA PELA SUBESTAÇÃO É {} mW ÀS {} h".format(P_max, hora_de_pico_max))

    energia_na_rede = dss.meters_registervalues()[0]    # ENERGIA TOTOL NO ALIMENTADOR
    consumo_das_cargas = dss.meters_registervalues()[4] # ENERGIA CONSUMIDA PELAS CARGAS
    perdas_na_rede = dss.meters_registervalues()[12]    # ENERGIA PERDIDA NA REDE
    print("\nA ENERGIA TOTOL NA REDE É {} kWh\nA ENERGIA CONSUMIDA PELAS CARGAS É {} kWh\nA ENERGIA PERDIDA NA REDE É "
          "{} kWh".format(energia_na_rede, consumo_das_cargas, perdas_na_rede))

    return pt, qt

# ------------------------------------CLASSIFICAÇÃO DAS BARRAS PELO NÚMERO DE FASES-------------------------------------
def Classificacao_barras(dss):
    barras_lista = dss.circuit_allbusnames()

    # LISTAS COM AS BARRAS DA REDE, SEPARANDO-AS DE ACORDO COM O NÚMERO DE FASES
    barras_3fase_lista = list()
    barras_2fase_lista = list()
    barras_1fase_lista = list()

    # DICIONÁRIOS DAS TENSÕES DE BASE DAS BARRAS, SEPARADAS PELO NÚMERO DE FASE
    kV_base_3fase_dict = dict()
    kV_base_2fase_dict = dict()
    kV_base_1fase_dict = dict()

    for barra in barras_lista:
        dss.circuit_setactivebus(barra)             # ATIVANDO A BARRA
        num_fases = len(dss.bus_nodes())            # NUMERO DE FASES DA BARRA
        kv_base = dss.bus_kVbase()                  # TENSÃO DE BASE DA BARRA

        if num_fases == 1:
            barras_1fase_lista.append(barra)
            kV_base_1fase_dict[barra] = kv_base
        elif num_fases == 2:
            barras_2fase_lista.append(barra)
            kV_base_2fase_dict[barra] = kv_base
        else:
            barras_3fase_lista.append(barra)
            kV_base_3fase_dict[barra] = kv_base

    print("\nO CIRCUITO POSSUI:\n{} BARRAS TRIFÁSICAS\n{} BARRAS BIFASICAS\n{} BARRAS MONOFASICAS".format(
        len(barras_3fase_lista), len(barras_2fase_lista), len(barras_1fase_lista)))

# ------------------------------------DECLARANDO OS MONITORES DE TENSÃO E PERDAS----------------------------------------
def Declarando_monitores(dss):
    nome_tensao = list()
    nome_perdas = list()
    nome_t = "0"
    linhas_lista = dss.lines_allnames()

    for linhas in linhas_lista:
        dss.lines_write_name(linhas)                # ATIVANDO AS LINHAS
        barras = dss.lines_read_bus1()[0:3]         # PEGANDO A BARRA DO TERMINAL 1 DA LINHA

        # -----------------------------------------------MONITORES DE PERDAS------------------------------------------------
        nome_p = "Linha_" + str(linhas)             # NOME PARA DIFERIR OS MONITORES DE PERDAS
        nome_perdas.append(nome_p)                  # LISTA COM OS NOMES DOS MONITORES DE PERDAS
        dss.text("New Monitor.{} element = Line.{} terminal = 1 mode = 9 ppolar = false".format(nome_p, linhas))

        # -----------------------------------------------MONITORES DE TENSÃO------------------------------------------------
        nome_tensao.append(nome_t)                  # LISTA COM OS NOMES DOS MONITORES DE TENSÃO
        nome_t = ('Barra_' + str(barras))           # NOME PARA DIFERIR OS MONITORES DE TENSÃO
        if nome_t in nome_tensao:                   # TESTE PRA EVITAR QUE A SEJA CRIADO DOIS MONITORES PRA MESMA BARRA
            variavel = "Essa variável não tem nenhuma função para as análises, apenas auxilia na logica pra evitar termos" \
                       " monitores repetidos"
        else:
            dss.text("New Monitor.{} element = Line.{} terminal = 1 mode = 0 ppolar = false".format(nome_t, linhas))

    monitores_des = dss.monitors_allnames()         # LISTA DE TODOS OS MONITORES
    monitores = sorted(monitores_des)               # MONITORES ORGANIZADOS NA ORDEM ALFABÉTICA

    return monitores

# --------------------------------------------------MODO DE SOLUÇÃO-----------------------------------------------------
def Modo_de_Solucao(dss):
    dss.text("set mode = daily")
    dss.text("set number = 24")
    dss.text("set stepsize = 1h")
    dss.text("solve")

    dss.text("Set MarkTransformers=yes")
    dss.text("Interpolate")
