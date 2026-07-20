# Toolspython
Tools Python seperti Input Custom.  

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

