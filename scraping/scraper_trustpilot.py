import pandas as pd
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
 
 

def obtener_url_empresa(empresa):
    # Indicamos que no se abra el navegador al ejecutar el script
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1980,1020")
    options.add_argument("--headless")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    browser = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options= options)
    # Ponemos pantalla completa
    browser.maximize_window()
    # Iniciamos el navegador y abrimos la página de trustpilot
    browser.get('https://www.trustpilot.com/')
    # Aceptamos cookies
    cookies_button = browser.find_element(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler')
    cookies_button.click()
    # Buscamos empresa
    search_text = (browser
        .find_element(By.CSS_SELECTOR,"input[name='query'][type='search']"))
    search_text.click()
    search_text.clear()
    search_text.send_keys(empresa)
    # Clicamos el primer resultado
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.styles_wrapper__08YQY > a"))).click()
    url = browser.find_element(By.CSS_SELECTOR, "div.styles_wrapper__08YQY > a").get_attribute('href')
    return url


def scrapeamos_comentarios(url_empresa):
    web_page = requests.get(url_empresa).text
    soup = BeautifulSoup(web_page, "html.parser")

    titulos = []
    descripciones = []
    ratings = []
    paises = []
    fechas = []

    # Iteramos cada comentario
    for comentario in soup.find_all(class_ = "styles_cardWrapper__LcCPA styles_show__HUXRb styles_reviewCard__9HxJJ"):
        # Titulo
        titulo = comentario.find(class_ = "typography_heading-s__f7029 typography_appearance-default__AAY17").text
        titulos.append(titulo)
        # Descripcion (algunos comentarios pueden no tener descripciiones)
        try:
            descripcion = comentario.find(class_ = "typography_body-l__KUYFJ typography_appearance-default__AAY17 typography_color-black__5LYEn").text
            descripciones.append(descripcion)
        except:
            descripciones.append('')
            pass
        # Ratings
        rating = comentario.find(class_ = "styles_reviewHeader__iU9Px").get('data-service-review-rating')
        ratings.append(int(rating))
        # Pais
        pais = comentario.find(class_ = "typography_body-m__xgxZ_ typography_appearance-subtle__8_H2l styles_detailsIcon__Fo_ua").text
        paises.append(pais)
        # Fecha
        fecha = comentario.find(class_ = "typography_body-m__xgxZ_ typography_appearance-default__AAY17 typography_color-black__5LYEn").text
        fechas.append(fecha.split('Date of experience: ')[1])
    return pd.DataFrame({'Fecha':fechas, 'Título': titulos, 'Descripción': descripciones, 'Rating': ratings, 'Fuente': 'Trustpilot' ,'País': paises, 'Estado USA': ''})

def scrapeamos_numero_paginas(url_empresa):
    web_page = requests.get(url_empresa).text
    soup = BeautifulSoup(web_page, "html.parser")
    return int(soup.find(class_ = 'pagination_pagination___F1qS').get_text(separator = ',').split(',')[-2])


def trust_pilot_reviews_scraping(empresa, n_paginas):
    trust_pilot_df = pd.DataFrame()
    url_pagina = obtener_url_empresa(empresa)
    pagina = 1
    while pagina <= n_paginas and pagina <= scrapeamos_numero_paginas(url_pagina):
        trust_pilot_df = pd.concat([trust_pilot_df, scrapeamos_comentarios(url_pagina + f'?page={pagina}')])
        # trust_pilot_df['Fecha'] = pd.to_datetime(trust_pilot_df['Fecha'], infer_datetime_format=True)
        pagina += 1

    return trust_pilot_df










