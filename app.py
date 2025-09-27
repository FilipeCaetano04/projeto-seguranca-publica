import streamlit as st
from analysis import carregar_dados
from ui import renderizar_mapa_calor_ais
from ui import renderizar_sidebar
from ui import renderizar_grafico_furtos_mes

st.set_page_config(layout="wide")
st.title('🚨 Dados sobre a insegurança em Fortaleza')
st.markdown(""" Esse painel tem o intuito de mostrar os dados de insegurança pública da cidade baseando-se somente na quantidade de furtos por Área Integrada de Segurança.""")

# 1. Carrega os dados
df_principal = carregar_dados()

# 2. Sidebar
ano_selecionado = renderizar_sidebar(df_principal)

# 3. Aplica os filtros e mostra os resultados
df_filtrado = df_principal[df_principal['Ano'] == ano_selecionado]

# 4. Mapa de calor por AIS
renderizar_mapa_calor_ais(
    df_filtrado,
    "dados/Bairros_de_Fortaleza.geojson",
    "dados/bairro_para_ais.csv"
)

# 5. Gráfico mensal
renderizar_grafico_furtos_mes(df_filtrado)


