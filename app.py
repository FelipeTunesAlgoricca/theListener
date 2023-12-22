from textblob import TextBlob
import requests
import pandas as pd

# Função para realizar a busca no Google Custom Search
def buscar_google(api_key, cse_id, query, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': num
    }
    response = requests.get(url, params=params)
    return response.json()

# Função para analisar o sentimento de um texto
def analisar_sentimento(texto):
    return TextBlob(texto).sentiment

# Função para tentar classificar o tipo de site
def classificar_site(url):
    if 'noticias' in url or 'news' in url:
        return 'Notícias'
    elif 'blog' in url:
        return 'Blog'
    elif 'gov' in url:
        return 'Governo'
    elif 'edu' in url:
        return 'Educativo'
    else:
        return 'Outro'

# Substitua pelas suas chaves de API e CSE
api_key = 'AIzaSyAw9ZoaiuKW-3jA1WjbS6yKn8NcOyMHJxA'
cse_id = '5423e72690868452f'

# Lista com os nomes dos três políticos
politicos = ['lula', 'bolsonaro']

# Lista para armazenar os dados coletados
dados_coletados = []

# Busca e análise de sentimentos
for politico in politicos:
    resultados = buscar_google(api_key, cse_id, politico)
    for item in resultados.get('items', []):
        analise = analisar_sentimento(item['snippet'])
        tipo_site = classificar_site(item['link'])
        dados_coletados.append({
            'Político': politico,
            'Sentimento': analise.polarity,
            'Subjetividade': analise.subjectivity,
            'Snippet': item['snippet'],
            'Título': item['title'],
            'Link': item['link'],
            'Tipo de Site': tipo_site
        })

# Cria um DataFrame com os dados
df_dados = pd.DataFrame(dados_coletados)

# Exibe os resultados
print(df_dados)

# Calcula a média de sentimento para cada político e exibe
df_media_sentimentos = df_dados.groupby(['Político', 'Tipo de Site'])['Sentimento'].mean().reset_index()
print(df_media_sentimentos)
