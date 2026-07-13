import streamlit as st
import pandas as pd
import plotly.express as px
import glob
import os

st.set_page_config(page_title="Dashboard SEFA-PR Completo", layout="wide")

# Função para carregar e tratar todos os arquivos
@st.cache_data
def carregar_dados():
    # Encontra todos os arquivos que começam com 'receitas'
    arquivos = glob.glob("receitas*.csv")
    lista_dfs = []
    
    for arquivo in arquivos:
        # Extrai o ano do nome do arquivo (assume formato 'receitas2017.csv')
        ano = "".join(filter(str.isdigit, arquivo))
        
        df = pd.read_csv(arquivo, skiprows=1, names=['Mes', 'Grupo', 'Valor'])
        df['Ano'] = ano  # Adiciona uma coluna de ano
        lista_dfs.append(df)
        
    df_final = pd.concat(lista_dfs)
    
    # Tratamento de dados
    df_final['Valor'] = df_final['Valor'].astype(str).str.replace('R$ ', '', regex=False)
    df_final['Valor'] = df_final['Valor'].str.replace('.', '', regex=False)
    df_final['Valor'] = df_final['Valor'].str.replace(',', '.', regex=False)
    df_final['Valor'] = pd.to_numeric(df_final['Valor'], errors='coerce')
    df_final['Mes'] = df_final['Mes'].ffill()
    
    return df_final

df = carregar_dados()

# Dashboard
st.title("Painel de Arrecadação Tributária (2017-2025) - SEFA-PR")

# Filtros
ano_selecionado = st.sidebar.multiselect("Selecione os Anos:", sorted(df['Ano'].unique()), default=df['Ano'].unique())
grupos = st.sidebar.multiselect("Selecione os Grupos:", df['Grupo'].unique(), default=df['Grupo'].unique())

df_filtrado = df[(df['Ano'].isin(ano_selecionado)) & (df['Grupo'].isin(grupos))]

# Visuais
col1, col2 = st.columns(2)

with col1:
    st.subheader("Evolução Temporal")
    fig1 = px.line(df_filtrado.groupby(['Ano', 'Mes'])['Valor'].sum().reset_index(), x='Mes', y='Valor', color='Ano')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Composição por Grupo")
    fig2 = px.pie(df_filtrado, values='Valor', names='Grupo')
    st.plotly_chart(fig2, use_container_width=True)

st.metric("Total Acumulado no Período", f"R$ {df_filtrado['Valor'].sum():,.2f}")
st.dataframe(df_filtrado)