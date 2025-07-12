import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Statistik UMKM", layout="wide",page_icon="kukar.png")
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

    with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')

    #
    perizinan_chart = df.groupby(['Jenis_Usaha', 'Perizinan']).size().reset_index(name='Jumlah')
    fig = px.bar(perizinan_chart, x='Jenis_Usaha', y='Jumlah', color='Perizinan',
                barmode='group', title="Status Perizinan per Jenis Usaha")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')
     
        
with col2:
    st.header("Perizinan UMKM")
    fig2 = px.pie(df, names='Perizinan',
                  hole=0.4, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')
     
     # Tambahkan kolom status kontak
    df['Kontak'] = df['No._HP'].apply(lambda x: 'Ada Kontak' if str(x).strip() not in ['-', '', 'nan'] else 'Tidak Ada')

    # Buat pie chart
    fig_kontak = px.pie(
        df,
        names='Kontak',
        title="Status Ketersediaan Nomor Kontak UMKM",
        color_discrete_sequence=px.colors.sequential.RdBu,
        hole=0.4
    )
    st.plotly_chart(fig_kontak, use_container_width=True)
    with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')
     

st.header("Jumlah UMKM per RT")
rt_count = df['RT'].value_counts().reset_index()
rt_count.columns = ['RT', 'Jumlah']
fig3 = px.bar(rt_count, x='RT', y='Jumlah', color='RT', color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')
    
df['Ada_Kontak'] = df['No._HP'].apply(lambda x: "Ada" if str(x).strip() not in ["-", "", "nan"] else "Tidak")
summary = df.groupby('RT').agg(
    Total=('Nama_Pemilik_Usaha', 'count'),
    Berizin=('Perizinan', lambda x: (x == 'ADA').sum()),
    Ada_Kontak=('Ada_Kontak', lambda x: (x == 'Ada').sum())
).reset_index()

fig = px.bar(summary, x='RT', y=['Total', 'Berizin', 'Ada_Kontak'],
             barmode='group', title="Komparasi UMKM per RT")
st.plotly_chart(fig, use_container_width=True)
with st.expander("See Explanation"):
            st.write('Dari diagram lingkaran diatas, dapat dilihat:')
            st.write('Lorem ipsum dolor sit amet consectetur adipiscing elit quisque faucibus ex sapien vitae pellentesque sem placerat in id cursus mi pretium tellus duis convallis tempus leo eu aenean sed diam urna tempor pulvinar vivamus fringilla lacus nec metus bibendum egestas.')
     