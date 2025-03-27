import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from folium.features import GeoJsonTooltip, GeoJson

st.title("Mapa de Bairros - Salvador")

# Lista de bairros a serem destacados
bairros_destacados = [
    "Mata Escura", "Cajazeiras VIII", "Cajazeiras XI", "Curuzu", "Liberdade", "Ribeira", 
    "Pituba", "Graça", "IAPI", "Pau Miúdo", "Barra", "Lobato", "Plataforma", "Periperi", 
    "Coutos", "São Tomé de Paripe", "Nazaré", "Imbuí", "Stella Maris", "Bomfim", 
    "Rio Vermelho", "Santo Antonio Além do Carmo", "Itapoan", "Mont Serrat", "Ondina"
]

@st.cache_data
def load_geojson(file):
    return gpd.read_file(file)

uploaded_file = st.file_uploader("Carregue um arquivo GeoJSON", type=["geojson"])

if uploaded_file:
    gdf = load_geojson(uploaded_file)

    # Mostrar os nomes das colunas do GeoJSON para referência
    st.subheader("Nomes das Colunas no GeoJSON")
    st.write(gdf.columns.tolist())

    # Mostrar os dados das primeiras 10 linhas
    st.subheader("Amostra dos Dados (Primeiras 10 Linhas)")
    st.write(gdf.head(10))

    # Criar um mapa
    m = folium.Map(location=[-12.9714, -38.5014], zoom_start=12, tiles="OpenStreetMap")

    # Função para definir estilos dos polígonos
    def estilo_poligono(feature):
        nome_bairro = feature["properties"].get("NomeBairro", "")  # Pegando a coluna correta do GeoJSON
        
        if nome_bairro in bairros_destacados:
            return {"fillColor": "yellow", "color": "black", "weight": 2, "fillOpacity": 0.7}
        return {"fillColor": "transparent", "color": "#FF0000", "weight": 1, "fillOpacity": 0.3}
    
    # Função para interatividade ao passar o mouse
    def highlight_function(feature):
        return {"fillColor": "blue", "color": "black", "weight": 3, "fillOpacity": 0.9}

    # Adicionar polígonos ao mapa com interatividade
    geojson = GeoJson(
        gdf,
        style_function=estilo_poligono,
        highlight_function=highlight_function,
        tooltip=GeoJsonTooltip(fields=["NomeBairro"], aliases=["Bairro:"])
    )
    geojson.add_to(m)

    # Renderizar o mapa no Streamlit
    st_folium(m, width=800, height=600, key="mapa_bairros")
