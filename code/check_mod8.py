"""Checks for Section 7 (the split by p mod 8).

p = +-1 (mod 8), Proposition 7.1:
  on the even-weight ideal R_ev, r_Q and r_N are complementary orthogonal
  idempotents, so C_ev = (r_N R_ev, 0) + (0, r_Q R_ev), and
  d(C_ev) is the minimum distance of the even-like binary QR code.
p = +-3 (mod 8), Proposition 7.2:
  C_ev is closed under (a, b) -> (b, a + b), hence F_4-linear, and
  d_4 <= d(C_ev) <= (4/3) d_4 for the F_4 weight d_4 = min wt(a | b).

Exhaustive enumeration, so keep p small (about a minute in total).
"""
from qqr import sets, mask, mul


def even_basis(p):
    return [(1 << i) | (1 << (i + 1)) for i in range(p - 1)]


def span_min(vecs, weight):
    """Minimum of weight(v) over nonzero v in the F_2-span of vecs (Gray code)."""
    best, cur = None, 0
    basis = vecs
    for g in range(1, 1 << len(basis)):
        cur ^= basis[(g & -g).bit_length() - 1]
        w = weight(cur)
        if w and (best is None or w < best):
            best = w
    return best


def reduce_basis(vecs):
    piv = {}
    for v in vecs:
        while v:
            h = v.bit_length() - 1
            if h in piv:
                v ^= piv[h]
            else:
                piv[h] = v
                break
    return list(piv.values())


def check_pm1(p):
    Q, N = sets(p)
    rQ, rN = mask(Q), mask(N)
    for u in even_basis(p):
        assert mul(rQ, mul(rQ, u, p), p) == mul(rQ, u, p)        # r_Q idempotent on R_ev
        assert mul(rQ, mul(rN, u, p), p) == 0                     # r_Q r_N = 0 on R_ev
        assert mul(rQ, u, p) ^ mul(rN, u, p) == u                 # r_Q + r_N = 1 on R_ev
    qr = reduce_basis([mul(rQ, u, p) for u in even_basis(p)])
    d = span_min(qr, lambda v: bin(v).count("1"))
    print(f"p={p:2d} (= {p % 8} mod 8): C_ev = QR_ev + QR_ev, dim QR_ev = {len(qr)}, "
          f"d = {d}, M_p = {2*p + 2 - d}")


def check_pm3(p):
    Q, N = sets(p)
    rQ, rN = mask(Q), mask(N)
    words = [(mul(rN, u, p), mul(rQ, u, p)) for u in even_basis(p)]
    # pack (a, b) into one integer: a in the low p bits, b in the high p bits
    packed = reduce_basis([a | (b << p) for a, b in words])
    full = (1 << p) - 1
    span = set()
    cur = 0
    span.add(0)
    for g in range(1, 1 << len(packed)):
        cur ^= packed[(g & -g).bit_length() - 1]
        span.add(cur)
    for v in packed:                                              # closure under omega
        a, b = v & full, v >> p
        assert (b | ((a ^ b) << p)) in span
    dbin = min(bin(v).count("1") for v in span if v)
    d4 = min(bin((v & full) | (v >> p)).count("1") for v in span if v)
    assert d4 <= dbin <= 4 * d4 / 3
    print(f"p={p:2d} (= {p % 8} mod 8): C_ev is F_4-linear, d_4 = {d4}, "
          f"d(C_ev) = {dbin}, M_p = {2*p + 2 - dbin}")


if __name__ == "__main__":
    for p in (7, 17, 23, 31, 41):
        check_pm1(p)
    for p in (5, 11, 13, 19):
        check_pm3(p)
