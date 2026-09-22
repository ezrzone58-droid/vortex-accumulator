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

# Inisialisasi Session State untuk navigasi dan login
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
        st.session_state.halaman = "dashboard"
        st.rerun()
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
        # Menyiapkan struktur data user termasuk tempat penyimpanan informasi/catatan
        db_data["users"][new_user] = {"password": new_pass, "informasi": []}
        simpan_database(db_data)
        st.success("Pendaftaran berhasil! Silakan klik Kembali untuk masuk.")
  with col2:
    if st.button("KEMBALI", use_container_width=True):
      st.session_state.halaman = "utama"
      st.rerun()

# --- 4. HALAMAN DASHBOARD / PENYIMPANAN DATA INFORMASI ---
elif st.session_state.halaman == "dashboard":
  user_aktif = st.session_state.user_login
  st.subheader(f"SELAMAT DATANG, {user_aktif}")
  st.write("Kelola dan simpan informasi atau data Anda di sini.")

  # Form untuk menambah informasi baru
  st.markdown("---")
  st.write("### TAMBAH INFORMASI BARU")
  judul_info = st.text_input("Judul Informasi / Data")
  isi_info = st.text_area("Isi Detail Informasi")

  if st.button("SIMPAN INFORMASI", use_container_width=True):
    if not judul_info or not isi_info:
      st.error("Judul dan isi informasi tidak boleh kosong!")
    else:
      # Pastikan key 'informasi' ada untuk jaga-jaga
      if "informasi" not in db_data["users"][user_aktif]:
        db_data["users"][user_aktif]["informasi"] = []

      # Masukkan data baru ke list informasi pengguna
      db_data["users"][user_aktif]["informasi"].append(
          {"judul": judul_info, "isi": isi_info}
      )
      simpan_database(db_data)
      st.success("Informasi berhasil disimpan!")
      st.rerun()

  # Menampilkan daftar informasi yang sudah disimpan
  st.markdown("---")
  st.write("### DAFTAR INFORMASI ANDA")

  user_data = db_data["users"].get(user_aktif, {})
  daftar_info = user_data.get("informasi", [])

  if not daftar_info:
    st.info("Belum ada informasi yang tersimpan.")
  else:
    for i, item in enumerate(daftar_info):
      with st.expander(f"{i + 1}. {item['judul']}"):
        st.write(item["isi"])

  st.markdown("---")
  if st.button("KELUAR / LOGOUT", use_container_width=True):
    st.session_state.user_login = None
    st.session_state.halaman = "utama"
    st.rerun()
