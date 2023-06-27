import os
if download:
    print(download)
    dados1 = {}
    falhas = []

    for ticker in tqdm(símbolos):
        yq.Ticker(ticker, backoff_factor=0.1, retry=3, status_forcelist=[404, 429, 500, 502, 503, 504], asynchronous=True)
        try:
            histórico = query.history(period=período, interval=intervalo,adj_timezone=True)
        except:
            falhas.append(ticker)
            #print(ticker,"falhou.")
        else:
            histórico = histórico.reset_index()
            if 'date' in histórico.columns: # Ajusta os tempos e salva em dados1
                histórico['date'] = pd.to_datetime(histórico['date'])
                histórico['weekday'] = histórico['date'].dt.weekday # Cria dias da semana
                histórico['weekday'] = padronização(histórico['weekday'])
                histórico['yearday'] = histórico['date'].dt.dayofyear # Cria dias da semana
                histórico['yearday'] = padronização(histórico['yearday'])
                histórico['date'] = histórico['date'].dt.tz_localize(None) # Remove timezone
                histórico['date'] = histórico['date'].dt.date # Remove horário
                histórico = histórico.sort_values('date') # Organiza por data
                
                dados1[ticker] = histórico # Salva tudo em dados1
            else:
                #print(ticker,"não contém datas, mas contém:")
                #print(histórico.columns)
                None

    print(len(dados1),"tickers salvos com sucesso.")
    print(len(falhas),"tickers apresentaram falha.")

    Medidas = []
    for tckr in dados1:
        for col in dados1[tckr].columns:
            if col not in Medidas:
                Medidas.append(col)
                print(col)
    for tckr in dados1:
        for col in Medidas:
            if col not in dados1[tckr].columns:
                dados1[tckr][col] = 0

    # Verifica se a pasta de destino existe, se não, cria-a
    if not os.path.exists('dados'):
        os.makedirs('dados')
    # Itera pelo dicionário e salva cada dataframe como um arquivo CSV
    for tckr, df in dados1.items():
        caminho_arquivo = os.path.join('dados', f'{tckr}.csv')  # Caminho completo para o arquivo CSV
        df.to_csv(caminho_arquivo, index=False)  # Salva o dataframe como arquivo CSV