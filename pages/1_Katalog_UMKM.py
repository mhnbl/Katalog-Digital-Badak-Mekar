import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

# -----------------------------
# Konfigurasi Halaman
# -----------------------------
st.set_page_config(
    page_title="Katalog UMKM",
    layout="wide",
    page_icon="kukar.png"
)

st.title("Katalog UMKM Desa Badak Mekar")

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("UMKM Desa Badak Mekar.csv")
    df.columns = df.columns.str.strip()
    # Ganti nama kolom ke format lebih rapih
    df = df.rename(columns={
        "Nama_Pemilik_Usaha": "Nama Pemilik Usaha",
        "Jenis_Usaha": "Jenis Usaha",
        "No._RT": "No. RT",
        "Alamat": "Alamat",
        "No._HP": "No. HP",
        "Perizinan": "Perizinan"
    })
    return df

df = load_data()

# Format No. RT → string dua digit → RT
df['RT'] = df['No. RT'].fillna(0).astype(int).astype(str).str.zfill(2)
df = df.drop(columns=['No. RT'])

# -----------------------------
# Sidebar Filter
# -----------------------------
st.sidebar.header("🔍 Filter UMKM")
jenis_filter = st.sidebar.multiselect("Jenis Usaha", sorted(df['Jenis Usaha'].unique()))
izin_filter = st.sidebar.multiselect("Status Perizinan", sorted(df['Perizinan'].unique()))
rt_filter = st.sidebar.multiselect("RT", sorted(df['RT'].unique()))

filtered = df.copy()
if jenis_filter:
    filtered = filtered[filtered['Jenis Usaha'].isin(jenis_filter)]
if izin_filter:
    filtered = filtered[filtered['Perizinan'].isin(izin_filter)]
if rt_filter:
    filtered = filtered[filtered['RT'].isin(rt_filter)]

# -----------------------------
# Konfigurasi Tabel AgGrid
# -----------------------------
gb = GridOptionsBuilder.from_dataframe(filtered)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_default_column(
    wrapText=False,
    autoHeight=False,
    resizable=True,
    filter=True,
    sortable=True
)

# Tambahkan checkbox pada kolom pertama
gb.configure_column(filtered.columns[0], checkboxSelection=True, headerCheckboxSelection=True)

# Auto size kolom
for col in filtered.columns:
    gb.configure_column(col, autoSize=True)

grid = gb.build()

response = AgGrid(
    filtered,
    gridOptions=grid,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=450,
    theme="streamlit",
    fit_columns_on_grid_load=True
)

# -----------------------------
# Tombol Download
# -----------------------------
st.download_button(
    label="⬇️ Download Data CSV",
    data=filtered.to_csv(index=False).encode("utf-8"),
    file_name="UMKM_Badak_Mekar_filtered.csv",
    mime="text/csv"
)

# -----------------------------
# Detail UMKM Terpilih
# -----------------------------
selected = pd.DataFrame(response['selected_rows'])
st.subheader("Detail UMKM Yang Terpilih")

if not selected.empty:
    detail = selected.iloc[0]

    nomor = str(detail['No. HP']).replace(" ", "")
    link_wa = f"https://wa.me/{nomor}" if nomor.isdigit() else None

    st.markdown(
        f"""
        <div style="padding: 20px; background-color: rgba(240,240,240,0.85); 
                    border-left: 5px solid #2a9d8f; border-radius: 8px; margin-bottom: 1rem;">
            <p style="margin: 0 0 6px 0; font-size: 16px;"><strong>Nama Pemilik:</strong> {detail['Nama Pemilik Usaha']}</p>
            <p style="margin: 0 0 6px 0;"><strong>Jenis Usaha:</strong> {detail['Jenis Usaha']}</p>
            <p style="margin: 0 0 6px 0;"><strong>Alamat:</strong> {detail['Alamat']} (RT {detail['RT']})</p>
            <p style="margin: 0 0 6px 0;"><strong>No HP:</strong> {detail['No. HP']}</p>
            <p style="margin: 0 0 6px 0;"><strong>Status Perizinan:</strong> {detail['Perizinan']}</p>
            {f'<a href="{link_wa}" target="_blank" style="text-decoration:none;"><button style="margin-top:10px; background-color:#25D366; color:white; padding:8px 12px; border:none; border-radius:4px;">Hubungi via WhatsApp</button></a>' if link_wa else ''}
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.info("Klik salah satu baris pada tabel di atas untuk melihat detail UMKM.")

