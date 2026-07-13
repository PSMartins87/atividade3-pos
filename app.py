import streamlit as st
import pandas as pd
import plotly.express as px


st.set_page_config(page_title="Dashboard SEFA-PR", layout="wide")


df = pd.read_csv('receitas.csv', skiprows=1, names=['Mes', 'Grupo', 'Valor'])
df['Valor'] = df['Valor'].str.replace('R$ ', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
df['Valor'] = pd.to_numeric(df['Valor'])
df['Mes'] = df['Mes'].ffill()


st.title("Painel de Arrecadação Tributária - SEFA-PR")
st.markdown("**Fonte:** Portal da Transparência do Estado do Paraná")


grupos = st.multiselect("Selecione os Grupos de Arrecadação:", df['Grupo'].unique(), default=df['Grupo'].unique())
df_filtrado = df[df['Grupo'].isin(grupos)]


col1, col2 = st.columns(2)

with col1:
    st.subheader("Arrecadação Mensal")
    fig1 = px.bar(df_filtrado, x='Mes', y='Valor', color='Grupo')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Composição por Grupo")
    fig2 = px.pie(df_filtrado, values='Valor', names='Grupo')
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Indicadores")
total = df_filtrado['Valor'].sum()
st.metric("Arrecadação Total Selecionada", f"R$ {total:,.2f}")

st.subheader("Tabela de Detalhamento")
st.dataframe(df_filtrado)