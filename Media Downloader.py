import os
import threading
import subprocess
import customtkinter as ctk
from yt_dlp import YoutubeDL
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")
FOLDER_DOWNLOAD = os.path.expanduser("~/Downloads")
class DownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Media Downloader")
        self.geometry("600x400")
        self.resizable(False, False)
        self.title_label = ctk.CTkLabel(self, text="Media Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(padx=20, pady=(30, 10))
        self.sub_label = ctk.CTkLabel(self, text="Mendukung Semua URL Video/Audio Internet", font=ctk.CTkFont(size=13))
        self.sub_label.pack(padx=20, pady=(0, 20))
        self.url_entry = ctk.CTkEntry(self, width=500, placeholder_text="Tempel atau ketik URL apa saja di sini...")
        self.url_entry.pack(padx=20, pady=10)
        self.status_label = ctk.CTkLabel(self, text="Siap menerima tautan internet apa pun.", text_color="gray", font=ctk.CTkFont(size=12))
        self.status_label.pack(padx=20, pady=10)
        self.progress_bar = ctk.CTkProgressBar(self, width=500)
        self.progress_bar.pack(padx=20, pady=10)
        self.progress_bar.set(0)
        self.download_btn = ctk.CTkButton(self, text="Unduh Sekarang", font=ctk.CTkFont(weight="bold"), command=self.mulai_proses_thread)
        self.download_btn.pack(padx=20, pady=20)
        self.info_footer = ctk.CTkLabel(self, text=f"📂 Lokasi Penyimpanan: {FOLDER_DOWNLOAD}", text_color="gray", font=ctk.CTkFont(size=11))
        self.info_footer.pack(padx=20, pady=(20, 0), side="bottom")
    def kirim_notifikasi(self, judul, pesan, tipe="info"):
        ikon = "dialog-information"
        if tipe == "sukses":
            ikon = "emblem-success"
        elif tipe == "error":
            ikon = "dialog-error"
        try:
            subprocess.run(["notify-send", "-i", ikon, judul, pesan], check=True)
        except Exception:
            pass
    def mulai_proses_thread(self):
        url = self.url_entry.get().strip()
        if not url or not url.startswith(("http://", "https://")):
            self.status_label.configure(text="❌ URL tidak valid! Harus diawali http:// atau https://", text_color="red")
            return
        self.download_btn.configure(state="disabled", text="Memproses...")
        self.progress_bar.start()
        self.status_label.configure(text="⏳ Sedang menganalisis dan mengunduh dari sumber...", text_color="#3b8ed0")
        threading.Thread(target=self.proses_unduhan, args=(url,), daemon=True).start()
    def proses_unduhan(self, url):
        try:
            if "spotify.com" in url:
                judul, ext_akhir = self.unduh_via_spotdl(url)
            else:
                judul, ext_akhir = self.unduh_via_yt_dlp(url)
            self.after(0, self.unduhan_sukses, judul, ext_akhir)
        except Exception as e:
            pesan_error = str(e).split('\n')[0]
            self.after(0, self.unduhan_gagal, pesan_error)
    def unduh_via_yt_dlp(self, url):
        apakah_musik = "music.youtube.com" in url
        if apakah_musik:
            ydl_opts = {
                'outtmpl': f'{FOLDER_DOWNLOAD}/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'quiet': True,
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]
            }
        else:
            ydl_opts = {
                'outtmpl': f'{FOLDER_DOWNLOAD}/%(title)s.%(ext)s',
                'format': 'bestvideo+bestaudio/best',
                'quiet': True,
                'nocheckcertificate': True, 
            }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            judul_media = info.get('title', 'Media Internet')
            return judul_media, "MP3" if apakah_musik else "Format Terbaik"
    def unduh_via_spotdl(self, url):
        path_asal = os.getcwd()
        try:
            os.chdir(FOLDER_DOWNLOAD)
            proses = subprocess.run(["spotdl", "download", url], capture_output=True, text=True)
            os.chdir(path_asal)
            if proses.returncode == 0:
                return "Lagu dari Spotify", "MP3"
            else:
                raise Exception(proses.stderr)
        except Exception as e:
            os.chdir(path_asal)
            raise e
    def unduhan_sukses(self, judul, ext_akhir):
        self.progress_bar.stop()
        self.progress_bar.set(1.0)
        self.download_btn.configure(state="normal", text="Unduh Sekarang")
        self.url_entry.delete(0, 'end')
        self.status_label.configure(text=f"✅ Berhasil mengunduh media!", text_color="green")
        self.kirim_notifikasi("✅ Unduhan Sukses!", f"File [{ext_akhir}] berhasil disimpan ke folder Downloads.", tipe="sukses")
    def unduhan_gagal(self, error):
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.download_btn.configure(state="normal", text="Unduh Sekarang")
        self.status_label.configure(text=f"❌ Gagal: Tautan tidak didukung atau unduhan diblokir.", text_color="red")
        self.kirim_notifikasi("❌ Unduhan Gagal", f"Info: {error[:60]}", tipe="error")
if __name__ == "__main__":
    app = DownloaderApp()
    app.mainloop()