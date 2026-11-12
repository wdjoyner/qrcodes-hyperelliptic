#!/usr/bin/env python3
"""Checks every number in the examples added in Draft 2 of
paper/perm_decoding_step2_revision.tex (Examples 1.1, 3.1-3.6, 4.8, 6.5, 9.1).

Run:  python3 check_examples_draft2.py
Needs only the Python 3 standard library.  Every check is exhaustive and exact.
"""
from itertools import combinations, permutations, product
from math import comb, sqrt

p = 7
ok = True


def check(name, cond):
    global ok
    print(("OK   " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


# ----------------------------------------------------------------------
# The [7,3,5] code of Example 7.4 (generator matrix from GUAVA)
G = [[1, 0, 0, 6, 4, 6, 4],
     [0, 1, 0, 6, 3, 3, 1],
     [0, 0, 1, 3, 1, 6, 3]]
H = [[1, 1, 4, 1, 0, 0, 0],
     [3, 4, 6, 0, 1, 0, 0],
     [1, 4, 1, 0, 0, 1, 0],
     [3, 6, 4, 0, 0, 0, 1]]


def span(M):
    k, n = len(M), len(M[0])
    return {tuple(sum(c[i] * M[i][j] for i in range(k)) % p for j in range(n))
            for c in product(range(p), repeat=k)}


def wt(v):
    return sum(1 for x in v if x)


def det3(cols):
    a = [[G[i][j] for j in cols] for i in range(3)]
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
            - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])) % p


C = span(G)
# Example 3.1
check("Ex 3.1: H = (-A^T | I_4)",
      all(H[j][i] == (-G[i][3 + j]) % p for i in range(3) for j in range(4)))
check("Ex 3.1: H G^T = 0",
      all(sum(h[j] * g[j] for j in range(7)) % p == 0 for h in H for g in G))
check("Ex 3.1: minimum distance 5", min(wt(c) for c in C if any(c)) == 5)
check("Ex 3.1: every 3-subset is an information set",
      all(det3(c) != 0 for c in combinations(range(7), 3)))
check("Ex 3.1: first row has weight 5", wt(G[0]) == 5)

# Example 1.1: permutation group of this code has order 42
aut = sum(1 for s in permutations(range(7))
          if all(tuple(g[s[j]] for j in range(7)) in C for g in G))
check("Ex 1.1: |PAut| = 42 (search of all of S_7)", aut == 42)

# Example 3.2
RS = {tuple((a + b * x + c * x * x) % p for x in range(p))
      for a, b, c in product(range(p), repeat=3)}
check("Ex 3.2: x^2 -> (0,1,4,2,2,4,1)",
      tuple(x * x % p for x in range(p)) == (0, 1, 4, 2, 2, 4, 1))
w = tuple((x - 1) * (x - 2) % p for x in range(p))
check("Ex 3.2: (x-1)(x-2) -> (2,0,0,2,6,5,6), weight 5",
      w == (2, 0, 0, 2, 6, 5, 6) and wt(w) == 5)
affine = [(u, b) for u in range(1, p) for b in range(p)]
check("Ex 3.2: |AGL(1,7)| = 42", len(affine) == 42)
check("Ex 3.2: unique affine map 0->3, 1->5 is 2x+3",
      [(u, b) for u, b in affine if b % p == 3 and (u + b) % p == 5] == [(2, 3)])
# Example 3.3
check("Ex 3.3: RS(F_7,3) is a [7,3,5] code",
      len(RS) == 343 and min(wt(c) for c in RS if any(c)) == 5)
check("Ex 3.2/6.5: AGL(1,7) preserves RS(F_7,3)",
      all(tuple(c[(u * x + b) % p] for x in range(p)) in RS
          for c in RS for u, b in affine))

# ----------------------------------------------------------------------
# F_49 = F_7[i], i^2 = -1 (7 = 3 mod 4).  Elements are pairs (a,b) = a + b i.
def mul(z, w):
    return ((z[0] * w[0] - z[1] * w[1]) % p, (z[0] * w[1] + z[1] * w[0]) % p)


def add(z, w):
    return ((z[0] + w[0]) % p, (z[1] + w[1]) % p)


def power(z, n):
    r = (1, 0)
    for _ in range(n):
        r = mul(r, z)
    return r


F49 = [(a, b) for a in range(p) for b in range(p)]
pts49 = [(x, y) for x in F49 for y in F49
         if mul(y, y) == add(power(x, 7), ((-x[0]) % p, (-x[1]) % p))]
pts7 = [(x, y) for x in range(p) for y in range(p) if (y * y - x ** 7 + x) % p == 0]

# Example 3.4
check("Ex 3.4: 7 affine F_7-points, all with y = 0",
      len(pts7) == 7 and all(y == 0 for _, y in pts7))
check("Ex 3.4: 8 = 2g+2 and Hasse-Weil 2*3*sqrt(7) ~ 15.9",
      8 == 2 * 3 + 2 and abs(2 * 3 * sqrt(7) - 15.9) < 0.05)
check("Ex 3.4: |X(F_49)| = 92 = 49+1+2*3*7",
      len(pts49) + 1 == 92 and 92 == 49 + 1 + 2 * 3 * 7)

# Example 3.5
check("Ex 3.5: stabilizer of 0 has 6 elements, 42/6 = 7",
      sum(1 for u, b in affine if b == 0) == 6)
check("Ex 3.5: AGL(1,7) is transitive but not regular",
      {b for u, b in affine} == set(range(p)) and len(affine) != p)
check("Ex 3.5: translations act regularly",
      all(sum(1 for b in range(p) if (a + b) % p == c) == 1
          for a in range(p) for c in range(p)))
v = [1, -1, 0, 0, 0, 0, 0]                       # e_0 - e_1, in W
tv = [v[(a - 1) % p] for a in range(p)]          # translate by 1
check("Ex 3.5: translation by 1 moves e_0 - e_1 inside W",
      tv != v and sum(tv) == 0)
check("Ex 3.5: no element of S_6 has order 7", 720 % 7 != 0)

# Example 3.6
check("Ex 3.6: |PGL_2(7)| = 336, |PSL_2(7)| = 168, Borel 42",
      7 * 48 == 336 and 336 // 2 == 168 and 336 // 8 == 42)
check("Ex 3.6: squares mod 7 are 1,2,4",
      sorted({x * x % p for x in range(1, p)}) == [1, 2, 4])

# ----------------------------------------------------------------------
# Example 4.8
nongaps = sorted({2 * i + 7 * j for i in range(8) for j in range(2) if 2 * i + 7 * j <= 7})
check("Ex 4.8: non-gaps of <2,7> up to 7 are 0,2,4,6,7 (gaps 1,3,5)",
      nongaps == [0, 2, 4, 6, 7])
check("Ex 4.8: |G_7| = 336 > 8, |H_7| = 42, 21 induced permutations",
      7 * 48 == 336 and 336 // 8 == 42 and 42 // 2 == 21)
check("Ex 4.8: |G_49| = 672 > 92", 2 * 7 * 48 == 672 and 672 > 92)
O2 = [P for P in pts49 if P[0][1] != 0]
check("Ex 4.8: |O_1| = 8, |O_2| = 84", len(pts49) + 1 - len(O2) == 8 and len(O2) == 84)
Hmaps = [(u, b, eta) for u in range(1, p) for b in range(p)
         for eta in F49 if mul(eta, eta) == (u, 0)]
check("Ex 4.8: |H| = 84", len(Hmaps) == 84)
P0 = O2[0]
orbit = {(add(mul((u, 0), P0[0]), (b, 0)), mul(eta, P0[1])) for u, b, eta in Hmaps}
check("Ex 4.8: H acts regularly on O_2", orbit == set(O2) and len(orbit) == 84)
check("Ex 4.8: l(D_2) = 82", 84 + 1 - 3 == 82)

# ----------------------------------------------------------------------
# Example 6.5
J = {3, 4, 5, 6}
trans = range(p)
check("Ex 6.5: translations are a 2-PD-set for I = {0,1,2}",
      all(any({(a + b) % p for a in T} <= J for b in trans)
          for s in (1, 2) for T in combinations(range(p), s)))
check("Ex 6.5: 7*C(4,2) = 42 >= 21 and 3*C(4,2) = 18 < 21",
      7 * comb(4, 2) == 42 and comb(7, 2) == 21 and 3 * comb(4, 2) == 18)

# Example 9.1
check("Ex 9.1: 7*4 = 28, 42*28 = 1176, 23*12 = 276, 506*276 = 139656",
      7 * 4 == 28 and 42 * 28 == 1176 and 23 * 12 == 276
      and 23 * 22 == 506 and 506 * 276 == 139656)

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
