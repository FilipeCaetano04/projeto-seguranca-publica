import streamlit as st
import plotly.express as px

def renderizar_sidebar(df):
    st.sidebar.header('Filtros')
    ano = st.sidebar.slider('Ano:', df['Ano'].min(), df['Ano'].max())
    return ano # Retorna o valor do filtro

def renderizar_grafico_furtos_mes(df_filtrado):
    st.subheader('Furtos por Mês')
    dados_grafico = df_filtrado.groupby('Mês').size().reset_index(name='Total')
    fig = px.bar(dados_grafico, x='Mês', y='Total')
    st.plotly_chart(fig, use_container_width=True)