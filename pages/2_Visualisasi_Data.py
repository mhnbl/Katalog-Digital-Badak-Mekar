import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistik UMKM", layout="wide")
st.title("Statistik & Visualisasi UMKM")

@st.cache_data
def load_data():
    df = pd.read_csv("UMKM Desa Badak Mekar.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()
df['RT'] = df['No._RT'].astype(str)

col1, col2 = st.columns(2)

with col1:
    st.header("Jumlah UMKM per Jenis Usaha")
    jenis_df = df['Jenis_Usaha'].value_counts().reset_index()
    jenis_df.columns = ['Jenis_Usaha', 'Jumlah']
    fig1 = px.bar(jenis_df,
                  x='Jenis_Usaha', y='Jumlah',
                  labels={'Jenis_Usaha': 'Jenis Usaha', 'Jumlah': 'Jumlah'},
                  color_discrete_sequence=['#4a90e2'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.header("Perizinan UMKM")
    fig2 = px.pie(df, names='Perizinan', title="Status Perizinan",
                  hole=0.4, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig2, use_container_width=True)

st.header("Jumlah UMKM per RT")
rt_count = df['RT'].value_counts().reset_index()
rt_count.columns = ['RT', 'Jumlah']
fig3 = px.bar(rt_count, x='RT', y='Jumlah', color='RT', color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig3, use_container_width=True)
