import yahooquery as yq
import os
import pandas as pd
from tqdm import tqdm

def CompleteDownload(tickers, período = '5y', intervalo = '1d', report = False):
    '''
    símbolos: lista, tupla, array unidimensional ou série contendo os tickers das ações
    '''
    dados = {}
    falhas = []

    for ticker in tqdm(tickers):
        yq.Ticker(ticker, backoff_factor=0.1, retry=3, status_forcelist=[404, 429, 500, 502, 503, 504], asynchronous=True)
        try:
            histórico = query.history(period=período, interval=intervalo,adj_timezone=True)
        except:
            falhas.append(ticker)
        else:
            histórico = histórico.reset_index()
            if 'date' in histórico.columns: # Ajusta os tempos e salva em dados
                histórico['date'] = pd.to_datetime(histórico['date'])
                histórico['weekday'] = histórico['date'].dt.weekday # Cria dias da semana
                histórico['weekday'] = padronização(histórico['weekday'])
                histórico['yearday'] = histórico['date'].dt.dayofyear # Cria dias da semana
                histórico['yearday'] = padronização(histórico['yearday'])
                histórico['date'] = histórico['date'].dt.tz_localize(None) # Remove timezone
                histórico['date'] = histórico['date'].dt.date # Remove horário
                histórico = histórico.sort_values('date') # Organiza por data
                
                dados[ticker] = histórico # Salva tudo em dados
            else:
                #print(ticker,"não contém datas, mas contém:")
                #print(histórico.columns)
                None

    print(len(dados),"tickers salvos com sucesso.") if report else None
    print(len(falhas),"tickers apresentaram falha.") if report else None

    Medidas = []
    print('  Colunas:') if report else None
    for tckr in dados:
        for col in dados[tckr].columns:
            if col not in Medidas:
                Medidas.append(col)
                print(col) if report else None
    for tckr in dados:
        for col in Medidas:
            if col not in dados[tckr].columns:
                dados[tckr][col] = 0

    # Verifica se a pasta de destino existe, se não, cria-a
    if not os.path.exists('dados_yq'):
        os.makedirs('dados_yq')
    # Itera pelo dicionário e salva cada dataframe como um arquivo CSV
    for tckr, df in dados.items():
        caminho_arquivo = os.path.join('dados', f'{tckr}.csv')  # Caminho completo para o arquivo CSV
        df.to_csv(caminho_arquivo, index=False)  # Salva o dataframe como arquivo CSV