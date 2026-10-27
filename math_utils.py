def is_prime(n):
    if n < 2:
        return False
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True


def mod_exp(base, exp, mod):
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = result * base % mod
        base = base * base % mod
        exp >>= 1
    return result


def mod_inverse(a, m):
    old_r, r = a % m, m
    old_s, s = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    if old_r != 1:
        raise ValueError(f"{a} tidak punya invers mod {m}")
    return old_s % m


def is_primitive_root(g, p):
    if not is_prime(p):
        return False
    seen = set()
    x = 1
    for _ in range(p - 1):
        x = x * g % p
        seen.add(x)
    return len(seen) == p - 1