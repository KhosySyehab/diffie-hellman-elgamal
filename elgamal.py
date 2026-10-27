from math_utils import mod_exp


# ---------------------------------------------------------------------------
# Konversi teks ↔ blok integer
# Setiap huruf direpresentasikan sebagai 2 digit: A=00, B=01, ..., Z=25
# Blok dibuat sepanjang block_size digit, di mana block_size = len(str(p-1))
# Contoh (p=2273 → block_size=4): "HALO" → [700, 1114]
# ---------------------------------------------------------------------------

def text_to_blocks(text, p):
    """Ubah teks ke list blok integer, tiap blok < p.

    Langkah:
    1. Setiap huruf → 2 digit  (A=00 … Z=25)
    2. Gabungkan semua digit
    3. Potong menjadi blok block_size digit (padding '00' jika perlu)
    """
    digits = ''.join(f'{ord(c.upper()) - ord("A"):02d}'
                     for c in text if c.isalpha())
    block_size = len(str(p - 1))           # p=2273 → 4, p=251 → 3
    # padding agar panjang digit kelipatan block_size
    while len(digits) % block_size:
        digits += '00'
    return [int(digits[i:i + block_size])
            for i in range(0, len(digits), block_size)]


def blocks_to_text(blocks, p, trim=None):
    """Kembalikan list blok integer ke teks.

    Args:
        blocks    : list integer hasil dekripsi
        p         : bilangan prima yang dipakai (menentukan block_size)
        trim      : potong hasil ke panjang ini (untuk buang padding)
    """
    block_size = len(str(p - 1))
    # format tiap blok kembali ke string digit sepanjang block_size
    digits = ''.join(f'{b:0{block_size}d}' for b in blocks)
    # baca 2 digit sekaligus → 1 huruf
    chars = []
    for i in range(0, len(digits), 2):
        val = int(digits[i:i + 2])
        if 0 <= val <= 25:
            chars.append(chr(val + ord('A')))
    text = ''.join(chars)
    return text[:trim] if trim is not None else text


# ---------------------------------------------------------------------------
# Pembangkitan kunci
# ---------------------------------------------------------------------------

def elgamal_keygen(p, g, x):
    """Bangkitkan kunci publik y = g^x mod p.

    Args:
        p : bilangan prima (publik)
        g : akar primitif dari p (publik)
        x : kunci privat (1 < x < p-1)

    Returns:
        y : kunci publik
    """
    return mod_exp(g, x, p)


# ---------------------------------------------------------------------------
# Enkripsi
# ---------------------------------------------------------------------------

def elgamal_encrypt(m, p, g, y, k):
    """Enkripsi blok plaintext m menjadi ciphertext (a, b).

    Rumus:
        a = g^k  mod p
        b = y^k * m  mod p

    Args:
        m : plaintext block (integer)
        p : bilangan prima
        g : akar primitif dari p
        y : kunci publik penerima
        k : bilangan acak (1 < k < p-1), dipilih pengirim

    Returns:
        (a, b) : pasangan ciphertext
    """
    a = mod_exp(g, k, p)
    b = mod_exp(y, k, p) * m % p
    return a, b


# ---------------------------------------------------------------------------
# Dekripsi
# ---------------------------------------------------------------------------

def elgamal_decrypt(a, b, p, x):
    """Dekripsi ciphertext (a, b) menjadi plaintext m.

    Rumus:
        m = b * (a^x)^{-1}  mod p
          = b * a^{p-1-x}   mod p   (Fermat: a^{p-1} ≡ 1 mod p)

    Args:
        a, b : ciphertext
        p    : bilangan prima
        x    : kunci privat penerima

    Returns:
        m : plaintext block (integer)
    """
    ax_inv = mod_exp(a, p - 1 - x, p)   # (a^x)^{-1} mod p
    return b * ax_inv % p
