import streamlit as st 
import pandas as pd
from streamlit_extras import add_vertical_space
import plotly.express as px
import datetime
import scraping.scraper_final as scraper_final




def principal():
    
    ## Título, subtítulo y descripción de la app
    row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3 = st.columns(
    (0.1, 2, 0.2, 1, 0.1)
    )

    row0_1.title("Analyzing Company Reviews on the Internet")
    row0_1.subheader("Web app design based on [tyler richards' goodreads site](https://github.com/tylerjrichards/streamlit_goodreads_app)")

    with row0_2:
        add_vertical_space.add_vertical_space()

    row0_2.subheader(
        "Application for the Open Data and Dynamic Visualization courses in the Big Data Master's Degree at AFI Escuela by Jorge Guerra Hipólito ([Github](https://github.com/jorgeguerrah))"
    )

    row1_spacer1, row1_1, row1_spacer2 = st.columns((0.1, 3.2, 0.1))

    with row1_1:
        st.markdown(
        '''
        Welcome to my website! This application tracks opinions of a company based on different websites specialized in reviews and analyzes the data of the comments,
        including temporal evolution, sentiment analysis and geospatial analysis. In addition, you can interact with the data to study companies according to variables such as date, 
        country or data source.
        '''
        )
        st.markdown(
            '''
            **To start, enter your company here** 👇
            '''
        )

    ## Selección de empresa
    row2_spacer1, row2_1, row2_spacer2 = st.columns((0.1, 3.2, 0.1))
    with row2_1:
        nombre_empresa = st.selectbox(
            "Select one of the default companies",
            (
                "Netflix", "Amazon", "Tesla", "Walmart"
            ), index = 0
        )
        st.markdown("**OR**")
        company_input = st.text_input(
            "Enter the company of your choice:"
        )



        st.warning(
            """
            IMPORTANT: The application scrapes the first option of each search performed. Try to be as specific as possible when entering the company for best results. 
            Also, it is possible that the company you are looking for does not appear in the site's database.
            """
        )

    if not company_input:
        df = pd.read_csv('csv/{}.csv'.format(nombre_empresa.lower()), parse_dates=['Fecha'])
        
    else:
        nombre_empresa = company_input
        df = scraper_final.scrapeo_final(company_input, 5)
        

        

    ResumenTab, TablaTab = st.tabs(["Resumen", "Tabla"])
    # Pestaña de resumen
    with ResumenTab:
        line1_spacer1, line1_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))
        # Título
        with line1_1:
            st.header("Analyzing **{}** reviews".format(nombre_empresa))

        st.write("")
        row3_space1, row3_1, row3_space2, row3_2, row3_space3 = st.columns(
            (0.1, 1, 0.1, 1, 0.1)
        )

        # Primera fila con dos gráficos
        with row3_1:
            st.subheader("Distribution of ratings")
            fig = px.density_heatmap(title="Ratings frequency",data_frame = df, x = 'Rating')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)


        sentimientos_anuales = df.set_index('Fecha').groupby(pd.Grouper(freq = "Y")).mean().reset_index()

        with row3_2:
            st.subheader("Evolution of opinions over time.")
            fig = px.line(title="Average opinion rating by year", color_discrete_sequence=["#9EE6CF"], data_frame = sentimientos_anuales, x = 'Fecha', y = 'Rating')
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)

        add_vertical_space.add_vertical_space()

        line2_spacer1, line2_1, line1_spacer2 = st.columns((0.1, 3.2, 0.1))

        with line2_1:
            st.header("About data sources")


        row4_space1, row4_1, row4_space2, row4_2, row4_space3 = st.columns(
            (0.1, 1, 0.1, 1, 0.1)
        )

        # Segunda fila con dos gráficos
        with row4_1:
            st.subheader("Número de opiniones recogidas en cada página")
            fig = px.histogram(data_frame = df, x = 'Fuente')
            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)

        with row4_2:
            st.subheader("On which page are the best opinions given?")
            fig = px.box(data_frame = df, x = 'Fuente', y = 'Rating')
            st.plotly_chart(fig, theme = 'streamlit', use_container_width = True)
            

    # Pestaña de tabla
    with TablaTab:
        row5_spacer1, row5_1, row5_spacer2, row5_2, row5_spacer3 = st.columns((0.1, 1, 0.2, 5, 0.1))
        # Filtro
        with row5_1:
            st.subheader("Filter")
            rango_rating = st.slider('Rating', 1, 5, (1, 5))
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            fecha_inicial = st.date_input('Initial Date', df['Fecha'].min())
            fecha_final = st.date_input('Final Date', today)
            fuente = st.multiselect('Choose the sources you want to add', ['Trustpilot', 'Bestcompany', 'Consumeraffairs'], ['Trustpilot', 'Bestcompany', 'Consumeraffairs'])

        # Filtrado de tabla según el input
        tabla_filtrada = df[df['Rating'].between(rango_rating[0], rango_rating[1])]
        tabla_filtrada = tabla_filtrada[(tabla_filtrada['Fecha'].dt.strftime('%Y-%m-%d') > fecha_inicial.strftime('%Y-%m-%d')) & (tabla_filtrada['Fecha'].dt.strftime('%Y-%m-%d') < fecha_final.strftime('%Y-%m-%d'))]
        if fuente != 'Todas':
            tabla_filtrada = tabla_filtrada[tabla_filtrada['Fuente'].isin(fuente)]
        
        # Tabla filtrada
        with row5_2:
            st.dataframe(tabla_filtrada.loc[:,['Fecha','Título','Descripción','Rating','Fuente']])
    

    return df
