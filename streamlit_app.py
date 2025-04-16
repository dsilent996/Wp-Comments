import streamlit as st
import requests
from bs4 import BeautifulSoup

st.title("📝 Auto Comment to Multiple WordPress Articles")

# Input form
urls = st.text_area("🔗 Masukkan URL Artikel (satu per baris)", height=150)
nama = st.text_input("👤 Nama")
email = st.text_input("📧 Email")
komentar = st.text_area("💬 Komentar")

if st.button("🚀 Kirim Komentar"):
    if not urls or not nama or not email or not komentar:
        st.warning("⚠️ Harap isi semua kolom sebelum mengirim!")
    else:
        url_list = urls.strip().split("\n")  # Pecah input menjadi list URL
        st.info(f"🔍 Menemukan {len(url_list)} URL untuk dikomentari.")

        # Loop melalui setiap URL
        for article_url in url_list:
            article_url = article_url.strip()
            if not article_url:
                continue

            st.write(f"🔗 **Mengakses:** {article_url}")

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Referer": article_url,
                "Upgrade-Insecure-Requests": "1",
            }

            session = requests.Session()
            response = session.get(article_url, headers=headers)

            if response.status_code != 200:
                st.error(f"❌ Gagal mengakses: {article_url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            comment_form = soup.find("form", class_="comment-form")

            if not comment_form:
                st.error(f"❌ Form komentar tidak ditemukan di {article_url}")
                continue

            if not article_url.startswith("http://") and not article_url.startswith("https://"):
                st.error(f"Invalid URL: {article_url}")
                continue


            # Ambil hidden input
            hidden_inputs = comment_form.find_all("input", {"type": "hidden"})
            hidden_data = {inp["name"]: inp["value"] for inp in hidden_inputs if "name" in inp.attrs and "value" in inp.attrs}

            # Data komentar
            comment_data = {
                "author": nama,
                "email": email,
                "comment": komentar,
                "submit": "Post Comment"
            }
            comment_data.update(hidden_data)

            # Kirim komentar
            comment_url = comment_form.get("action") or article_url
            post_response = session.post(comment_url, data=comment_data, headers=headers)

            if post_response.status_code == 200:
                st.success(f"✅ Komentar berhasil dikirim ke: {article_url} (Cek moderasi WordPress)")
            else:
                st.error(f"❌ Gagal mengirim komentar ke: {article_url}")
