# Media Downloader
  Aplikasi desktop berbasis GUI (Antarmuka Grafis) yang ringan dan modern untuk mengunduh audio serta video dari berbagai platform internet. Aplikasi ini dibangun menggunakan **Python** dengan antarmuka **CustomTkinter**, serta ditenagai oleh pustaka andal `yt-dlp` dan `spotdl`.

---

## Fitur Utama
- **Antarmuka Modern:** Menggunakan tema bawaan CustomTkinter yang mendukung otomatisasi Mode Gelap/Terang (System                           Theme).
- **Multi-Platform:** Mendukung pengunduhan dari YouTube, YouTube Music, Spotify, dan ratusan situs internet lainnya                       yang didukung oleh `yt-dlp`.
- **Deteksi Otomatis:** Otomatis memisahkan logika pengunduhan musik (`.mp3` kualitas tinggi 320kbps) atau video                             dengan kualitas terbaik berdasarkan tautan yang dimasukkan.
- **Bebas Hang/Freeze:** Proses pengunduhan berjalan di latar belakang menggunakan teknik *Asynchronous Threading*,                           sehingga aplikasi tetap responsif selama proses berlangsung.
- **Penyimpanan Otomatis:** Seluruh file hasil unduhan langsung diarahkan secara rapi ke folder bawaan sistem yaitu                              `Downloads`.
- **Notifikasi Desktop:** Terintegrasi dengan notifikasi sistem OS (mendukung `notify-send` untuk lingkungan Linux)                            saat unduhan berhasil atau gagal.

---

## Prasyarat & Dependensi
Sebelum menjalankan aplikasi ini, pastikan komputer Anda sudah terinstal pustaka dan komponen berikut:
### 1. Python
Pastikan Python versi 3.8 atau yang lebih baru sudah terpasang di sistem Anda.
### 2. FFmpeg (Penting!)
Aplikasi ini membutuhkan **FFmpeg** untuk menggabungkan video beresolusi tinggi atau mengonversi audio ke format `.mp3`.
- **Linux:** `sudo apt install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Unduh binari FFmpeg resmi dan pastikan jalurnya sudah dimasukkan ke dalam *Environment Variables (PATH)* Windows Anda.
### 3. Pustaka Python (Pip)
Instal pustaka yang dibutuhkan dengan menjalankan perintah berikut di terminal/command prompt:
```bash
pip install customtkinter yt-dlp spotdl
