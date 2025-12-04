# The Pong Game Project

Repository ini berisi kode sumber untuk implementasi permainan klasik **Pong**, yang dikembangkan menggunakan bahasa pemrograman Python. Proyek ini menggabungkan logika pemrograman prosedural dengan antarmuka grafis sederhana untuk menciptakan simulasi permainan arkade yang interaktif.

## Deskripsi Proyek

Aplikasi ini dirancang untuk mensimulasikan mekanisme permainan tenis meja dua dimensi (2D). Program ini mengintegrasikan beberapa pustaka standar dan eksternal Python untuk menangani aspek-aspek berbeda dari permainan, mulai dari *rendering* grafis vektor, manajemen antarmuka pengguna (GUI) untuk konfigurasi awal, hingga pemrosesan efek suara.

Tujuan utama dari pengembangan proyek ini adalah untuk mendemonstrasikan penerapan logika *Game Loop*, deteksi tabrakan (*collision detection*), dan manajemen *state* permainan dalam lingkungan Python.

## Fitur Utama

* **Antarmuka *Launcher* Interaktif:** Menggunakan `tkinter` untuk menu konfigurasi awal yang memungkinkan pengguna mengatur parameter permainan sebelum memulai.
* **Mode Permainan Fleksibel:** Mendukung mode pemain tunggal (*Single Player*) melawan komputer (Bot) dan mode dua pemain (*Multiplayer* lokal).
* **Tingkat Kesulitan Adaptif:** Tersedia tiga tingkat kesulitan (Easy, Medium, Hard) yang mempengaruhi kecepatan reaksi dan pergerakan Bot.
* **Sistem Audio:** Integrasi efek suara untuk pantulan bola, skor, dan notifikasi kemenangan menggunakan `pygame.mixer`.
* **Kustomisasi Permainan:** Pengguna dapat menentukan nama pemain dan batas skor maksimal untuk memenangkan pertandingan.

## Prasyarat Sistem

Sebelum menjalankan aplikasi ini, pastikan perangkat Anda telah memenuhi persyaratan berikut:

* **Python 3.x** terinstal di sistem operasi.
* Pustaka **Pygame** (diperlukan untuk fitur audio).

## Instalasi

1.  **Kloning Repository**
    Unduh atau kloning repositori ini ke direktori lokal Anda:
    ```bash
    git clone https://github.com/mahfudfaried/pong-game
    ```

2.  **Instalasi Dependensi**
    Instal pustaka eksternal yang dibutuhkan menggunakan PIP:
    ```bash
    pip install pygame
    ```

3.  **Persiapan Aset**
    Pastikan file audio berikut tersedia dalam satu direktori yang sama dengan `main.py` agar fitur suara berfungsi dengan baik:
    * `music_background.mp3`
    * `bounce.mp3`
    * `score.mp3`
    * `win.mp3`

## Cara Menjalankan

Jalankan file utama program melalui terminal atau *command prompt*:

```bash
python main.py
