from textblob import TextBlob
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

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

# Função para gerar a nuvem de palavras
def gerar_nuvem_de_palavras(textos, titulo):
    texto_unificado = ' '.join(textos)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_unificado)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(titulo)
    plt.show()

# Substitua pelas suas chaves de API e CSE
api_key = 'AIzaSyAw9ZoaiuKW-3jA1WjbS6yKn8NcOyMHJxA'
cse_id = '5423e72690868452f'

# Lista com os nomes dos três políticos
politicos = ['lula', 'bolsonaro', 'dilma ']

# Lista para armazenar os sentimentos e outros dados
sentimentos_data = []

# Busca e análise de sentimentos
for politico in politicos:
    resultados = buscar_google(api_key, cse_id, politico)
    textos_para_nuvem = []
    for item in resultados.get('items', []):
        analise = analisar_sentimento(item['snippet'])
        sentimentos_data.append({
            'Político': politico,
            'Sentimento': analise.polarity,
            'Subjetividade': analise.subjectivity,
            'Snippet': item['snippet'],
            'Título': item['title'],
            'Link': item['link']
        })
        textos_para_nuvem.append(item['snippet'])

    # Geração da nuvem de palavras para cada político
    gerar_nuvem_de_palavras(textos_para_nuvem, f'Palavras Mais Usadas: {politico}')

# Cria um DataFrame com os dados
df_sentimentos = pd.DataFrame(sentimentos_data)

# Exibe os resultados
print(df_sentimentos)

# Calcula a média de sentimento para cada político e exibe
df_media_sentimentos = df_sentimentos.groupby('Político')['Sentimento'].mean().reset_index()
print(df_media_sentimentos)

# Criação do gráfico de barras para a média dos sentimentos
plt.figure(figsize=(10, 5))
plt.bar(df_media_sentimentos['Político'], df_media_sentimentos['Sentimento'], color='blue')
plt.xlabel('Político')
plt.ylabel('Média de Sentimento')
plt.title('Média de Sentimento por Político')
plt.show()
