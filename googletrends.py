from pytrends.request import TrendReq
import time
import json
import pandas as pd

# Carregar configurações do arquivo JSON
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Inicializar o objeto pytrends com configurações carregadas
pytrends = TrendReq(hl=config['hl'], tz=config['tz'], timeout=tuple(config['timeout']))

# Estrutura para armazenar todos os dados
all_data = []
all_data_df = pd.DataFrame()

for keyword in config['keywords']:
    attempt = 0
    success = False
    while not success and attempt < 5:  # Tentar até 5 vezes
        try:
            pytrends.build_payload(kw_list=[keyword], timeframe=config['timeframe'], geo=config['geo'])

            # Obter consultas relacionadas e interesse por região
            related_queries_dict = pytrends.related_queries()
            interest_by_region_df = pytrends.interest_by_region()

            # Processar dados de consultas relacionadas
            top_queries_df = pd.DataFrame(related_queries_dict[keyword]['top'])
            rising_queries_df = pd.DataFrame(related_queries_dict[keyword]['rising'])

            # Imprimir consultas relacionadas
            print(f"Principais consultas relacionadas a {keyword}:")
            print(top_queries_df)
            print(f"\nConsultas em ascensão relacionadas a {keyword}:")
            print(rising_queries_df)

            # Obter interesse por região
            interest_by_region_df = pytrends.interest_by_region()
            print(f"\nInteresse por região para '{keyword}':")
            print(interest_by_region_df)


            # Adicionar ao DataFrame geral
            if not top_queries_df.empty:
                top_queries_df['keyword'] = keyword
                top_queries_df['type'] = 'top'
                all_data_df = pd.concat([all_data_df, top_queries_df])

            if not rising_queries_df.empty:
                rising_queries_df['keyword'] = keyword
                rising_queries_df['type'] = 'rising'
                all_data_df = pd.concat([all_data_df, rising_queries_df])

            # Adicionar ao array para JSON
            all_data.append({
                'keyword': keyword,
                'top_queries': related_queries_dict[keyword]['top'],
                'rising_queries': related_queries_dict[keyword]['rising'],
                'interest_by_region': interest_by_region_df.to_dict()
            })

            success = True
        except Exception as e:
            if '429' in str(e):
                attempt += 1
                delay = config['base_delay'] * (2 ** attempt)
                print(f"Erro 429, tentando novamente após {delay} segundos.")
                time.sleep(delay)
            else:
                raise e

# Salvar os dados em um arquivo CSV
csv_filename = f'{keyword}_pytrends_data.csv'
all_data_df.to_csv(csv_filename, index=False)

# Salvar os dados em um arquivo JSON


# Save data to JSON file
json_filename = f'{keyword}_pytrends_data.json'
# Supondo que all_data é uma lista de dicionários
df = pd.DataFrame(all_data)
df.to_json(json_filename, orient='records', lines=True)
print(f"Dados salvos no arquivo {json_filename}")

