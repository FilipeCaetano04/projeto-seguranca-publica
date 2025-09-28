import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd
import json
import streamlit as st
import plotly.express as px



def renderizar_mapa_calor_ais(df_furtos, geojson_bairros, csv_bairro_ais):
    st.subheader("📍 Mapa de Insegurança por AIS em Fortaleza")

    # Carregar GeoJSON
    with open(geojson_bairros, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Transformar em GeoDataFrame
    gdf_bairros = gpd.GeoDataFrame.from_features(data["features"])

    # --- DEFINIR CRS ---
    if gdf_bairros.crs is None:
        gdf_bairros = gdf_bairros.set_crs("EPSG:4326")
    gdf_bairros = gdf_bairros.to_crs("EPSG:4326")

    # Carregar CSV de correspondência bairro → AIS
    df_bairro_ais = pd.read_csv(csv_bairro_ais)

    # Limpa espaços e padroniza as colunas de AIS para garantir o merge
    df_furtos['AIS'] = df_furtos['AIS'].str.strip()
    df_bairro_ais['AIS'] = df_bairro_ais['AIS'].str.strip()

    # Juntar GeoJSON com CSV de bairros → AIS
    gdf_bairros = gdf_bairros.merge(
        df_bairro_ais, left_on="Nome", right_on="Bairro", how="left"
    )

    # Agrupar furtos por AIS
    furtos_por_ais = df_furtos.groupby("AIS").size().reset_index(name="Qtd_Furtos")

    # Juntar com o GeoDataFrame
    gdf_bairros = gdf_bairros.merge(furtos_por_ais, on="AIS", how="left")
    gdf_bairros["Qtd_Furtos"] = gdf_bairros["Qtd_Furtos"].fillna(0)

    # 🔧 Converter para tipo adequado (folium às vezes não aceita int64 ou float64)
    gdf_bairros["AIS"] = gdf_bairros["AIS"].astype(str)
    gdf_bairros["Qtd_Furtos"] = gdf_bairros["Qtd_Furtos"].astype(int)

    # 🛠️ Gerar GeoJSON correto com propriedades incluídas
    geojson_data = gdf_bairros.to_json()

    # Criar mapa
    mapa = folium.Map(location=[-3.730451, -38.521802], zoom_start=12)

    # Criar Choropleth
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        data=gdf_bairros,
        columns=["AIS", "Qtd_Furtos"],
        key_on="feature.properties.AIS",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Quantidade de Furtos",
    )
    choropleth.add_to(mapa)

    # Adicionar tooltip
    folium.GeoJson(
        geojson_data,
        tooltip=folium.GeoJsonTooltip(
            fields=["Nome", "AIS", "Qtd_Furtos"],
            aliases=["Bairro:", "AIS:", "Furtos:"],
            localize=True
        )
    ).add_to(mapa)

    # Mostrar no Streamlit
    st_data = st_folium(mapa, width=800, height=600)
    return st_data


def renderizar_sidebar(df):
    st.sidebar.header('Filtros')
    ano = st.sidebar.slider('Ano:', df['Ano'].min(), df['Ano'].max())
    return ano # Retorna o valor do filtro

def renderizar_grafico_furtos_mes(df_filtrado):
    st.subheader('Furtos por Mês')
    dados_grafico = df_filtrado.groupby('Mês').size().reset_index(name='Total')
    fig = px.bar(dados_grafico, x='Mês', y='Total')
    st.plotly_chart(fig, use_container_width=True)