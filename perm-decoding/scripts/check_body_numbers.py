#!/usr/bin/env python3
"""Rechecks numerical statements in the body of
paper/perm_decoding_step2_revision.tex that pd_affine.py does not cover:
Example 7.7, Theorem 7.8, Remark 7.9, the table after Corollary 8.2 and
Example 8.3.  Standard library only.  Run:  python3 check_body_numbers.py
"""
from math import comb, floor, log2

ok = True


def check(name, cond):
    global ok
    print(("OK   " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


def primes(lo, hi):
    return [n for n in range(lo, hi + 1) if all(n % d for d in range(2, int(n ** 0.5) + 1))]


# Example 7.7
p, J, T = 17, {0, 1, 2, 3, 4, 7, 9, 10}, {0, 1, 4, 5}
check("Ex 7.7: no affine map sends T into J",
      not any(all((u * x + b) % p in J for x in T) for u in range(1, p) for b in range(p)))
check("Ex 7.7: 272*C(8,4) = 19040 > 2380 = C(17,4)",
      272 * comb(8, 4) == 19040 and comb(17, 4) == 2380)

# Theorem 7.8
check("Thm 7.8: 1332*184756 = 246094992 < 348330136 = C(37,10)",
      37 * 36 == 1332 and comb(20, 10) == 184756
      and 1332 * 184756 == 246094992 and comb(37, 10) == 348330136)


def excluded(p):
    """Dimensions 2 <= k <= p-2 where the counting bound rules out AGL(1,p)."""
    return [k for k in range(2, p - 1)
            if (p - k) // 2 >= 1
            and p * (p - 1) * comb(p - k, (p - k) // 2) < comb(p, (p - k) // 2)]


# Remark 7.9
check("Rem 7.9: counting bound excludes nothing for primes 5 <= p <= 31",
      all(not excluded(q) for q in primes(5, 31)))
check("Rem 7.9: at p = 37 it excludes exactly k = 17..25 and 27",
      excluded(37) == list(range(17, 26)) + [27])

# Table after Corollary 8.2 and Example 8.3
rows = {7: (84, 42, 19, 7), 11: (220, 110, 52, 8), 19: (684, 342, 166, 10),
        23: (1012, 506, 247, 10), 31: (1860, 930, 457, 11)}
good = True
for p, (n, k, tlow, s0) in rows.items():
    g = (p - 1) // 2
    d = n // 2 - g + 1                      # designed distance bound
    good &= (n == 2 * p * (p - 1) and k == n // 2 and (d - 1) // 2 == tlow
             and tlow == ((p - 1) * (2 * p - 1)) // 4
             and s0 == floor(log2(n)) + 1 and s0 <= tlow and 2 ** s0 > n)
check("Table after Cor 8.2: n, k, bound for t, s_0", good)
check("Ex 8.3: m = 44, 84*C(42,7) = 2266179552 < 4529365776 = C(84,7)",
      84 // 2 + 3 - 1 == 44 and 84 * comb(42, 7) == 2266179552
      and comb(84, 7) == 4529365776)
check("Ex 8.3: s = 6 is not excluded by the counting bound",
      84 * comb(42, 6) >= comb(84, 6))

print("\nALL CHECKS PASSED" if ok else "\nSOME CHECKS FAILED")
raise SystemExit(0 if ok else 1)
