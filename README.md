## Anggota Kelompok
1. 2306165534: Nur Khoirunnisa Salsabila
2. 2306203324: Nabil Zahid Rahman
3. 2306245642: Alica Kinar Deska
4. 2306275172: Patricia Gloria Sujatmoko Silaban
5. 2306275203: Malika Atha Indurasmi

## Tentang Proyek
- Nama Web: MlakuMlaku
- Repositori GitHub: https://github.com/Chromss/mlaku-mlaku
- Deployment Web: https://pbp.cs.ui.ac.id/nabil.zahid/mlakumlaku
*Tentatif, bisa berubah ke web hosting/domain lain, jika ada perubahan terkait ini, README akan diubah secepatnya.

## Deskripsi Proyek
Jogja adalah kota yang istimewa dengan sejuta cerita. Kota ini selalu punya berbagai cara untuk menanamkan rindu untuk kembali kepadanya. Namun, kurang lengkap rasanya bila kita mencintai Jogja tanpa pernah menyusuri setiap sudut kotanya. Bingung mau ke mana di Jogja? MlakuMlaku solusinya! MlakuMlaku berarti “Jalan-jalan” di bahasa Jawa. Seperti namanya, MlakuMlaku hadir untuk menemani kegiatan “Jalan-jalan” Anda di Kota Jogja. MlakuMlaku bukan hanya menampilkan destinasi wisata, tetapi juga menampilkan katalog souvenir yang dijual di lokasi wisata tersebut. MlakuMlaku menghadirkan berbagai fitur yang siap Anda nikmati selama mengeksplorasi Kota Jogja.

Berikut adalah manfaat menggunakan web MlakuMlaku dari Kami, webmaster.

### A. Berbelanja Souvenir
Pengguna dapat melihat souvenir yang dijual di suatu lokasi dan membelinya.

### B. Melihat Ulasan dan Rating, serta Berkomentar
Pengguna dapat memberikan ulasan dan rating untuk setiap destinasi wisata, serta melihat ulasan dan rating dari pengguna lain. Hal ini akan meningkatkan keyakinan pengguna dalam memilih tempat yang ingin \`dikunjungi.

### C. Template Itinerary
1. Menyediakan berbagai template itinerary seperti "2 Hari 2 Malam di Jogja" yang dapat disesuaikan sesuai preferensi.
2. Pengguna dapat menambahkan atau menghapus destinasi sesuai preferensi.

### D. Bookmark/Playlist Tempat Wisata
1. Pengguna dapat menyimpan destinasi favorit ke dalam daftar bookmark pribadi.
2. Pengguna dapat mengakses fitur untuk membuat beberapa playlist berdasarkan tema atau rencana perjalanan.
3. Pengguna dapat mengatur agar playlist dapat menjadi public untuk dibagikan dengan teman maupun private untuk koleksi pribadi.

### E. #JurnalJogjaku 
1. Platform seperti Medium untuk membagikan pengalaman pribadi selama di Jogja.
2. Pengguna dapat menulis cerita, tips, atau momen berkesan yang dialami.

## Daftar Modul

### A. Modul Admin: Manajemen Produk
1. Menambahkan Produk: Setelah memilih lokasi, admin dapat menambahkan produk-produk yang dijual di lokasi tersebut.
2. Mengedit Produk: Admin dapat mengubah detail produk, seperti nama, deskripsi, harga, dan gambar.
3. Menghapus Produk: Admin dapat menghapus produk yang tidak lagi tersedia atau ingin dihentikan penjualannya di lokasi tersebut.

### B. Places
Setelah memilih lokasi, pengguna dapat melihat deskripsi singkat mengenai lokasi tersebut serta daftar produk yang dijual di lokasi tersebut.

**Ulasan dan Komentar**
1. Memberikan Ulasan: Pengguna dapat memberikan rating (bintang) terhadap lokasi yang dikunjungi.
2. Komentar: Pengguna dapat meninggalkan komentar atau feedback mengenai pengalaman mereka di lokasi tersebut.
3. Interaksi Sosial: Pengguna dapat membaca ulasan dan komentar dari pengguna lain untuk mendapatkan informasi tambahan sebelum mengunjungi lokasi.

**Pembelian Produk**
1. Keranjang Belanja: Pengguna dapat memilih produk yang ingin dibeli dan menambahkannya ke dalam keranjang belanja.
2. Pembayaran: Aplikasi menyediakan berbagai metode pembayaran yang aman dan mudah digunakan untuk menyelesaikan transaksi pembelian.
3. Notifikasi Pembelian: Setelah melakukan pembelian, pengguna akan menerima notifikasi konfirmasi serta informasi pengiriman produk.

### C. Itinerary
1. Template Management: Menyediakan berbagai template itinerary yang dapat disesuaikan oleh pengguna.
2. Destination Editing: Menambah, menghapus, atau mengubah destinasi dalam template itinerary yang dipilih jika user merasa kurang puas dengan template.
3. Itinerary Sharing: Mengizinkan user untuk membagikan tautan  itinerary yang telah dibuat dengan user lain.

### D. Collections
1. Bookmark Management: Mengizinkan user menyimpan destinasi favorit mereka ke dalam sebuah koleksi di akun mereka.
2. Playlist Creation: Untuk membuat, mengedit, dan menghapus playlist berdasarkan tema atau rencana perjalanan yang sesuai dengan preferensi user.
3. Playlist Privacy: Mengatur playlist sebagai public atau private, sesuai keinginan user.
4. Playlist Sharing: Memungkinkan user untuk membagikan playlist mereka dengan orang lain.

### E. #JurnalJogjaku
1. Journal Posting: Mengizinkan pengguna menulis cerita, tips, dan pengalaman mereka dalam format thread (seperti Twitter).
2. Comment: Pengguna lain dapat meninggalkan komentar pada cerita yang diposting.
3. Journal Search: Untuk mencari cerita berdasarkan hashtag atau kata kunci tertentu.

## Role dan Peran Pengguna
### A. Customer
Role ini merupakan role umum yang dapat mengakses modul 2 s.d. 5 di dalam web MlakuMlaku, yakni Places, Itinerary, Collections, dan #JurnalJogjaku. Role ini diperuntukkan bagi pengguna yang ingin menikmati layanan web dalam sudut pandang pembeli, yakni mengamati, membeli, dan berbagi. Batasan yang dimiliki role ini adalah tidak dapat menambahkan, menyunting, dan menghapus daftar produk yang tersedia pada web, juga memiliki batasan dalam mengakses page-page berbasis admin. Namun, registrasi untuk mengambil role ini lebih sederhana dengan hanya memasukkan data umum seperti username, email, dan password walaupun untuk pembelian produk tetap harus menyertakan data pengantaran.

### B. Admin
Role ini merupakan role khusus yang dapat mengakses seluruh modul di dalam web MlakuMlaku. Role ini hanya diperuntukkan bagi webmaster yang mengatur deployment dari keseluruhan web termasuk menambahkan, menyunting, dan menghapus daftar produk yang didaftarkan. Selain itu, sebagai webmaster, role ini juga dapat melakukan modifikasi dan penambahan pada aspek modul yang lain sesuai kepentingan tertentu. Role ini hanya dimiliki oleh lima orang, yakni yang tertera namanya di paling atas.

## Sumber Dataset Awal
1. Kaggle: https://www.kaggle.com/code/kevinarnandes/rekomendasi-wisata-jogja-cosine-similarity 
2. Dataset Tempat Wisata dalam JSON dan Formatted dalam Spreadsheet: ristek.link/PBP-A09
3. Sumber Nama Produk:
    - https://jogjaki.jogjaprov.go.id/byname_cobranding.asp
    - https://www.jogjasouvenir.com/
    - https://www.indonesia.travel/id/id/ide-liburan/ke-jogja-jangan-lupa-beli-6-oleh-oleh-yang-unik-dan-istimewa-ini.html 
4. Dataset Fix PBP A09: ristek.link/DATASET_MlakuMlaku