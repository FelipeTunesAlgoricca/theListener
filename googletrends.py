from pytrends.request import TrendReq
import time

pytrends = TrendReq(hl='pt-BR', tz=360, timeout=(10,25))
keywords = ["gta 6"]
base_delay = 30  # Tempo inicial de espera de 30 segundos

for keyword in keywords:
    attempt = 0
    success = False
    while not success and attempt < 5:  # Tentar até 5 vezes
        try:
            pytrends.build_payload(kw_list=[keyword], timeframe='today 12-m', geo='BR')

            # Obter consultas relacionadas
            related_queries_dict = pytrends.related_queries()
            top_queries = related_queries_dict[keyword]['top']
            rising_queries = related_queries_dict[keyword]['rising']

            print(f"Principais consultas relacionadas a {keyword}:")
            print(top_queries)
            print(f"\nConsultas em ascensão relacionadas a {keyword}:")
            print(rising_queries)

            # Obter interesse por região
            interest_by_region_df = pytrends.interest_by_region()
            print(f"\nInteresse por região para '{keyword}':")
            print(interest_by_region_df)

            success = True
        except Exception as e:
            if '429' in str(e):
                attempt += 1
                delay = base_delay * (2 ** attempt)  # Backoff exponencial
                print(f"Erro 429, tentando novamente após {delay} segundos.")
                time.sleep(delay)
            else:
                raise e
