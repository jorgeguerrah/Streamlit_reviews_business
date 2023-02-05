import streamlit as st 
import pandas as pd
import folium
import json
from streamlit_folium import st_folium

def pagina_mapa(df):
    
    USATab, PaisesTab = st.tabs(["USA States", "World countries"])
    # Pestaña de Estados Unidos
    with USATab:
        try:
            row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns((0.1, 1, 0.2, 5, 0.1))
            with row5_1:
                st.subheader("Filter")
                variable_USA_input = st.radio(
                    "Select the USA map variable",
                    ["Number of USA opinions", "Average Ratings USA"]) 
                    
            # Generamos las abreviaturas de los Estados de EEUU
            f = open('streamlit_parts/maps/usa.json')
            data = json.load(f)
            abreviaturas_estado = []

            for i in data['features']:
                abreviaturas_estado.append(i['id'])

            # Preprocesado de datos: filtramos por opiniones que contengan estados y agrupamos por media y número de opiniones
            df_estados_unidos = df.loc[(pd.notnull(df['Estado USA'])) & (df['Estado USA'].isin(abreviaturas_estado)), ['Estado USA', 'Rating']]
            df_estados_unidos = df_estados_unidos.groupby(['Estado USA'], as_index=False).agg(['mean','count']).reset_index()
            df_estados_unidos.columns = df_estados_unidos.columns.droplevel()

            
            variable_USA = 'count' if variable_USA_input == 'Number of USA opinions' else 'mean'
            
            # Generamos el mapa de Estados Unidos
            map = folium.Map(location=[48, -102], zoom_start=3)
            map.choropleth(geo_data='streamlit_parts/maps/usa.json', data=df_estados_unidos,
                        columns=['', variable_USA],
                        key_on='feature.id',
                        fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                        legend_name=variable_USA_input, 
                        )
                
            with row5_2:
                st_folium(map, width = 1210)
                  
        except:
            st.subheader("There is not enough data to generate this map. You can try with other companies by going back to the home screen")
            pass
    
    # Pestaña del mundo
    with PaisesTab:
        try: 
            row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns((0.1, 1, 0.2, 5, 0.1))
            with row5_1:
                st.subheader("Filtro")
                variable_world_input = st.radio(
                    "Select the World map variable",
                    ["Number of World opinions", "Average Ratings World"])
            
            # Pasamos las abreviaturas de 2 dígitos a 3 dígitos con una tabla de equivalencia para que coincida con el ID del fichero json
            equivalencia_siglas_paises = pd.read_html('https://www.iban.com/country-codes')[0]
            equivalencia_siglas_paises = {fila['Alpha-2 code'] : fila['Alpha-3 code'] for indice, fila in equivalencia_siglas_paises.iterrows()}
            df_paises = df.copy()
            df_paises['País'] = df_paises['País'].apply(lambda x: equivalencia_siglas_paises[x])
                
            # Generamos las abreviaturas de los países
            f = open('streamlit_parts/maps/world.json')
            data = json.load(f)
            abreviaturas_paises = []

            for i in data['features']:
                abreviaturas_paises.append(i['id'])
                
                    
            # Preprocesado de datos: filtramos por opiniones que contengan países y agrupamos por media y número de opiniones   
            df_paises = df_paises.loc[(pd.notnull(df_paises['País'])) & (df_paises['País'].isin(abreviaturas_paises)), ['País', 'Rating']]
            df_paises = df_paises.groupby(['País'], as_index = False).agg(['mean','count']).reset_index()
            df_paises.columns = df_paises.columns.droplevel()
            

            variable_mundial = 'count' if variable_world_input == "Number of World opinions" else 'mean'

            map = folium.Map()
            map.choropleth(geo_data='streamlit_parts/maps/world.json', data= df_paises,
                        columns=['', variable_mundial],
                        key_on='feature.id',
                        fill_color='YlGn', fill_opacity=0.7, line_opacity=0.2,
                        legend_name=variable_world_input, 
                        )
                        
            # Generamos el mapa de países
            with row5_2:
                st_folium(map, width = 1210)
                st.warning("WARNING: The world map may take a few seconds to load.")

        except KeyError:
            st.subheader("There is not enough data to generate this map. You can try with other companies by going back to the home screen")
            pass
