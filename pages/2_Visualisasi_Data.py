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
        total_jenis = jenis_df["Jumlah"].sum()
        jenis_terbanyak = jenis_df.iloc[0]

        st.markdown(f"""
        Dari diagram batang di atas, dapat disimpulkan hal-hal berikut:

        - Jenis usaha terbanyak adalah **{jenis_terbanyak['Jenis_Usaha']}** sebanyak **{jenis_terbanyak['Jumlah']}** UMKM.
        - Total terdapat **{total_jenis}** UMKM yang dikategorikan dalam berbagai jenis usaha.
        - Diagram ini dapat membantu mengidentifikasi sektor usaha dominan di Desa Badak Mekar, yang bisa dijadikan fokus pengembangan atau pendampingan lanjutan.
        """)
    #
    perizinan_chart = df.groupby(['Jenis_Usaha', 'Perizinan']).size().reset_index(name='Jumlah')
    fig = px.bar(perizinan_chart, x='Jenis_Usaha', y='Jumlah', color='Perizinan',
                barmode='group', title="Status Perizinan per Jenis Usaha")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("See Explanation"):
        total_usaha = df.shape[0]
        izin_summary = df.groupby("Perizinan").size().reset_index(name="Jumlah").sort_values("Jumlah", ascending=False)
        
        izin_terbanyak = izin_summary.iloc[0]
        izin_tersedikit = izin_summary.iloc[-1]

        st.markdown(f"""
        Dari diagram batang di atas, dapat disimpulkan:

        - Jenis status perizinan yang paling umum adalah **{izin_terbanyak['Perizinan']}** dengan jumlah **{izin_terbanyak['Jumlah']}** UMKM.
        - Sedangkan yang paling sedikit adalah **{izin_tersedikit['Perizinan']}** sebanyak **{izin_tersedikit['Jumlah']}** UMKM.
        - Total terdapat **{total_usaha}** UMKM yang tersebar dalam berbagai jenis usaha dan status perizinan.
        - Informasi ini dapat digunakan untuk merancang program pendampingan legalitas usaha, khususnya pada usaha-usaha yang belum memiliki izin.
        """)

        
with col2:
    st.header("Perizinan UMKM")
    fig2 = px.pie(df, names='Perizinan',
                  hole=0.4, color_discrete_sequence=px.colors.sequential.Aggrnyl)
    st.plotly_chart(fig2, use_container_width=True)

    with st.expander("See Explanation"):
        perizinan_counts = df['Perizinan'].value_counts()
        total = perizinan_counts.sum()
        ada = perizinan_counts.get("ADA", 0)
        tidak_ada = perizinan_counts.get("TIDAK ADA", 0)

        persen_ada = round((ada / total) * 100, 2) if total else 0
        persen_tidak = round((tidak_ada / total) * 100, 2) if total else 0

        st.write(f"""
        Dari diagram lingkaran di atas, dapat dilihat bahwa:
        
        - Sebanyak **{ada} UMKM** atau **{persen_ada}%** memiliki status **perizinan ADA**.
        - Sebanyak **{tidak_ada} UMKM** atau **{persen_tidak}%** memiliki status **perizinan TIDAK ADA**.
        
        Ini menunjukkan bahwa {persen_tidak}% UMKM di Desa Badak Mekar masih perlu mendapatkan pendampingan terkait legalitas usaha.
        """)

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
        kontak_counts = df['Kontak'].value_counts()
        total = kontak_counts.sum()
        ada = kontak_counts.get("Ada Kontak", 0)
        tidak_ada = kontak_counts.get("Tidak Ada", 0)

        persen_ada = round((ada / total) * 100, 2) if total else 0
        persen_tidak = round((tidak_ada / total) * 100, 2) if total else 0

        st.write(f"""
        Dari diagram lingkaran di atas, dapat dilihat bahwa:

        - Sebanyak **{ada} UMKM** atau **{persen_ada}%** memiliki **nomor kontak yang tercantum**.
        - Sebanyak **{tidak_ada} UMKM** atau **{persen_tidak}%** **belum mencantumkan nomor kontak**.

        Informasi ini penting untuk memudahkan komunikasi, pemasaran, serta koordinasi lebih lanjut dengan pelaku UMKM.
        """)

st.header("Jumlah UMKM per RT")
rt_count = df['RT'].value_counts().reset_index()
rt_count.columns = ['RT', 'Jumlah']
fig3 = px.bar(rt_count, x='RT', y='Jumlah', color='RT', color_discrete_sequence=px.colors.qualitative.Set3)
st.plotly_chart(fig3, use_container_width=True)

with st.expander("See Explanation"):
    rt_sorted = rt_count.sort_values(by='Jumlah', ascending=False).reset_index(drop=True)
    rt_terbanyak = rt_sorted.iloc[0]
    rt_tersedikit = rt_sorted.iloc[-1]

    st.write(f"""
    Dari diagram batang di atas, dapat dilihat bahwa:

    - RT dengan jumlah UMKM terbanyak adalah **RT {rt_terbanyak['RT']}** dengan total **{rt_terbanyak['Jumlah']} UMKM**.
    - RT dengan jumlah UMKM paling sedikit adalah **RT {rt_tersedikit['RT']}** dengan total **{rt_tersedikit['Jumlah']} UMKM**.

    Data ini membantu mengetahui persebaran aktivitas ekonomi di setiap RT, dan dapat digunakan untuk fokus pembinaan atau pengembangan UMKM secara lebih merata.
    """)

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
    rt_terbanyak = summary.loc[summary['Total'].idxmax()]
    rt_berizin_terbanyak = summary.loc[summary['Berizin'].idxmax()]
    rt_kontak_terbanyak = summary.loc[summary['Ada_Kontak'].idxmax()]

    st.write(f"""
    Dari diagram batang di atas, dapat diperoleh beberapa informasi penting:

    - RT dengan jumlah **UMKM terbanyak** adalah **RT {rt_terbanyak['RT']}** sebanyak **{rt_terbanyak['Total']} UMKM**.
    - RT dengan jumlah **UMKM berizin terbanyak** adalah **RT {rt_berizin_terbanyak['RT']}** sebanyak **{rt_berizin_terbanyak['Berizin']} UMKM**.
    - RT dengan **ketersediaan kontak terbanyak** adalah **RT {rt_kontak_terbanyak['RT']}** sebanyak **{rt_kontak_terbanyak['Ada_Kontak']} UMKM**.

    Visualisasi ini membantu memahami sebaran, legalitas, dan aksesibilitas UMKM di setiap RT, yang berguna untuk perencanaan program pendampingan atau intervensi.
    """)
