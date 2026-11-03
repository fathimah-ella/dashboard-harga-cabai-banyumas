# Dataset Harga Cabai Rawit Kabupaten Banyumas

## Sumber Data

Dataset ini berasal dari data harga cabai rawit Kabupaten Banyumas yang dicatat oleh **Dinas Perindustrian dan Perdagangan (Dinperindag) Kabupaten Banyumas**. Data harga bahan pangan Dinperindag juga tersedia secara publik melalui portal [SIGAOKMAS](https://sigaokmas.banyumaskab.go.id/).

Dataset yang tersedia di repository ini **bukan merupakan data mentah resmi dari pemerintah**, melainkan data yang telah melalui tahap preprocessing untuk keperluan penelitian skripsi.

## Deskripsi Dataset

| Keterangan | Detail |
|---|---|
| Periode | Januari 2023 s/d Desember 2025 |
| Frekuensi | Harian |
| Komoditas | Cabai Rawit Merah dan Cabai Rawit Hijau |
| Jumlah Pasar | 14 pasar tradisional (dari 25 pasar yang dipantau Dinperindag) |
| Satuan Harga | Rupiah per kilogram (Rp/kg) |
| Format File | Excel (.xlsx) |

## Daftar 14 Pasar

Ajibarang, Banyumas, Buntu, Kemukusan, Larangan, Manis, Proliman, Sarimulyo, Sokaraja, Sumpiuh, Tambak, Wage, Wangon, Wijahan.

11 pasar lainnya dieliminasi karena memiliki persentase data asli (observed) di bawah 50%, yang berarti lebih dari separuh datanya merupakan hasil imputasi dan tidak cukup representatif untuk pemodelan.

## Struktur File

### `data/dinperindag_2023-2025.xlsx`

File data asli dari Dinperindag sebelum preprocessing. Berisi harga harian cabai rawit merah dan hijau di seluruh pasar yang dipantau.

### `data/dinperindag_2023-2025_clean.xlsx`

File data hasil preprocessing. Terdiri dari dua sheet:

**Sheet `cabai_rawit`** berisi kolom:

| Kolom | Tipe | Keterangan |
|---|---|---|
| `tanggal` | datetime | Tanggal pencatatan harga |
| `nama_pasar` | string | Nama pasar tradisional |
| `harga_rawit_merah` | float | Harga cabai rawit merah (Rp/kg) |
| `harga_rawit_hijau` | float | Harga cabai rawit hijau (Rp/kg) |
| `is_observed_merah` | int (0/1) | 1 = harga asli tercatat, 0 = hasil imputasi |
| `is_observed_hijau` | int (0/1) | 1 = harga asli tercatat, 0 = hasil imputasi |

**Sheet `master_pasar`** berisi informasi referensi 14 pasar terpilih beserta metadata pendukung.

## Tahap Preprocessing

Dataset telah melalui tahap preprocessing berikut:

1. **Pembersihan data** : Penghapusan duplikat, perbaikan format tanggal, dan standarisasi nama pasar.

2. **Seleksi pasar** : Dari 25 pasar yang dipantau Dinperindag, hanya 14 pasar yang dipertahankan berdasarkan kriteria persentase data asli (observed) di atas 50%.

3. **Forward fill** : Nilai harga yang kosong (missing) diisi dengan harga terakhir yang tercatat sebelumnya. Metode ini dipilih karena harga komoditas cenderung bertahan sampai ada perubahan baru.

4. **Backward fill** : Untuk mengisi missing values di awal periode data yang tidak bisa dijangkau oleh forward fill.

5. **Penambahan kolom `is_observed`** : Kolom `is_observed_merah` dan `is_observed_hijau` ditambahkan untuk menandai mana data harga yang asli tercatat (bernilai 1) dan mana yang merupakan hasil imputasi (bernilai 0). Kolom ini penting untuk transparansi kualitas data.

## Statistik Deskriptif (Setelah Preprocessing)

| Statistik | Rawit Merah (Rp) | Rawit Hijau (Rp) |
|---|---|---|
| Jumlah Data | 15.232 | 15.232 |
| Rata-rata | 47.719 | 33.613 |
| Std Deviasi | 21.412 | 12.124 |
| Minimum | 15.000 | 3.000 |
| Q1 (25%) | 30.000 | 25.000 |
| Median (50%) | 40.000 | 30.000 |
| Q3 (75%) | 60.000 | 40.000 |
| Maksimum | 160.000 | 92.000 |

## Analisis Outlier

Deteksi outlier dilakukan menggunakan metode IQR (Interquartile Range):

| Komoditas | Jumlah Outlier | Persentase | Keputusan |
|---|---|---|---|
| Rawit Merah | 85 data | 0,56% | Dipertahankan |
| Rawit Hijau | 411 data | 2,70% | Dipertahankan |

Outlier yang terdeteksi merupakan lonjakan harga valid yang terjadi pada periode Idul Fitri 2025 (Maret sampai April) dan akhir tahun 2023, bukan kesalahan entri data. Outlier tidak dihapus karena model menggunakan Huber Loss yang secara inheren robust terhadap outlier.

## Catatan Penting

- Dataset ini digunakan untuk keperluan penelitian skripsi dengan judul **"Prediksi Harga Cabai Rawit di Kabupaten Banyumas Menggunakan Graph Neural Network (GNN)"**.
- Data ini tidak bersifat real-time dan hanya mencakup periode Januari 2023 sampai Desember 2025.
- Penggunaan data ini di luar konteks penelitian harus memperhatikan bahwa sebagian nilai harga merupakan hasil imputasi (forward fill dan backward fill), yang dapat dilihat melalui kolom `is_observed`.

## Lisensi

Dataset ini disediakan hanya untuk keperluan akademis dan penelitian. Data asli merupakan milik Dinperindag Kabupaten Banyumas dan tersedia secara publik melalui portal SIGAOKMAS.

## Kontak
Email: fathimahellasyarif@gmail.com
Fathimah Ella Syarif
S1 Sistem Informasi, Universitas Telkom Purwokerto
