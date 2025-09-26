import pandas as pd
import streamlit as st

@st.cache_data
def carregar_dados():
    # Carregar arquivo excel
    # df = pd.read_excel('./Furto_2009-a-2024.xlsx')
    
    # Criar arquivo csv filtrado para furtos apenas em fortaleza

    # df = df[df['Município'] == 'Fortaleza']
    # df.to_csv('Furto_2009-a-2024-Fortaleza.csv', index=False)

    df = pd.read_csv('./Furto_2009-a-2024-Fortaleza.csv')
    
    # Definindo as AIS de Fortaleza para retirar AIS não identificadas do conjunto de dados
    AIS_fortaleza = ['AIS 01', 'AIS 02', 'AIS 03', 'AIS 04', 'AIS 05', 'AIS 06', 'AIS 07', 'AIS 08', 'AIS 09', 'AIS 10']

    # Filtrando com base nas AIS definidas 
    df = df[df.AIS.isin(AIS_fortaleza)]
    
    df['Data'] = pd.to_datetime(df['Data'])
    df['Ano'] = df['Data'].dt.year
    df['Mês'] = df['Data'].dt.month

    return df