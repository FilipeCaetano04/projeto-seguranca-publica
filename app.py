import streamlit as st
import pandas as pd
import plotly.express as px

# st.set_page_config(
#     page_title='Dashboard de Segurança - CE',
#     page_icon='🚨','
#     layout='wide'
# )

# Decorator garante que os dados não sejam recarregado a cada iteração
# @st.cache_data
def carregar_dados():
    # Carregar arquivo excel
    # df = pd.read_excel('./Furto_2009-a-2024.xlsx')
    # df.to_csv('Furto_2009-a-2024-Fortaleza.csv', index=False)
    # df = df[df['Município'] == 'Fortaleza']

    df = pd.read_csv('./Furto_2009-a-2024-Fortaleza.csv')
    AIS_fortaleza = ['AIS 01', 'AIS 02', 'AIS 03', 'AIS 04', 'AIS 05', 'AIS 06', 'AIS 07', 'AIS 08', 'AIS 09', 'AIS 10']
    df = df[df['AIS'].any(AIS_fortaleza)]
    print(df)

carregar_dados()

