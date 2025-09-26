import streamlit as st
from analysis import *
from ui import *

st.set_page_config(layout="wide")
st.title('🚨 Análise de Furtos no Ceará')

# 1. Carrega os dados (usando a função do analysis.py)
df_principal = carregar_dados()

# 2. Renderiza a interface (usando as funções do ui.py)
ano_selecionado = renderizar_sidebar(df_principal)

# 3. Aplica os filtros e mostra os resultados
df_filtrado = df_principal[df_principal['Ano'] == ano_selecionado]

renderizar_grafico_furtos_mes(df_filtrado)
# ...outras visualizações...