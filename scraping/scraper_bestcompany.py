import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
from datetime import timedelta

def obtener_url_empresa(empresa):
    # Indicamos que no se abra el navegador al ejecutar el script
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    # Iniciamos el navegador y abrimos la página de trustpilot
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options=options)
    browser.get('https://bestcompany.com/')
    # Buscamos empresa
    search_text = browser.find_element(By.CSS_SELECTOR, "#home-search")
    search_text.click()
    search_text.clear()
    search_text.send_keys(empresa)
    # Clicamos el primer resultado
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[class='px-3 py-2 Text-2 border-b block hover:bg-gray-100 bg-gray-100']"))).click()
    return browser.current_url


def scrapeamos_comentarios(url_empresa):
    request = requests.get(url_empresa)
    soup = BeautifulSoup(request.text, 'html.parser')

    titulos = []
    descripciones = []
    ratings = []
    estados_usa = []
    fechas = []

    # Iteramos cada comentario
    for comentario in soup.find_all('div', {'class' : 'w-full mb-4'}):
        # Descripcion
        descripcion = comentario.select('div.whitespace-pre-line.break-words')[0].text
        descripciones.append(descripcion)
        # Rating 
        rating = 5 -comentario.select('div.flex.items-center.justify-center.mr-2')[0].text.count("border")
        ratings.append(rating)
        # Titulo
        titulos.append(' '.join(descripcion.split()[:5]))

        # Estado USA (Algunos comentarios pueden no tener Estado USA)
        try:
            estado_usa = comentario.select('span.text-text-secondary')[0].text.rstrip()[-2:]
            estados_usa.append(estado_usa)
        except:
            estados_usa.append('')
            pass
        # Fechas (Sigue el formato 'Hace x días/semanas/años)
        fecha_origen = comentario.select('p.Body-2.text-text-secondary')[0].text.lstrip().rstrip().split(' ')
        if 'week' in fecha_origen[1]:
            fechas.append(datetime.now().date() - timedelta(days = 7 * int(fecha_origen[0])))
        elif 'month' in fecha_origen[1]:
            fechas.append(datetime.now().date() - timedelta(days = 31 * int(fecha_origen[0])))
        else:
            fechas.append(datetime.now().date() - timedelta(days = 365 * int(fecha_origen[0])))

    return pd.DataFrame({'Fecha':fechas, 'Título': titulos, 'Descripción': descripciones, 'Rating': ratings, 'Fuente': 'Bestcompany' ,'País': '', 'Estado USA': estados_usa})


def scrapeamos_numero_paginas(url_empresa):
    web_page = requests.get(url_empresa).text
    soup = BeautifulSoup(web_page, "html.parser")
    try: 
        return int(soup.find_all('a')[-30].text.lstrip().rstrip())
    except:
        return 1


def bestcompany_reviews_scraping(empresa, n_paginas):
    bestcompany_df = pd.DataFrame()
    url_pagina = obtener_url_empresa(empresa)
    pagina = 1
    while pagina <= n_paginas and pagina <= scrapeamos_numero_paginas(url_pagina):
        bestcompany_df = pd.concat([bestcompany_df, scrapeamos_comentarios(url_pagina + f'?page={pagina}')])
        pagina += 1

    return bestcompany_df



