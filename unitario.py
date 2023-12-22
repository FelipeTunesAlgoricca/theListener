import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords

# Configurações iniciais
nltk.download('stopwords')
stopwords_pt = set(stopwords.words('portuguese'))

# Função para realizar a busca no Google Custom Search com tratamento de exceções
def buscar_google(api_key, cse_id, query, num=10):
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': cse_id,
            'q': query,
            'num': num,
            'lr': 'lang_pt'
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return None

# Função para limpar e normalizar o texto
def limpar_normalizar_texto(texto):
    texto = ' '.join([word.lower() for word in texto.split() if word.isalpha() and word.lower() not in stopwords_pt])
    return texto

# Função para analisar o sentimento de um texto já limpo
def analisar_sentimento(texto):
    return TextBlob(texto).sentiment

# Função para gerar a nuvem de palavras
def gerar_nuvem_de_palavras(textos, titulo):
    texto_unificado = ' '.join(textos)
    wordcloud = WordCloud(width=800, height=400, background_color='white', stopwords=stopwords_pt).generate(texto_unificado)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(titulo)
    plt.show()

# Substitua pelas suas chaves de API e CSE
api_key = 'AIzaSyAw9ZoaiuKW-3jA1WjbS6yKn8NcOyMHJxA'
cse_id = '5423e72690868452f'

# Lista com os nomes dos políticos
politicos = ['corrupção', 'STF', 'governo']

# Lista para armazenar os sentimentos e outros dados
dados_coletados = []

# Coleta de dados e análise de sentimentos
for politico in politicos:
    dados = buscar_google(api_key, cse_id, politico)
    textos_para_nuvem = []
    if dados:
        for item in dados.get('items', []):
            texto_limpo = limpar_normalizar_texto(item['snippet'])
            analise = analisar_sentimento(texto_limpo)
            dados_coletados.append({
                'Político': politico,
                'Sentimento': analise.polarity,
                'Subjetividade': analise.subjectivity,
                'Snippet': item['snippet'],
                'Título': item['title'],
                'Link': item['link']
            })
            textos_para_nuvem.append(texto_limpo)

        # Geração da nuvem de palavras para cada político
        gerar_nuvem_de_palavras(textos_para_nuvem, f'Palavras Mais Usadas: {politico}')

# Cria um DataFrame com os dados
df_sentimentos = pd.DataFrame(dados_coletados)

# Exibe os resultados
print(df_sentimentos)

# Calcula a média de sentimento para cada político e exibe
df_media_sentimentos = df_sentimentos.groupby('Político')['Sentimento'].mean().reset_index()
print(df_media_sentimentos)

# Criação do gráfico de barras para a média dos sentimentos usando seaborn
plt.figure(figsize=(10, 5))
sns.barplot(
    x='Político',
    y='Sentimento',
    data=df_media_sentimentos,
    palette='viridis'
)

plt.figure(figsize=(10, 5))
plt.bar(df_media_sentimentos['Político'], df_media_sentimentos['Sentimento'], color='blue')
plt.xlabel('Político')
plt.ylabel('Média de Sentimento')
plt.title('Média de Sentimento por Político')
plt.show()

# Salvar os dados em um arquivo CSV
df_sentimentos.to_csv('sentimentos_politicos.csv', index=False)
