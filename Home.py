import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Beranda - UMKM Badak Mekar", layout="wide",page_icon="kukar.png")


st.title("Katalog Digital UMKM Desa Badak Mekar")
st.markdown("""
Selamat datang di katalog digital UMKM Desa **Badak Mekar**.  
Website ini menyajikan data UMKM lokal untuk mendukung promosi dan pengembangan ekonomi desa.
""")

@st.cache_data
def load_data():
    df = pd.read_csv("UMKM Desa Badak Mekar.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

st.subheader(f"Total UMKM Terdata: {len(df)} UMKM")
st.page_link("pages/1_Katalog_UMKM.py", label="Lihat Katalog")
# Buat dua kolom untuk dua visualisasi
st.subheader("Visulisasi Data")
col1, col2 = st.columns(2)

with col1:
    df['RT'] = df['No._RT'].astype(str)
    rt_chart = df['RT'].value_counts().reset_index()
    rt_chart.columns = ['RT', 'Jumlah']
    fig_rt = px.pie(rt_chart, names='RT', values='Jumlah',
                    title="Distribusi UMKM per RT",
                    hole=0.3,
                    color_discrete_sequence=px.colors.sequential.Blues)
    fig_rt.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig_rt, use_container_width=True)

with col2:
    jenis_chart = df['Jenis_Usaha'].value_counts().reset_index()
    jenis_chart.columns = ['Jenis_Usaha', 'Jumlah']
    fig_jenis = px.pie(jenis_chart, names='Jenis_Usaha', values='Jumlah',
                    title="Distribusi UMKM per Jenis Usaha",
                    hole=0.3,
                    color_discrete_sequence=px.colors.sequential.Aggrnyl)

    # Tampilkan label hanya di legend (tidak di tengah pie)
    fig_jenis.update_traces(textinfo='none')

    st.plotly_chart(fig_jenis, use_container_width=True)
st.page_link("pages/2_Visualisasi_Data.py", label="Lihat Statistik")
# Jenis usaha terbanyak
most_common = df['Jenis_Usaha'].value_counts().idxmax()
st.success(f"✨ Jenis usaha terbanyak: **{most_common}**")

    
