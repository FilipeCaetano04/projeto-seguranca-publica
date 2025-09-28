import streamlit as st
from analysis import carregar_dados
from ui import renderizar_mapa_calor_ais
from ui import renderizar_sidebar
from ui import renderizar_grafico_furtos_mes
import os

st.set_page_config(layout="wide")
st.title('🚨 Dados sobre a insegurança em Fortaleza')
st.markdown(""" Esse painel tem o intuito de mostrar os dados de insegurança pública da cidade baseando-se somente na quantidade de furtos por Área Integrada de Segurança.""")

caminho_do_csv = './Furto_2009-a-2024-Fortaleza.csv'

# Trecho necessário para evitar atualizações denecessárias ao atualizar o csv
def get_last_mod_time(path):
    try:
        return os.path.getmtime(path)
    except FileNotFoundError:
        return None

# Verifica a data da última modificação, se for diferente, então foi modificado
last_mod_time = get_last_mod_time(caminho_do_csv)

# 1. Carrega os dados mais recentes
if 'last_mod_time' not in st.session_state or st.session_state.last_mod_time != last_mod_time:
    st.toast("Ficheiro de dados modificado! A atualizar...")
    
    carregar_dados.clear()

    st.session_state.df_principal = carregar_dados()
    st.session_state.last_mod_time = last_mod_time
    st.rerun()


# 2. Sidebar
ano_selecionado = renderizar_sidebar(st.session_state.df_principal)

# 3. Aplica os filtros e mostra os resultados
df_filtrado = st.session_state.df_principal[st.session_state.df_principal['Ano'] == ano_selecionado]


# 4. Mapa de calor por AIS
renderizar_mapa_calor_ais(
    df_filtrado,
    "dados/Bairros_de_Fortaleza.geojson",
    "dados/bairro_para_ais.csv"
)

# 5. Gráfico mensal
renderizar_grafico_furtos_mes(df_filtrado)
