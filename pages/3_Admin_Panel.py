import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import hashlib

# --------------------------
# 🔐 Autentikasi Sederhana
# --------------------------
st.set_page_config(page_title="Admin Panel UMKM", layout="wide")
st.title("Admin Panel UMKM")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Ganti username dan password sesuai kebutuhan
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = hash_password("12345")  # Ganti password di sini

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("Login Admin")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == ADMIN_USERNAME and hash_password(password) == ADMIN_PASSWORD_HASH:
            st.session_state.logged_in = True
            st.success("Login berhasil!")
            st.rerun()
        else:
            st.error("Username atau password salah.")
    st.stop()

# --------------------------
# 📦 Load dan Simpan Data
# --------------------------
DATA_FILE = "UMKM Desa Badak Mekar.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# --------------------------
# 📋 Tabel Interaktif CRUD
# --------------------------
st.subheader("Data UMKM (Interaktif)")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single", use_checkbox=True)
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=400,
    theme="streamlit",
    fit_columns_on_grid_load=True
)

selected = pd.DataFrame(grid_response['selected_rows'])

if not selected.empty:
    selected_index = selected.index[0]
    st.markdown("### Edit / Detail UMKM")
    col1, col2 = st.columns(2)

    with col1:
        nama_pemilik = st.text_input("Nama Pemilik", selected.iloc[0]['Nama_Pemilik_Usaha'])
        jenis_usaha = st.text_input("Jenis Usaha", selected.iloc[0]['Jenis_Usaha'])
        alamat = st.text_area("Alamat", selected.iloc[0]['Alamat'])
    with col2:
        no_hp = st.text_input("No HP", selected.iloc[0]['No._HP'])
        perizinan = st.text_input("Perizinan", selected.iloc[0]['Perizinan'])

    if st.button("Simpan Perubahan"):
        df.loc[selected_index, 'Nama_Pemilik'] = nama_pemilik
        df.loc[selected_index, 'Jenis_Usaha'] = jenis_usaha
        df.loc[selected_index, 'Alamat'] = alamat
        df.loc[selected_index, 'No_HP'] = no_hp
        df.loc[selected_index, 'Perizinan'] = perizinan
        save_data(df)
        st.success("Data berhasil diperbarui.")
        st.rerun()

    if st.button("Hapus Data"):
        if st.warning("Yakin ingin menghapus data UMKM ini?"):
            df = df.drop(index=selected_index)
            save_data(df)
            st.success("Data berhasil dihapus.")
            st.rerun()

# --------------------------
# ➕ Tambah UMKM Baru
# --------------------------
st.markdown("---")
st.subheader("Tambah UMKM Baru")

with st.form("tambah_umkm"):
    nama_pemilik = st.text_input("Nama Pemilik")
    jenis_usaha = st.text_input("Jenis Usaha")
    alamat = st.text_area("Alamat")
    no_hp = st.text_input("No HP")
    perizinan = st.text_input("Status Perizinan")
    submitted = st.form_submit_button("Tambah")

    if submitted:
        if nama_pemilik and jenis_usaha and alamat and no_hp:
            new_row = {
                "Nama_Pemilik": nama_pemilik,
                "Jenis_Usaha": jenis_usaha,
                "Alamat": alamat,
                "No_HP": no_hp,
                "Perizinan": perizinan
            }
            df = df.append(new_row, ignore_index=True)
            save_data(df)
            st.success("Data UMKM baru berhasil ditambahkan.")
            st.rerun()
        else:
            st.error("Harap isi semua kolom wajib.")
