import scraping.scraper_bestcompany as scraper_bestcompany
import scraping.scraper_consumeraffairs as scraper_consumeraffairs
import scraping.scraper_trustpilot as scraper_trustpilot
import pandas as pd


def scrapeo_final(empresa, paginas):
    try:
        df_bc = scraper_bestcompany.bestcompany_reviews_scraping(empresa, paginas)
    except:
        df_bc = pd.DataFrame()
        pass
    try:
        df_ca = scraper_consumeraffairs.consumeraffairs_reviews_scraping(empresa, paginas)
    except:
        df_ca = pd.DataFrame()
        pass
    try:
        df_tp = scraper_trustpilot.trust_pilot_reviews_scraping(empresa,paginas)
    except:
        df_tp = pd.DataFrame()
        pass

    df_total = pd.concat([df_bc, df_ca, df_tp])
    df_total['Fecha'] = pd.to_datetime(df_total['Fecha'], infer_datetime_format= True)

    return df_total
