# Toolspython
Tools Python seperti Input Custom.  

**1. Input Custom**
Saya buat untuk menggantikan input asli, karena input asli tidak bisa panah kanan kiri. Dan simpan memory. Dan juga, input biasa tidak bisa memvalidasi nilai integer atau float sebelum dienter.  

Tujuan, awalnya saya buat untuk mempermudah pembuatan proyek-proyek saya selanjutnya.  

Cara pemakaian :
```py
# standar
nama = readline(prompt="Masukkan nama Anda: ")
print(f"Halo, {nama}!")

# Input terisi default "Ketik di sini..."
teks = readline(prompt="Pesan: ", input_val="Ketik di sini...")

# menambahkan satuan ' kg' yang tidak bisa dihapus, tipe terkunci float
berat = readline(prompt="Berat badan: ", end_line=" kg", type="float")
```
**2. Tools Terminal**

Sebuah Custom CLI IDE, menggunakan python di terminal Linux di Android.  
Digunakan untuk mempermudah saya untuk belajar programming. 

1. Mendukung multi bahasa pemrograman.
2. Auto compile dan menghapus file.
3. Multi bahasa satu perintah 'run'
4. run HTML menggunakan python
5. Auto installer bahasa
6. Menggunakan module readline

Yang belum :
Banyak, diantaranya run html + php


