import streamlit as st 
import streamlit_parts.pagina_principal as pagina_principal
import streamlit_parts.pagina_mapa as pagina_mapa
import streamlit_parts.pagina_sentimiento as pagina_sentimiento

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title="Analyzing Company Reviews on the Internet", layout="wide")


menu = st.sidebar.radio(
    "",
    ("Introduction to the data", "Geospatial analysis", "Sentiment analysis")
)

if menu == "Introduction to the data":
    df = pagina_principal.principal()
    st.session_state['dataframe'] = df
if menu == "Geospatial analysis":
    pagina_mapa.pagina_mapa(st.session_state['dataframe'])   
if menu == "Sentiment analysis":
    pagina_sentimiento.sentimiento(st.session_state['dataframe'])


