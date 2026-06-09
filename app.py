import streamlit as st
from collections import deque

# =====================================
# KELAS PRIORITY QUEUE PUSKESMAS
# =====================================
class PuskesmasQueue:
    def __init__(self):
        self.darurat = deque()
        self.lansia = deque()
        self.ibu_hamil = deque()
        self.umum = deque()
        self.nomor = 0

    def tambah_pasien(self, nama, kategori):
        self.nomor += 1

        pasien = {
            "nomor": self.nomor,
            "nama": nama,
            "kategori": kategori
        }

        if kategori == "Darurat":
            self.darurat.append(pasien)

        elif kategori == "Lansia":
            self.lansia.append(pasien)

        elif kategori == "Ibu Hamil":
            self.ibu_hamil.append(pasien)

        else:
            self.umum.append(pasien)

        return self.nomor

    def panggil_pasien(self):

        if self.darurat:
            return self.darurat.popleft()

        elif self.lansia:
            return self.lansia.popleft()

        elif self.ibu_hamil:
            return self.ibu_hamil.popleft()

        elif self.umum:
            return self.umum.popleft()

        return None

    def tampilkan(self):
        return (
            list(self.darurat),
            list(self.lansia),
            list(self.ibu_hamil),
            list(self.umum)
        )


# =====================================
# SESSION STATE
# =====================================
if "antrian" not in st.session_state:
    st.session_state.antrian = PuskesmasQueue()

# =====================================
# KONFIGURASI HALAMAN
# =====================================
st.set_page_config(
    page_title="Sistem Antrean Puskesmas",
    page_icon="🏥",
    layout="wide"
)

# =====================================
# HEADER
# =====================================
st.markdown("""
<h1 style="
text-align:center;
color:#0066CC;">
🏥 PUSKESMAS ASFIH TANGERANG
</h1>

<p style="
text-align:center;
font-size:18px;
color:#666666;">
Selamat Datang! Sistem ini digunakan untuk mengelola antrean pasien secara cepat,
mudah, dan terorganisir menggunakan <b>Priority Queue</b>.
</p>
""", unsafe_allow_html=True)

st.markdown("---")

# =====================================
# MENU UTAMA
# =====================================
menu = st.sidebar.selectbox(
    "📋 Pilih Menu",
    [
        "Daftar Pasien",
        "Lihat Antrean",
        "Panggil Pasien"
    ]
)

# =====================================
# DAFTAR PASIEN
# =====================================
if menu == "Daftar Pasien":

    st.header("📝 Pendaftaran Pasien")

    kategori = st.selectbox(
        "Kategori Pasien",
        [
            "Umum",
            "Ibu Hamil",
            "Lansia",
            "Darurat"
        ]
    )

    nama = st.text_input(
        "Masukkan Nama Pasien"
    )

    if st.button("Ambil Nomor Antrean"):

        if nama:

            nomor = (
                st.session_state.antrian
                .tambah_pasien(
                    nama,
                    kategori
                )
            )

            st.success(
                f"Nomor Antrean Anda : {nomor}"
            )

        else:

            st.warning(
                "Nama pasien harus diisi!"
            )

# =====================================
# LIHAT ANTREAN
# =====================================
elif menu == "Lihat Antrean":

    st.header("📋 Daftar Antrean Pasien")

    darurat, lansia, ibu_hamil, umum = (
        st.session_state.antrian.tampilkan()
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🚑 Antrean Darurat")

        if darurat:
            for p in darurat:
                st.error(
                    f"No {p['nomor']} - {p['nama']}"
                )
        else:
            st.write("Kosong")

        st.subheader("👴 Antrean Lansia")

        if lansia:
            for p in lansia:
                st.warning(
                    f"No {p['nomor']} - {p['nama']}"
                )
        else:
            st.write("Kosong")

    with col2:

        st.subheader("🤰 Antrean Ibu Hamil")

        if ibu_hamil:
            for p in ibu_hamil:
                st.info(
                    f"No {p['nomor']} - {p['nama']}"
                )
        else:
            st.write("Kosong")

        st.subheader("👤 Antrean Umum")

        if umum:
            for p in umum:
                st.success(
                    f"No {p['nomor']} - {p['nama']}"
                )
        else:
            st.write("Kosong")

# =====================================
# PANGGIL PASIEN
# =====================================
elif menu == "Panggil Pasien":

    st.header("📢 Panggil Pasien")

    if st.button(
        "Panggil Pasien Berikutnya",
        use_container_width=True
    ):

        pasien = (
            st.session_state.antrian
            .panggil_pasien()
        )

        if pasien:

            st.success(
                f"""
Nomor Antrean : {pasien['nomor']}

Nama Pasien : {pasien['nama']}

Kategori : {pasien['kategori']}

Silakan menuju ruang pemeriksaan.
"""
            )

            st.balloons()

        else:

            st.warning(
                "Tidak ada pasien dalam antrean."
            )
