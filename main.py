import json
import os
import tkinter as tk
from tkinter import messagebox

FILE_DB = "database_pengguna.json"

# Konfigurasi Palet Warna Tema (Light & Dark)
THEMES = {
    "light": {
        "bg_main": "#f0f4f8",
        "bg_card": "#ffffff",
        "text_main": "#1e293b",
        "text_sub": "#64748b",
        "primary": "#3368A0",
        "border": "#cbd5e1",
        "input_bg": "#f8fafc",
        "input_fg": "#0f172a",
        "accent": "#10b981",
    },
    "dark": {
        "bg_main": "#050a1a",
        "bg_card": "#091540",
        "text_main": "#f9fafb",
        "text_sub": "#94a3b8",
        "primary": "#2a52be",
        "border": "#172b66",
        "input_bg": "#0d1b4f",
        "input_fg": "#f9fafb",
        "accent": "#34d399",
    },
}

current_theme = "light"


def muat_database():
  if os.path.exists(FILE_DB):
    try:
      with open(FILE_DB, "r") as f:
        return json.load(f)
    except:
      return {"users": {}, "pending": []}
  return {"users": {}, "pending": []}


def simpan_database(data):
  with open(FILE_DB, "w") as f:
    json.dump(data, f, indent=4)


db_data = muat_database()


def bersihkan_frame():
  for widget in jendela.winfo_children():
    widget.destroy()


# --- KELAS TOMBOL KUSTOM ---
class ModernButton(tk.Canvas):

  def __init__(
      self,
      parent,
      text,
      command,
      bg_color,
      fg_color,
      outline_color=None,
      height=42,
  ):
    super().__init__(
        parent,
        height=height,
        highlightthickness=0,
        bg=parent["bg"],
        cursor="hand2",
    )
    self.command = command
    self.bg_color = bg_color
    self.fg_color = fg_color
    self.outline_color = outline_color
    self.text = text

    self.bind("<Configure>", self.draw)
    self.bind("<Button-1>", lambda e: self.command())

  def draw(self, event=None):
    self.delete("all")
    w = self.winfo_width()
    h = self.winfo_height()
    if w <= 1 or h <= 1:
      return

    # Efek bayangan
    self.create_rounded_rect(
        3, 6, w - 3, h - 2 + 3, radius=14, fill="#cbd5e1", outline=""
    )
    # Kotak utama tombol
    kwargs = {"radius": 14, "fill": self.bg_color}
    if self.outline_color:
      kwargs["outline"] = self.outline_color
      kwargs["width"] = 2
    else:
      kwargs["outline"] = self.bg_color

    self.create_rounded_rect(3, 3, w - 3, h - 2, **kwargs)
    self.create_text(
        w / 2,
        (h - 2) / 2 + 1,
        text=self.text,
        fill=self.fg_color,
        font=("Segoe UI", 10, "bold"),
    )

  def create_rounded_rect(self, x1, y1, x2, y2, radius=15, **kwargs):
    points = [
        x1 + radius,
        y1,
        x1 + radius,
        y1,
        x2 - radius,
        y1,
        x2 - radius,
        y1,
        x2,
        y1,
        x2,
        y1 + radius,
        x2,
        y1 + radius,
        x2,
        y2 - radius,
        x2,
        y2 - radius,
        x2,
        y2,
        x2 - radius,
        y2,
        x2 - radius,
        y2,
        x1 + radius,
        y2,
        x1 + radius,
        y2,
        x1,
        y2,
        x1,
        y2 - radius,
        x1,
        y2 - radius,
        x1,
        y1 + radius,
        x1,
        y1 + radius,
        x1,
        y1,
    ]
    return self.create_polygon(points, **kwargs, smooth=True)


# --- 1. HALAMAN UTAMA (Judul, Logo, Tombol Masuk & Daftar) ---
def halaman_utama():
  bersihkan_frame()
  th = THEMES[current_theme]
  jendela.configure(bg=th["bg_main"])

  card = tk.Frame(
      jendela,
      bg=th["bg_card"],
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=420)

  # Bagian Logo / Ikon & Judul
  tk.Label(
      card,
      text="⚡",
      font=("Segoe UI", 36),
      bg=th["bg_card"],
      fg=th["primary"],
  ).pack(pady=(35, 5))

  tk.Label(
      card,
      text="SISTEM PERHITUNGAN",
      font=("Segoe UI", 16, "bold"),
      bg=th["bg_card"],
      fg=th["primary"],
  ).pack(pady=(0, 5))

  tk.Label(
      card,
      text="Silakan masuk atau buat akun baru",
      font=("Segoe UI", 9),
      bg=th["bg_card"],
      fg=th["text_sub"],
  ).pack(pady=(0, 35))

  # Tombol Navigasi
  f_btn = tk.Frame(card, bg=th["bg_card"])
  f_btn.pack(fill="x", padx=35)

  btn_masuk = ModernButton(
      f_btn,
      text="MASUK",
      command=halaman_login,
      bg_color=th["primary"],
      fg_color="#ffffff",
      height=45,
  )
  btn_masuk.pack(fill="x", pady=(0, 12))

  btn_daftar = ModernButton(
      f_btn,
      text="DAFTAR AKUN",
      command=halaman_daftar,
      bg_color="#ffffff",
      fg_color=th["primary"],
      outline_color=th["primary"],
      height=45,
  )
  btn_daftar.pack(fill="x")


# --- 2. HALAMAN MASUK / LOGIN (Dua kolom sejajar: Username & Password) ---
def halaman_login():
  bersihkan_frame()
  th = THEMES[current_theme]
  jendela.configure(bg=th["bg_main"])

  card = tk.Frame(
      jendela,
      bg=th["bg_card"],
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=420)

  tk.Label(
      card,
      text="MASUK AKUN",
      font=("Segoe UI", 14, "bold"),
      bg=th["bg_card"],
      fg=th["primary"],
  ).pack(pady=(30, 20))

  f_form = tk.Frame(card, bg=th["bg_card"])
  f_form.pack(fill="x", padx=35)

  # Kolom Username Sejajar
  tk.Label(
      f_form,
      text="USERNAME",
      font=("Segoe UI", 8, "bold"),
      bg=th["bg_card"],
      fg=th["text_sub"],
      anchor="w",
  ).pack(fill="x", pady=(0, 2))
  e_user = tk.Entry(
      f_form,
      font=("Segoe UI", 11),
      bg=th["input_bg"],
      fg=th["input_fg"],
      bd=0,
      highlightthickness=1,
      highlightbackground=th["border"],
      highlightcolor=th["primary"],
  )
  e_user.pack(fill="x", ipady=6, pady=(0, 12))

  # Kolom Password Sejajar
  tk.Label(
      f_form,
      text="PASSWORD",
      font=("Segoe UI", 8, "bold"),
      bg=th["bg_card"],
      fg=th["text_sub"],
      anchor="w",
  ).pack(fill="x", pady=(0, 2))
  e_pass = tk.Entry(
      f_form,
      font=("Segoe UI", 11),
      bg=th["input_bg"],
      fg=th["input_fg"],
      show="*",
      bd=0,
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  e_pass.pack(fill="x", ipady=6, pady=(0, 20))

  def proses_login():
    u = e_user.get()
    p = e_pass.get()
    if not u or not p:
      messagebox.showerror("Error", "Username dan Password wajib diisi!")
      return
    if u in db_data["users"] and db_data["users"][u]["password"] == p:
      messagebox.showinfo("Sukses", f"Selamat datang kembali, {u}!")
    else:
      messagebox.showerror("Error", "Username atau Password salah!")

  f_btn = tk.Frame(card, bg=th["bg_card"])
  f_btn.pack(fill="x", padx=35)

  btn_submit = ModernButton(
      f_btn,
      text="LOGIN SEKARANG",
      command=proses_login,
      bg_color=th["primary"],
      fg_color="#ffffff",
      height=40,
  )
  btn_submit.pack(fill="x", pady=(0, 8))

  btn_kembali = ModernButton(
      f_btn,
      text="KEMBALI",
      command=halaman_utama,
      bg_color="#ffffff",
      fg_color=th["text_sub"],
      outline_color=th["border"],
      height=38,
  )
  btn_kembali.pack(fill="x")


# --- 3. HALAMAN DAFTAR / REGISTRASI ---
def halaman_daftar():
  bersihkan_frame()
  th = THEMES[current_theme]
  jendela.configure(bg=th["bg_main"])

  card = tk.Frame(
      jendela,
      bg=th["bg_card"],
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  card.place(relx=0.5, rely=0.5, anchor="center", width=400, height=460)

  tk.Label(
      card,
      text="PENDAFTARAN AKUN",
      font=("Segoe UI", 14, "bold"),
      bg=th["bg_card"],
      fg=th["primary"],
  ).pack(pady=(25, 15))

  f_form = tk.Frame(card, bg=th["bg_card"])
  f_form.pack(fill="x", padx=35)

  tk.Label(
      f_form,
      text="BUAT USERNAME",
      font=("Segoe UI", 8, "bold"),
      bg=th["bg_card"],
      fg=th["text_sub"],
      anchor="w",
  ).pack(fill="x", pady=(0, 2))
  e_user = tk.Entry(
      f_form,
      font=("Segoe UI", 11),
      bg=th["input_bg"],
      fg=th["input_fg"],
      bd=0,
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  e_user.pack(fill="x", ipady=6, pady=(0, 10))

  tk.Label(
      f_form,
      text="BUAT PASSWORD",
      font=("Segoe UI", 8, "bold"),
      bg=th["bg_card"],
      fg=th["text_sub"],
      anchor="w",
  ).pack(fill="x", pady=(0, 2))
  e_pass = tk.Entry(
      f_form,
      font=("Segoe UI", 11),
      bg=th["input_bg"],
      fg=th["input_fg"],
      show="*",
      bd=0,
      highlightthickness=1,
      highlightbackground=th["border"],
  )
  e_pass.pack(fill="x", ipady=6, pady=(0, 15))

  def proses_daftar():
    u = e_user.get()
    p = e_pass.get()
    if not u or not p:
      messagebox.showerror("Error", "Semua kolom harus diisi!")
      return
    if u in db_data["users"]:
      messagebox.showerror("Error", "Username sudah terdaftar!")
      return

    db_data["users"][u] = {"password": p}
    simpan_database(db_data)
    messagebox.showinfo("Sukses", "Pendaftaran berhasil! Silakan masuk.")
    halaman_login()

  f_btn = tk.Frame(card, bg=th["bg_card"])
  f_btn.pack(fill="x", padx=35)

  btn_submit = ModernButton(
      f_btn,
      text="DAFTARKAN AKUN",
      command=proses_daftar,
      bg_color=th["accent"],
      fg_color="#ffffff",
      height=40,
  )
  btn_submit.pack(fill="x", pady=(0, 8))

  btn_kembali = ModernButton(
      f_btn,
      text="KEMBALI KE UTAMA",
      command=halaman_utama,
      bg_color="#ffffff",
      fg_color=th["text_sub"],
      outline_color=th["border"],
      height=38,
  )
  btn_kembali.pack(fill="x")


# Inisialisasi Jendela Utama Tkinter
jendela = tk.Tk()
jendela.title("Sistem Perhitungan")
jendela.geometry("900x520")

# Mulai aplikasi dari Halaman 1
halaman_utama()
jendela.mainloop()
