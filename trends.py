from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk

# Baixar as stopwords em português
nltk.download('stopwords')
from nltk.corpus import stopwords
stopwords_pt = set(stopwords.words('portuguese'))

# Função para realizar a busca no Google Custom Search
def buscar_google(api_key, cse_id, query, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cse_id,
        'q': query,
        'num': num
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Irá disparar uma exceção para respostas não-200
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

# Função para analisar o sentimento de um texto
def analisar_sentimento(texto):
    blob = TextBlob(texto, analyzer=NaiveBayesAnalyzer())
    return blob.sentiment

# Função para gerar a nuvem de palavras
def gerar_nuvem_de_palavras(textos, titulo):
    texto_unificado = ' '.join(textos).lower()
    texto_unificado = ''.join([char for char in texto_unificado if char.isalpha() or char.isspace()])
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords_pt).generate(texto_unificado)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(titulo)
    plt.show()

# Substitua pelas suas chaves de API e CSE
api_key = 'AIzaSyAw9ZoaiuKW-3jA1WjbS6yKn8NcOyMHJxA'
cse_id = '5423e72690868452f'

# Lista com os nomes dos três políticos
politicos = ['biden', ' hilary clinton', 'trump']

# Lista para armazenar os sentimentos e outros dados
dados_coletados = []

# Busca e análise de sentimentos
for politico in politicos:
    resultados = buscar_google(api_key, cse_id, politico)
    if resultados:
        textos_para_nuvem = []
        for item in resultados.get('items', []):
            analise = analisar_sentimento(item['snippet'])
            dados_coletados.append({
                'Político': politico,
                'Sentimento': analise.classification,
                'Subjetividade': analise.p_pos - analise.p_neg,
                'Snippet': item['snippet'],
                'Título': item['title'],
                'Link': item['link']
            })
            textos_para_nuvem.append(item['snippet'])

        # Geração da nuvem de palavras para cada político
        gerar_nuvem_de_palavras(textos_para_nuvem, f'Palavras Mais Usadas: {politico}')

# Cria um DataFrame com os dados
df_sentimentos = pd.DataFrame(dados_coletados)

# Exibe os resultados
print(df_sentimentos)

# Calcula a média de sentimento para cada político e exibe
# Isso foi alterado para refletir o sentimento como classificação em vez de polaridade
df_media_sentimentos = df_sentimentos.groupby('Político').apply(
    lambda x: pd.Series({
        'Sentimento_Pos': (x['Sentimento'] == 'pos').mean(),
        'Sentimento_Neg': (x['Sentimento'] == 'neg').mean()
    })
).reset_index()

print(df_media_sentimentos)

# Criação do gráfico de barras para a média dos sentimentos
plt.figure(figsize=(10, 5))
plt.bar(df_media_sentimentos['Político'], df_media_sentimentos['Sentimento_Pos'], label='Positivo', alpha=0.6)
plt.bar(df_media_sentimentos['Político'], df_media_sentimentos['Sentimento_Neg'], label='Negativo', alpha=0.6, bottom=df_media_sentimentos['Sentimento_Pos'])
plt.xlabel('Político')
plt.ylabel('Média de Sentimento')
plt.title('Média de Sentimento por Político')
plt.legend()
plt.show()
