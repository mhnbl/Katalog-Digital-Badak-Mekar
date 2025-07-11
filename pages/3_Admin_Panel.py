import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import hashlib

# --------------------------
# 🔐 Autentikasi Sederhana
# --------------------------
st.set_page_config(page_title="Admin Panel UMKM", layout="wide", page_icon="kukar.png")
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
def load_data(ttl=0, show_spinner=False):
    df = pd.read_csv(DATA_FILE)
    df.columns = df.columns.str.strip()
    df.rename(columns={
        "Nama Pemilik Usaha": "Nama_Pemilik",
        "Jenis Usaha": "Jenis_Usaha",
        "No. RT": "No_RT",
        "Alamat": "Alamat",
        "No. HP": "No_HP",
        "Perizinan": "Perizinan"
    }, inplace=True)

    df["No_RT"] = df["No_RT"].astype(str).str.zfill(2)
    return df

def save_data(df):
    df = df.copy()
    df["No_RT"] = df["No_RT"].astype(str).str.zfill(2)
    df.rename(columns={
        "Nama_Pemilik": "Nama Pemilik Usaha",
        "Jenis_Usaha": "Jenis Usaha",
        "No_RT": "No. RT",
        "Alamat": "Alamat",
        "No_HP": "No. HP",
        "Perizinan": "Perizinan"
    }, inplace=True)
    df.to_csv(DATA_FILE, index=False)

df = load_data()

# 🔍 Deteksi data duplikat berdasarkan kolom penting
duplicates = df[df.duplicated(subset=["Nama_Pemilik", "Jenis_Usaha", "Alamat", "No_HP", "No_RT"], keep=False)]
if not duplicates.empty:
    st.warning("⚠️ Terdapat data duplikat yang mungkin menyulitkan proses edit atau hapus.")

# --------------------------
# 📋 Tabel Interaktif CRUD
# --------------------------
st.subheader("Data UMKM")

# Konfig AG Grid
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_selection(selection_mode="single", use_checkbox=True)
gb.configure_grid_options(domLayout='normal')  # 1-line height
grid_options = gb.build()

grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.SELECTION_CHANGED,
    height=450,
    theme="streamlit",
    fit_columns_on_grid_load=True
)

selected = pd.DataFrame(grid_response['selected_rows'])

# --------------------------
# ✏️ Edit / Hapus
# --------------------------
if not selected.empty:
    selected_row = selected.iloc[0]
    selected_index = df[
        (df["Nama_Pemilik"] == selected_row["Nama_Pemilik"]) &
        (df["Jenis_Usaha"] == selected_row["Jenis_Usaha"]) &
        (df["Alamat"] == selected_row["Alamat"])
    ].index[0]

    st.markdown("### Edit / Detail UMKM")
    col1, col2 = st.columns(2)

    with col1:
        nama_pemilik = st.text_input("Nama Pemilik", selected_row['Nama_Pemilik']).upper()
        jenis_usaha = st.text_input("Jenis Usaha", selected_row['Jenis_Usaha']).upper()
        alamat = st.text_area("Alamat", selected_row['Alamat']).upper()
    with col2:
        no_hp = st.text_input("No HP", selected_row['No_HP']).upper()
        no_rt = st.text_input("No. RT", selected_row['No_RT'])
        perizinan = st.radio("Perizinan", options=["ADA", "TIDAK ADA"], index=0 if selected_row['Perizinan'] == "ADA" else 1)


    if st.button("Simpan Perubahan"):
        updated_row = {
            "Nama_Pemilik": nama_pemilik,
            "Jenis_Usaha": jenis_usaha,
            "Alamat": alamat,
            "No_HP": no_hp,
            "No_RT": no_rt.zfill(2),
            "Perizinan": perizinan
        }

        for col, val in updated_row.items():
            df.at[selected_index, col] = val

        save_data(df)
        st.cache_data.clear()
        st.success("Data berhasil diperbarui.")
        st.rerun()

    with st.expander("Hapus Data", expanded=False):
        konfirmasi = st.checkbox("Saya yakin ingin menghapus data ini.")
        if konfirmasi:
            if st.button("Hapus Data Sekarang", type="primary"):
                df = df.drop(index=selected_index)
                df.reset_index(drop=True, inplace=True)
                save_data(df)
                st.cache_data.clear()
                st.success("Data berhasil dihapus.")
                st.rerun()
        else:
            st.warning("Centang konfirmasi terlebih dahulu untuk menghapus.")

# Atur reset field
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False

if st.session_state.reset_form:
    st.session_state.input_nama_pemilik = ""
    st.session_state.input_jenis_usaha = ""
    st.session_state.input_alamat = ""
    st.session_state.input_no_hp = ""
    st.session_state.input_no_rt = ""
    st.session_state.input_perizinan = "TIDAK ADA"
    st.session_state.reset_form = False
    st.rerun()

# --------------------------
# ➕ Tambah UMKM Baru
# --------------------------
st.markdown("---")
st.subheader("Tambah UMKM Baru")

with st.form("tambah_umkm"):
    nama_pemilik = st.text_input("Nama Pemilik Baru", key="input_nama_pemilik").upper()
    jenis_usaha = st.text_input("Jenis Usaha", key="input_jenis_usaha").upper()
    alamat = st.text_area("Alamat", key="input_alamat").upper()
    no_hp = st.text_input("No HP", key="input_no_hp").upper()
    no_rt = st.text_input("No. RT", key="input_no_rt").zfill(2)
    perizinan = st.radio("Status Perizinan", options=["ADA", "TIDAK ADA"], horizontal=True, key="input_perizinan")

    submitted = st.form_submit_button("Tambah")

    if submitted:
        if nama_pemilik and jenis_usaha and alamat and no_hp and no_rt:
            new_row = {
                "Nama_Pemilik": nama_pemilik,
                "Jenis_Usaha": jenis_usaha,
                "Alamat": alamat,
                "No_HP": no_hp,
                "No_RT": no_rt.zfill(2),
                "Perizinan": perizinan
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.cache_data.clear()

            st.success("Data UMKM baru berhasil ditambahkan.")

            # Trigger reset on next rerun
            st.session_state.reset_form = True
            st.rerun()
        else:
            st.error("Harap isi semua kolom wajib.")