# Analizando las opiniones de empresas a través de web scraping y streamlit

El objetivo de este proyecto consiste en ofrecer al usuario una manera automática de estudiar las opiniones de internet de una empresa americana específica.
Con ese fin, se han realizado en el trabajo dos partes diferenciadas; web scraping sobre 3 de las páginas más populares de opiniones de empresas en Estados Unidos (trustpilot, bestcompany y consumeraffairs). Pese a que la primera es la que tiene con diferencia una base de datos más grande que su competencia, se ha optado por diversificar las fuentes para poder expandir el análisis geográfico y añadir complejidad al proyecto. Por otro lado, estos datos se han llevado a un dashboard para poder estudiar las opiniones desde diferentes perspectivas como análisis de sentimiento, geográfico, temporal etc.

En el dashboard, se da la alternativa de o bien usar como datos para el análisis diferentes csvs creados anteriormente con el scraping o bien interactuar con el mismo y poder introducir la empresa que quiera el usuario haciéndose el scraping al momento.

En cuanto a las librerías utilizadas, en el caso del web scraping se ha usado selenium y beautifulsoup4 mientras que para el dashboard se ha usado la librería streamlit. 

## Instrucciones de ejecución

Ejecutar `streamlit run streamlit.py` en un entorno virtual creado con las versiones de las librerías de requirements.txt.

