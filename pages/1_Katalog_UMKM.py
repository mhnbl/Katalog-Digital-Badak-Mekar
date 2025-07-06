import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="Katalog UMKM", layout="wide")
st.title("📋 Katalog UMKM Desa Badak Mekar")

@st.cache_data
def load_data():
    df = pd.read_csv("UMKM Desa Badak Mekar.csv")
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

df = load_data()

# Ekstrak RT jadi string
df['RT'] = df['No._RT'].astype(str)

# Sidebar Filter
st.sidebar.header("🔍 Filter UMKM")
jenis_filter = st.sidebar.multiselect("Jenis Usaha", sorted(df['Jenis_Usaha'].unique()))
izin_filter = st.sidebar.multiselect("Status Perizinan", sorted(df['Perizinan'].unique()))
rt_filter = st.sidebar.multiselect("RT", sorted(df['RT'].unique()))

filtered = df.copy()
if jenis_filter:
    filtered = filtered[filtered['Jenis_Usaha'].isin(jenis_filter)]
if izin_filter:
    filtered = filtered[filtered['Perizinan'].isin(izin_filter)]
if rt_filter:
    filtered = filtered[filtered['RT'].isin(rt_filter)]

# Table
gb = GridOptionsBuilder.from_dataframe(filtered)
gb.configure_selection(selection_mode="single", use_checkbox=True)
grid = gb.build()

response = AgGrid(
    filtered,
    gridOptions=grid,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=450,
    theme="streamlit"
)

# Detail UMKM
selected = pd.DataFrame(response['selected_rows'])
st.subheader("Detail UMKM Terpilih")

if not selected.empty:
    detail = selected.iloc[0]
    st.markdown(f"""
    **Nama Pemilik:** {detail['Nama_Pemilik_Usaha']}  
    **Jenis Usaha:** {detail['Jenis_Usaha']}  
    **Alamat:** {detail['Alamat']}  
    **No HP:** {detail['No._HP']}  
    **RT:** {detail['RT']}  
    **Status Perizinan:** {detail['Perizinan']}
    """)
    # Opsional: Tombol kontak
    nomor = str(detail['No._HP']).replace(" ", "")
    if nomor.isdigit():
        link_wa = f"https://wa.me/{nomor}"
        st.markdown(f"[📱 Hubungi via WhatsApp]({link_wa})", unsafe_allow_html=True)
else:
    st.info("Klik salah satu baris untuk melihat detail UMKM.")
