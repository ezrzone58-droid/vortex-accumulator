import json
import os
import streamlit as st

FILE_DB = "database_pengguna.json"


def muat_database():
  if os.path.exists(FILE_DB):
    try:
      with open(FILE_DB, "r") as f:
        return json.load(f)
    except:
      return {"users": {}}
  return {"users": {}}


def simpan_database(data):
  with open(FILE_DB, "w") as f:
    json.dump(data, f, indent=4)


db_data = muat_database()

st.set_page_config(
    page_title="Vortex Accumulator", page_icon="", layout="centered"
)

# Inisialisasi Session State untuk navigasi halaman
if "halaman" not in st.session_state:
  st.session_state.halaman = "utama"
if "user_login" not in st.session_state:
  st.session_state.user_login = None

# --- 1. HALAMAN UTAMA ---
if st.session_state.halaman == "utama":
  st.markdown(
      "<h1 style='text-align: center;'>VORTEX ACCUMULATOR</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: gray;'>Silakan masuk atau buat akun"
      " baru</p>",
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2)
  with col1:
    if st.button("MASUK", use_container_width=True):
      st.session_state.halaman = "login"
      st.rerun()
  with col2:
    if st.button("DAFTAR AKUN", use_container_width=True):
      st.session_state.halaman = "daftar"
      st.rerun()

# --- 2. HALAMAN MASUK / LOGIN ---
elif st.session_state.halaman == "login":
  st.subheader("MASUK AKUN")

  username = st.text_input("USERNAME")
  password = st.text_input("PASSWORD", type="password")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("LOGIN SEKARANG", use_container_width=True):
      if not username or not password:
        st.error("Username dan Password wajib diisi!")
      elif (
          username in db_data["users"]
          and db_data["users"][username]["password"] == password
      ):
        st.session_state.user_login = username
        st.success(f"Selamat datang kembali, {username}!")
      else:
        st.error("Username atau Password salah!")

  with col2:
    if st.button("KEMBALI", use_container_width=True):
      st.session_state.halaman = "utama"
      st.rerun()

# --- 3. HALAMAN DAFTAR / REGISTRASI ---
elif st.session_state.halaman == "daftar":
  st.subheader("PENDAFTARAN AKUN")

  new_user = st.text_input("BUAT USERNAME")
  new_pass = st.text_input("BUAT PASSWORD", type="password")

  col1, col2 = st.columns(2)
  with col1:
    if st.button("DAFTARKAN AKUN", use_container_width=True):
      if not new_user or not new_pass:
        st.error("Semua kolom harus diisi!")
      elif new_user in db_data["users"]:
        st.error("Username sudah terdaftar!")
      else:
        db_data["users"][new_user] = {"password": new_pass}
        simpan_database(db_data)
        st.success("Pendaftaran berhasil! Silakan klik Kembali untuk masuk.")
  with col2:
    if st.button("KEMBALI", use_container_width=True):
      st.session_state.halaman = "utama"
      st.rerun()
