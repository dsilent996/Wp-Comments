import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("📝 Auto Comment to WordPress")

# Input form
article_url = st.text_input("🔗 URL Artikel WordPress")
nama = st.text_input("👤 Nama")
email = st.text_input("📧 Email")
komentar = st.text_area("💬 Komentar")

if st.button("🚀 Kirim Komentar"):
    if not article_url or not nama or not email or not komentar:
        st.warning("⚠️ Harap isi semua kolom sebelum mengirim!")
    else:
        st.info("🔍 Mengambil halaman artikel...")

        # Headers untuk permintaan HTTP
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive",
            "Referer": article_url,
            "Upgrade-Insecure-Requests": "1",
        }

        # Ambil halaman artikel
        session = requests.Session()
        response = session.get(article_url, headers=headers)

        if response.status_code != 200:
            st.error("❌ Gagal mengakses halaman artikel! Periksa URL.")
        else:
            soup = BeautifulSoup(response.text, "html.parser")

            # Cari form komentar
            comment_form = soup.find("form", class_="comment-form")

            if not comment_form:
                st.error("❌ Form komentar tidak ditemukan! Mungkin dimuat dengan JavaScript atau dilindungi.")
            else:
                st.success("✅ Form komentar ditemukan!")

                # Cek hidden input
                hidden_inputs = comment_form.find_all("input", {"type": "hidden"})
                hidden_data = {inp["name"]: inp["value"] for inp in hidden_inputs if "name" in inp.attrs and "value" in inp.attrs}

                # Data komentar
                comment_data = {
                    "author": nama,
                    "email": email,
                    "comment": komentar,
                    "submit": "Post Comment"
                }
                comment_data.update(hidden_data)  # Gabungkan dengan hidden data

                # Kirim komentar
                comment_url = comment_form.get("action") or article_url
                response = session.post(comment_url, data=comment_data, headers=headers)

                if response.status_code == 200:
                    st.success("✅ Komentar berhasil dikirim! (Cek moderasi WordPress)")
                else:
                    st.error(f"❌ Gagal mengirim komentar: {response.text}")
