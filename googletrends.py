from pytrends.request import TrendReq
import time
import json

# Carregar configurações do arquivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Inicializar o objeto pytrends com configurações carregadas
pytrends = TrendReq(hl=config['hl'], tz=config['tz'], timeout=tuple(config['timeout']))

for keyword in config['keywords']:
    attempt = 0
    success = False
    while not success and attempt < 5:  # Tentar até 5 vezes
        try:
            # Construir a carga de trabalho com a palavra-chave e configurações
            pytrends.build_payload(kw_list=[keyword], timeframe=config['timeframe'], geo=config['geo'])

            # Obter consultas relacionadas
            related_queries_dict = pytrends.related_queries()
            top_queries = related_queries_dict[keyword]['top']
            rising_queries = related_queries_dict[keyword]['rising']

            # Imprimir consultas relacionadas
            print(f"Principais consultas relacionadas a {keyword}:")
            print(top_queries)
            print(f"\nConsultas em ascensão relacionadas a {keyword}:")
            print(rising_queries)

            # Obter interesse por região
            interest_by_region_df = pytrends.interest_by_region()
            print(f"\nInteresse por região para '{keyword}':")
            print(interest_by_region_df)

            success = True  # Se tudo der certo, defina sucesso como verdadeiro

        except Exception as e:
            # Verificar se o erro é um erro 429 (muitas solicitações)
            if '429' in str(e):
                attempt += 1
                delay = config['base_delay'] * (2 ** attempt)  # Backoff exponencial
                print(f"Erro 429, tentando novamente após {delay} segundos.")
                time.sleep(delay)  # Esperar antes de tentar novamente
            else:
                raise e  # Se for outro erro, levantar exceção
