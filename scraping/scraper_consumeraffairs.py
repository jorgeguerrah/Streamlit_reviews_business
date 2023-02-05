import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import requests
import re


def obtener_url_empresa(empresa):
    # Indicamos que no se abra el navegador al ejecutar el script
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1980,1020")
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    # Iniciamos el navegador y abrimos la página de trustpilot
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    # Ponemos pantalla completa
    browser.maximize_window()
    browser.get('https://www.consumeraffairs.com/')
    time.sleep(3)
    # Accedemos a búsqueda
    WebDriverWait(browser, 40).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ca-hdr > div > div > nav.ca-hdr__main-nav.ca-hdr__mb-menu > div > button.ca-hdr__srch-icon.ca-hdr__open-srch-icon.js-ca-hdr-open-srch-btn'))).click()
    # Buscamos empresa
    search_text = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#ca-hdr > div > div > div.ca-hdr__srch-box.js-srch-box.h-bg-bfr > form > div > div > div.choices > div.choices__list.choices__list--dropdown.choices__list--search.choices__list--empty > input')))
    search_text.click()
    search_text.clear()
    search_text.send_keys(empresa)
    # Clicamos el primer resultado
    time.sleep(2)
    search_text.send_keys(Keys.ENTER)
    return browser.current_url


def scrapeamos_comentarios(url_empresa):
    web_page = requests.get(url_empresa).text
    soup = BeautifulSoup(web_page, "html.parser")

    titulos = []
    descripciones = []
    ratings = []
    estados_usa = []
    fechas = []

    # Iteramos cada comentario
    for comentario in soup.find_all('div', {'class':'rvw js-rvw'}):
        # Descripcion
        try:
            descripcion = comentario.find('p').find(text = True)
            descripciones.append(descripcion) 
        except:
            descripciones.append('')
            pass
        # Titulo
        titulo = ' '.join(descripcion.split()[:5])
        titulos.append(titulo)
        # Rating
        rating = int(comentario.select('div.rvw__hdr-stat')[0].contents[1]['data-rating'][0])
        ratings.append(rating)
        # Estado USA
        estado_usa = comentario.find('span', {'itemprop' : 'name'}).text
        if 'Other' in estado_usa:
            estados_usa.append('')
        else:
            estados_usa.append(estado_usa.split(', ')[1][:2].upper())
        # Fecha
        fecha = comentario.select('div.rvw-bd span.ca-txt-cpt')[0].text.split(': ')[1]
        fechas.append(fecha)

    return pd.DataFrame({'Fecha':fechas, 'Título': titulos, 'Descripción': descripciones, 'Rating': ratings, 'Fuente': 'Consumeraffairs' ,'País': '', 'Estado USA': estados_usa})


def scrapeamos_numero_paginas(url_empresa):
    web_page = requests.get(url_empresa).text
    soup = BeautifulSoup(web_page, "html.parser")
    url_pagina_final = soup.findAll('a', attrs={"data-uapi-link": "navigation_last_page"})[0]['href']
    return int(re.search(r"\?page=(\d+)#scr", url_pagina_final).group(1))


def consumeraffairs_reviews_scraping(empresa, n_paginas):
    consumer_affairs_df = pd.DataFrame()
    url_pagina = obtener_url_empresa(empresa)
    pagina = 1
    while pagina <= n_paginas and pagina <= scrapeamos_numero_paginas(url_pagina):
        consumer_affairs_df = pd.concat([consumer_affairs_df, scrapeamos_comentarios(url_pagina + f'?page={pagina}')])
        # consumer_affairs_df['Fecha'] = pd.to_datetime(consumer_affairs_df['Fecha'], infer_datetime_format=True)
        pagina += 1

    return consumer_affairs_df




