import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Beranda - UMKM Badak Mekar", 
    layout="wide",
    page_icon="kukar.png"
)

# ------------------------
# 🔰 HEADER DENGAN LOGO
# ------------------------
col1, col2, col3 = st.columns([1, 6, 1])

with col1:
    st.image("kukar.png", width=400)

with col2:
    st.markdown(
        """
        <h1 style='text-align: center; font-size: 38px; margin-bottom: 0;'>Katalog Digital UMKM Desa Badak Mekar</h1>
        <h4 style='text-align: center;font-size: 18px; color: gray; margin-top: 0;'>Program Kerja Individu KKN Bina Desa Universitas Mulawarman 2025</h4>
        """, 
        unsafe_allow_html=True
    )

with col3:
    st.image("unmul.png", width=400)

st.markdown("---")

# ------------------------
# 📦 LOAD DATA
# ------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("UMKM Desa Badak Mekar.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

# ------------------------
# 🧭 INTRO & STATS
# ------------------------

# 💡 CSS Transparan Abu-Abu
st.markdown("""
    <style>
    .info-box {
        height: 150px;
        padding: 20px;
        border-radius: 10px;
        background-color: rgba(240, 240, 240, 0.8); /* transparan abu-abu terang */
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: black;
    }
    .info-box h2, .info-box h3, .info-box h4 {
        margin: 0;
        line-height: 0.2;
    }
    .info-box p {
        margin: 4px 0 0 0;
        color: #444;
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        f"""
        <div class='info-box'>
            <h4>Total UMKM Terdata</h4>
            <h2 style='color: #264653;'>{len(df)}</h2>
            <p>UMKM aktif di desa</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    most_common = df['Jenis_Usaha'].value_counts().idxmax()
    count_common = df['Jenis_Usaha'].value_counts().max()
    st.markdown(
        f"""
        <div class='info-box'>
            <h4>Jenis Usaha Terbanyak</h4>
            <h3 style='color: #e76f51;'>{most_common}</h3>
            <p>{count_common} pelaku usaha</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    total_rt = df["No._RT"].nunique()
    st.markdown(
        f"""
        <div class='info-box'>
            <h4>RT Aktif UMKM</h4>
            <h2 style='color: #2a9d8f;'>{total_rt} RT</h2>
            <p>memiliki pelaku UMKM</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ------------------------
# 📝 PENJELASAN WEBSITE
# ------------------------
st.markdown(
    """
    <div style="padding: 20px; background-color: rgba(245, 245, 245, 0.8); border-left: 5px solid #264653; border-radius: 6px; margin-top: 10px;">
        <p style="margin: 0 0 10px 0; font-size: 15px;color: black;">
        Website ini merupakan hasil dari program kerja <strong>Kuliah Kerja Nyata (KKN)</strong> dengan fokus pada <strong>digitalisasi data UMKM lokal</strong> di Desa Badak Mekar. Tujuan utamanya adalah menyusun dan menyajikan informasi pelaku usaha mikro secara lebih tertata, interaktif, dan mudah diakses oleh semua pihak yang berkepentingan.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <div style="padding: 20px; background-color: rgba(245, 245, 245, 0.8); border-left: 5px solid #264653; border-radius: 6px; margin-top: 10px;">
        <p style="color: black;font-size: 15px; margin-bottom: 5px;"><strong>Melalui platform ini, Anda dapat menemukan:</strong></p>
        <ul style="color: black; font-size: 15px; padding-left: 20px; margin-top: 0;">
            <li>Data lengkap UMKM seperti nama pemilik usaha, jenis usaha, alamat, no.telepon, dan status perizinan</li>
            <li>Visualisasi statistik guna menadapatkan gambaran dan insight tentang kondisi umkm di wilayah desa</li>
            <li>Fitur pencarian dan penyaringan berdasarkan kategori tertentu</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="padding: 20px; background-color: rgba(245, 245, 245, 0.8); border-left: 5px solid #264653; border-radius: 6px; margin-top: 10px;">
        <p style="color: black;margin-top: 10px; font-size: 14px; color: #666;">
        Informasi yang disediakan ditujukan untuk membantu pemerintah desa, pelaku usaha, dan masyarakat umum dalam <strong>perencanaan pengembangan ekonomi lokal</strong> berbasis data. Harapannya, sistem ini dapat menjadi langkah awal menuju desa yang lebih <em>informatif</em>, <em>inovatif</em>, dan <em>berdaya saing</em>.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
# ------------------------
# 📈 VISUALISASI
# ------------------------
st.subheader("Visualisasi Ringkas")

col1, col2 = st.columns(2)

with col1:
    df['RT'] = df['No._RT'].astype(str)
    rt_chart = df['RT'].value_counts().reset_index()
    rt_chart.columns = ['RT', 'Jumlah']
    fig_rt = px.pie(
        rt_chart, names='RT', values='Jumlah',
        title="Distribusi UMKM per RT",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Blues
    )
    fig_rt.update_traces(textinfo='percent+label', textposition='inside')
    st.plotly_chart(fig_rt, use_container_width=True)

with col2:
    jenis_chart = df['Jenis_Usaha'].value_counts().reset_index()
    jenis_chart.columns = ['Jenis_Usaha', 'Jumlah']
    fig_jenis = px.pie(
        jenis_chart, names='Jenis_Usaha', values='Jumlah',
        title="Distribusi UMKM per Jenis Usaha",
        hole=0.3,
        color_discrete_sequence=px.colors.sequential.Aggrnyl
    )
    fig_jenis.update_traces(textinfo='none')
    st.plotly_chart(fig_jenis, use_container_width=True)


st.markdown("---")
st.caption("© 2025 Katalog Digital UMKM - Desa Badak Mekar | Mahasiswa Universitas Mulawarman")
