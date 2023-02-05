import streamlit as st 
import pandas as pd
import plotly.express as px
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud
from wordcloud import STOPWORDS
import matplotlib.pyplot as plt


def sentimiento(df):
    # Generación de sentimientos
    sid = SentimentIntensityAnalyzer()

    df['Sentimiento'] = df['Descripción'].apply(lambda x: 'Positivo' if sid.polarity_scores(str(x))['compound'] >= 0.5 else 'Negativo')
    df['Keywords'] = df.apply( lambda x: [palabra for palabra in ''.join(str(x['Descripción'])).split() 
                                                    if sid.polarity_scores(palabra)['compound'] >= 0.55] if x['Sentimiento'] == 'Positivo' 
                                                    else [palabra for palabra in ''.join(str(x['Descripción'])).split() 
                                                        if sid.polarity_scores(palabra)['compound'] <= -0.55], 
                                                        axis = 1)


    GraficoTab, NubeTab = st.tabs(["General info", "Sentiment Wordclouds"])

    # Pestaña de gráficos
    with GraficoTab:
        row2_space1, row2_1, row2_space2, row2_2, row2_space3 = st.columns(
                (0.1, 1, 0.1, 1, 0.1)
            )
        # Gráfico de distribución de sentimientos de comentarios
        with row2_1:
            fig = px.pie(title = "Sentiment distribution in comments", data_frame= df, values=df['Sentimiento'].value_counts().values, names=df['Sentimiento'].value_counts().index)
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        # Gráfico de evolución temporal de sentimientos positivos contra negativos
        with row2_2:
            df_ano = df.set_index('Fecha').groupby([pd.Grouper(freq = "Y"), 'Sentimiento']).count()
            df_ano = df_ano.pivot_table(values = 'Rating', index = 'Fecha', columns = 'Sentimiento', aggfunc = 'first').reset_index()  
            df_ano['Ratio'] = df_ano['Positivo'] / df_ano['Negativo']   
            fig = px.line(title = "Evolution of the positive/negative sentiment ratio by year", data_frame = df_ano, x = 'Fecha', y = 'Ratio')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                
    # Pestaña de nube de palabras
    with NubeTab:
        row1_space1, row1_1, row1_space2, row1_2, row1_space3 = st.columns(
                (0.1, 1, 0.1, 1, 0.1)
            )
        # Nube de palabras positivas
        with row1_1:
                st.subheader("Positive word cloud")
                text = df[(df['Sentimiento'] == 'Positivo') & (df['Keywords'].str.len() > 0)]
                text = text['Keywords'].tolist()
                text = [' '.join(i) for i in text]
                text = ' '.join(text).lower()


                wordcloud = WordCloud(stopwords = STOPWORDS,
                            collocations=True, min_word_length = 4, collocation_threshold = 3,
                            background_color= 'White').generate(text)
                plt.figure( figsize=(40,20) )
                plt.imshow(wordcloud, interpolation='bilInear')
                plt.axis('off')
                plt.show()
                st.pyplot()
        # Nube de palabras negativas
        with row1_2:
                st.subheader("Negative word cloud")
                text = df[(df['Sentimiento'] == 'Negativo') & (df['Keywords'].str.len() > 0)]
                text = text['Keywords'].tolist()
                text = [' '.join(i) for i in text]
                text = ' '.join(text).lower()


                wordcloud = WordCloud(stopwords = STOPWORDS,
                            collocations=True, min_word_length = 4, collocation_threshold = 3,
                            background_color= 'White').generate(text)
                plt.figure( figsize=(40,20) )
                plt.imshow(wordcloud, interpolation='bilInear')
                plt.axis('off')
                plt.show()
                st.pyplot()
    





