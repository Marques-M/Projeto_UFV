# Projeto_UFV
 Esse projeto tem como objetivo realizar simulações com uma unidade fotovoltaica variando as condições climáticas

O projeto foi dividido em funções para facilitar a escrita e entendimento, sendo dividido nas seguintes funções

Principal ---> é o codigo principal onde as demais funções são chamadas
Plotar ---> esse arquivo possui as funções responsáveis por fazer todas as plotagens de gráficos
Import_Irrad_Temp ---> é o arquivo que possui o codigo responsável por fazer a leituras dos aquitvos de temperatura (Temp_13d.csv) e o arquivo de irradiência (Irrad_13d)
Valor_da_Potencia ---> é o código responsável por calcular a potência para a unidade fotovoltaica a partir da curva de carga utilizada e da energia consumida por o sistema elétrico de 34 barras
PV_System ---> é onde a unidade fotovoltaica é definida utilizando o elemento PVSystem do OpenDSS
Funcoes ---> é onde possui algumas funções responsáveis por fazer cálculos de grandezas relacionadas ao sistema elétrico