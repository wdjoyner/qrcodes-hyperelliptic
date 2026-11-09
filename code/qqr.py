import sys, random
from fractions import Fraction

def chi(a, p):
    a %= p
    if a == 0: return 0
    return 1 if pow(a, (p-1)//2, p) == 1 else -1

def sets(p):
    Q = sorted({(x*x) % p for x in range(1, p)})
    N = [x for x in range(1, p) if x not in Q]
    return Q, N

def mask(S):
    m = 0
    for s in S: m |= 1 << s
    return m

def rot(m, i, p):
    i %= p
    full = (1 << p) - 1
    return ((m << i) | (m >> (p - i))) & full

def mul(a, b, p):
    r = 0
    i = 0
    while a:
        if a & 1: r ^= rot(b, i, p)
        a >>= 1; i += 1
    return r

def npts(S, p):
    """|X_S(GF(p))| on smooth projective model, S nonempty."""
    s = sum(chi(prod_minus(a, S, p), p) for a in range(p))
    return s + p + (2 if len(S) % 2 == 0 else 1), s

def prod_minus(a, S, p):
    r = 1
    for t in S: r = r * (a - t) % p
    return r

def codeword(S, p):
    Q, N = sets(p)
    rs = mask(S)
    return mul(mask(N), rs, p), mul(mask(Q), rs, p)

def wt(c): return sum(bin(x).count('1') for x in c)

def weight_dist(p):
    """Gray-code enumeration; returns dist for even-|S| and odd-|S| parts."""
    Q, N = sets(p)
    rows = [(rot(mask(N), i, p) << p) | rot(mask(Q), i, p) for i in range(p)]
    de = [0]*(2*p+1); do = [0]*(2*p+1)
    cur = 0; par = 0
    de[0] += 1
    for k in range(1, 1 << p):
        i = (k & -k).bit_length() - 1
        cur ^= rows[i]; par ^= 1
        w = cur.bit_count()
        if par: do[w] += 1
        else: de[w] += 1
    return de, do

def rank_gf2(vecs):
    basis = {}
    r = 0
    for v in vecs:
        while v:
            h = v.bit_length() - 1
            if h in basis: v ^= basis[h]
            else:
                basis[h] = v; r += 1; break
    return r
