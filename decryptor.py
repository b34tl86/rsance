#!/usr/bin/env python3
# search_batch_gcd_stdlib.py -- pure stdlib batch-gcd

from math import gcd
import sys

# ---------- Values pasted ----------
N = **
e = **
c = **
# ----------------------------------

def long_to_bytes(n: int) -> bytes:
    if n == 0:
        return b"\x00"
    return n.to_bytes((n.bit_length() + 7) // 8, "big")

# Tunable bounds
MAX_R = 1 << 14     # 16384
MAX_ER = 1 << 11    # 2048  (batch size per r; adjust)

def try_batch_search(max_r=MAX_R, max_er=MAX_ER):
    print("Batch search: max_r =", max_r, "batch size per r =", max_er)
    for r in range(1, max_r):
        if (r & 0x3FF) == 0:
            print("r =", r)
        A = e * r - 1
        P = 1
        # product of terms modulo N
        for er in range(1, max_er):
            K = (e + A * er) % N
            P = (P * K) % N
        g = gcd(P, N)
        if 1 < g < N:
            print("Found factor for r=", r, "g =", g)
            return r, g
    return None

if __name__ == "__main__":
    res = try_batch_search()
    if res is None:
        print("No factor found in the searched ranges.")
        sys.exit(0)
    r, g = res
    p = g
    q = N // p
    phi = (p - 1) * (q - 1)
    try:
        d = pow(e, -1, phi)
    except ValueError:
        print("Failed to invert e mod phi")
        sys.exit(1)
    m = pow(c, d, N)
    pt = long_to_bytes(m)
    print("Recovered plaintext bytes:", pt)
    print("As UTF-8 (best effort):", pt.decode("utf-8", errors="replace"))
