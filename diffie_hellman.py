from math_utils import mod_exp, is_primitive_root


def diffie_hellman(n, g, x, y):
    if not is_primitive_root(g, n):
        raise ValueError(f"g={g} bukan akar primitif dari p={n}")

    print("[FASE 1] Diffie-Hellman Key Exchange")
    print(f"  Parameter publik : p={n}, g={g}")
    print(f"  Kunci privat     : Lloyd x={x}, Anya y={y}\n")

    X = mod_exp(g, x, n)
    print(f"  Lloyd menghitung X = {g}^{x} mod {n} = {X}  [dikirim ke Anya]")
    Y = mod_exp(g, y, n)
    print(f"  Anya  menghitung Y = {g}^{y} mod {n} = {Y}  [dikirim ke Lloyd]")

    K = mod_exp(Y, x, n)
    print(f"  Lloyd menghitung K  = Y^x mod {n} = {K}")
    K2 = mod_exp(X, y, n)
    print(f"  Anya  menghitung K' = X^y mod {n} = {K2}")

    if K != K2:
        raise RuntimeError("Kunci tidak cocok")
    print(f"\n  ✓ Kunci simetri disepakati: K = {K}\n")
    return X, Y, K


if __name__ == "__main__":
    diffie_hellman(251, 6, 124, 158)