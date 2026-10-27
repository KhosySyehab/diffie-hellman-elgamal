# **Planning Tugas Kriptografi: Diffie-Hellman & ElGamal**

## **Studi Kasus: Misi Rahasia Twilight**

> **Lloyd Forger** (codename: Twilight) adalah agen mata-mata yang harus mengirim
> laporan intel lapangan kepada **Anya**, rekan operasinya di markas.
> Masalahnya, musuh sedang memantau semua jalur komunikasi.
>
> Lloyd menggunakan **Diffie-Hellman** untuk menyepakati kunci rahasia dengan Anya
> tanpa harus bertemu langsung, lalu **ElGamal** untuk mengenkripsi pesan `"INTEL"`
> agar tidak bisa dibaca seorangpun — bahkan orang yang bisa membaca pikiran sekalipun! 

```
Pengirim   :  Lloyd (Alice) — mengenkripsi laporan
Penerima   :  Anya  (Bob)  — mendekripsi dengan kunci privat
Pesan Asli :  "INTEL"
```

---

## **Arsitektur Program**

```
main.py
├── math_utils.py        ← Orang 1
├── diffie_hellman.py    ← Orang 1
└── elgamal.py           ← Orang 2
```

```
FASE 1 — Diffie-Hellman Key Exchange
  → Lloyd & Anya menyepakati kunci rahasia bersama lewat saluran publik

FASE 2 — ElGamal Key Generation
  → Anya membangkitkan kunci publik & privat

FASE 3 — ElGamal Encryption
  → Lloyd mengenkripsi "INTEL" menggunakan kunci publik Anya

FASE 4 — ElGamal Decryption
  → Anya mendekripsi ciphertext kembali menjadi "INTEL"
```

---

## **Pembagian Jobdesk — Sekuensial**

> [!IMPORTANT]
> **Orang 1 harus selesai dan menyerahkan semua file sebelum Orang 2 boleh mulai.**
> Orang 2 menggunakan fungsi dari Orang 1 secara langsung via import.

---

### Orang 1 — Fondasi Matematika + Diffie-Hellman
**Mengerjakan:** `math_utils.py` dan `diffie_hellman.py`

| No | Fungsi | Deskripsi |
|----|--------|-----------|
| 1 | `is_prime(n)` | Cek apakah n adalah bilangan prima (trial division) |
| 2 | `mod_exp(base, exp, mod)` | Modular exponentiation cepat (square & multiply) |
| 3 | `mod_inverse(a, p)` | Modular inverse dengan Extended Euclidean Algorithm |
| 4 | `is_primitive_root(g, p)` | Cek apakah g adalah akar primitif dari p |
| 5 | `diffie_hellman(n, g, x, y)` | Jalankan DH Key Exchange, print semua tahapan step-by-step |

**Yang diserahkan ke Orang 2 (setelah selesai & diuji):**
- `math_utils.py` — fungsi no. 1–4
- `diffie_hellman.py` — fungsi no. 5
- Nilai `p`, `g`, dan `K` yang dipakai agar Orang 2 bisa lanjut

**Test Case Validasi (dari materi):**
```
Input : n=251, g=6, x_lloyd=124, y_anya=158
Output: X=209, Y=197, K=K'=79  ✓
```

---

### **Orang 2 — ElGamal + Main Program**
**Mengerjakan:** `elgamal.py` dan `main.py`

**Mulai SETELAH menerima file dari Orang 1.**

| No | Fungsi | Deskripsi |
|----|--------|-----------|
| 1 | `text_to_blocks(text, p)` | Konversi teks → list blok integer (A=00, B=01, ..., Z=25) |
| 2 | `elgamal_keygen(p, g, x)` | Hasilkan kunci publik `y = g^x mod p` |
| 3 | `elgamal_encrypt(m, p, g, y, k)` | Enkripsi blok m → (a, b), print tiap tahap |
| 4 | `elgamal_decrypt(a, b, p, x)` | Dekripsi (a, b) → m, print tiap tahap |
| 5 | `blocks_to_text(blocks)` | Konversi list blok integer → teks kembali |
| 6 | `main()` | Rangkai semua fase dalam 1 studi kasus misi rahasia Lloyd & Anya |

> **Catatan:** `mod_exp` dan `mod_inverse` langsung di-import dari `math_utils.py`
> buatan Orang 1. Tidak perlu implementasi ulang.

**Test Case Validasi (dari materi):**
```
Input : p=2273, g=3, x=243, pesan="HALO"
y=461, m1=0700, m2=1114
Output enkripsi : c1=(1439,74), c2=(1220,1682)
Output dekripsi : "HALO" ✓
```

---

## **Timeline Pengerjaan**

```
Hari 1 — Orang 1
  ├── Implementasi is_prime, mod_exp, mod_inverse
  └── Implementasi is_primitive_root, uji semua dengan contoh materi

Hari 2 — Orang 1
  ├── Implementasi & uji Diffie-Hellman lengkap (step-by-step output)
  └── SERAHKAN math_utils.py + diffie_hellman.py ke Orang 2

Hari 3 — Orang 2
  ├── Import file Orang 1
  ├── Implementasi text_to_blocks, blocks_to_text
  ├── Implementasi elgamal_keygen & elgamal_encrypt
  └── Implementasi elgamal_decrypt

Hari 4 — Orang 2
  ├── Rakit main.py — studi kasus misi Lloyd & Anya end-to-end
  ├── Verifikasi output sesuai test case
  └── Tulis laporan & packaging ZIP
```

---

## **Format Laporan & ZIP**

```
Kelompok_X_NamaAnggota1_NamaAnggota2.zip
├── laporan.pdf
│   ├── Cover + Identitas Kelompok (Kelompok X: Nama1, Nama2)
│   ├── Studi Kasus (deskripsi skenario misi rahasia Lloyd & Anya)
│   ├── Teori Diffie-Hellman           ← Orang 1 yang nulis
│   ├── Teori ElGamal                  ← Orang 2 yang nulis
│   ├── Penjelasan fungsi + screenshot output
│   └── Kesimpulan
├── math_utils.py
├── diffie_hellman.py
├── elgamal.py
└── main.py
```

---

## Checklist Final

**Orang 1 (sebelum serah terima ke Orang 2):**
- [ ] `is_prime(n)` — diuji ✔
- [ ] `mod_exp(base, exp, mod)` — diuji dengan contoh materi ✔
- [ ] `mod_inverse(a, p)` — diuji ✔
- [ ] `is_primitive_root(g, p)` — diuji ✔
- [ ] `diffie_hellman()` — output X, Y, K, K' sesuai contoh materi ✔

**Orang 2 (sebelum submit):**
- [ ] `text_to_blocks()` & `blocks_to_text()` — diuji dengan "INTEL" ✔
- [ ] `elgamal_keygen()` — diuji ✔
- [ ] `elgamal_encrypt()` — output (a, b) sesuai test case ✔
- [ ] `elgamal_decrypt()` — output teks asli kembali ✔
- [ ] `main()` — studi kasus Lloyd & Anya berjalan end-to-end ✔
- [ ] **Tidak ada library eksternal** ✔
- [ ] Laporan lengkap + identitas kelompok ✔
- [ ] File dikemas dalam format ZIP ✔

---

## Contoh Output Program (Target)

```
=====================================================
      SISTEM KOMUNIKASI RAHASIA — OPERASI STRIX
=====================================================

[FASE 1] Diffie-Hellman Key Exchange
  Lloyd dan Anya menyepakati parameter publik: p=251, g=6
  Lloyd memilih kunci privat: x=124
  Anya  memilih kunci privat: y=158
  Lloyd menghitung X = g^x mod p = 6^124 mod 251 = 209  [dikirim ke Anya]
  Anya  menghitung Y = g^y mod p = 6^158 mod 251 = 197  [dikirim ke Lloyd]
  Lloyd menghitung K  = Y^x mod p = 197^124 mod 251 = 79
  Anya  menghitung K' = X^y mod p = 209^158 mod 251 = 79
  ✓ Kunci simetri berhasil disepakati: K = 79

[FASE 2] ElGamal Key Generation (Anya)
  Parameter: p=2273, g=3
  Anya memilih kunci privat: x=243
  Kunci publik: y = g^x mod p = 3^243 mod 2273 = 461

[FASE 3] Enkripsi Laporan Intel (Lloyd → Anya)
  Lloyd mengenkripsi pesan: "INTEL"
  Konversi: I=08, N=13, T=19, E=04, L=11
  m = 0813190411
  Blok: m1=0813, m2=1904, m3=0011
  Enkripsi m1 (k=...): a=..., b=... → c1=(a1, b1)
  Enkripsi m2 (k=...): a=..., b=... → c2=(a2, b2)
  Enkripsi m3 (k=...): a=..., b=... → c3=(a3, b3)

[FASE 4] Dekripsi (Anya)
  Dekripsi c1 → 0813
  Dekripsi c2 → 1904
  Dekripsi c3 → 0011
  ✓ Pesan berhasil didekripsi: "INTEL"

=====================================================
   Misi sukses. Bahkan pembaca pikiran pun
   tidak bisa mencuri pesan yang terenkripsi! 🧠
=====================================================
```
