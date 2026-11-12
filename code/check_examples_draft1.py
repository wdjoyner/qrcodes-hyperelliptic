"""Checks the examples added in Draft 1 (November 11, 2026).

Example 1.3   (p = 7): the largest #X_S over all non-empty S is 12, attained by
              S = N (odd) and S = {0,1,2,4} (even).
Example 8.2   (p = 7): r_Q R_ev is {0} plus the 7 cyclic shifts of
              x^2+x^4+x^5+x^6, a [7,3,4] code, so d(C_ev) = 4 and M_7 = 12.
Example 8.4   (p = 5): every nonzero word of C_ev has F_4-weight 4 and binary
              weight 4 or 6, so d_4 = 4, d(C_ev) = 4 and M_5 = 8.
Example 9.1   the heuristic constant 2(1 - H^{-1}(1/2)) and its predictions
              for p = 11 and p = 23, against M_11 = 16 and M_23 = 40.

Run from this directory:  python3 check_examples_draft1.py
"""
import itertools
from math import log2
from qqr import npts, sets, mask, mul, rot, codeword, weight_dist


def max_points(p):
    best = {0: (0, []), 1: (0, [])}
    for r in range(1, p + 1):
        for S in itertools.combinations(range(p), r):
            n, _ = npts(S, p)
            par = r % 2
            if n > best[par][0]:
                best[par] = (n, [S])
            elif n == best[par][0]:
                best[par][1].append(S)
    return best


def even_masks(p):
    return [m for m in range(1 << p) if bin(m).count("1") % 2 == 0]


def check_ex_B7():
    p = 7
    Q, N = sets(p)
    assert N == [3, 5, 6]
    assert [(x ** 3 + 1) % p for x in range(p)] == [1, 2, 2, 0, 2, 0, 0]
    assert npts(N, p)[0] == 12
    best = max_points(p)
    assert best[0][0] == 12 and best[1][0] == 12
    assert (0, 1, 2, 4) in best[0][1]
    assert tuple(N) in best[1][1]
    print("Example (p=7, B(c,7)): max #X_S = 12, attained by N and {0,1,2,4}  OK")


def check_ex_pm1_p7():
    p = 7
    Q, N = sets(p)
    words = {mul(mask(Q), m, p) for m in even_masks(p)}
    g = mask([2, 4, 5, 6])
    assert words == {0} | {rot(g, i, p) for i in range(p)}
    assert len(words) == 8
    assert {bin(w).count("1") for w in words if w} == {4}
    # d(C_ev) = 4 and M_7 = 2p + 2 - 4
    dmin = min(sum(bin(x).count("1") for x in codeword(
        [i for i in range(p) if m >> i & 1], p)) for m in even_masks(p) if m)
    assert dmin == 4 and 2 * p + 2 - dmin == 12
    print("Example (p=7, binary QR): [7,3,4], d(C_ev)=4, M_7=12  OK")


def check_ex_pm3_p5():
    p = 5
    w2, w4 = set(), set()
    count = 0
    for m in even_masks(p):
        a, b = codeword([i for i in range(p) if m >> i & 1], p)
        if a == 0 and b == 0:
            continue
        count += 1
        w2.add(bin(a).count("1") + bin(b).count("1"))
        w4.add(bin(a | b).count("1"))
    assert count == 15 and w4 == {4} and w2 == {4, 6}
    assert 2 * p + 2 - min(w2) == 8
    print("Example (p=5, quaternary QR): d_4=4, d(C_ev)=4, M_5=8  OK")


def Hinv_half():
    lo, hi = 0.0, 0.5
    for _ in range(200):
        mid = (lo + hi) / 2
        h = -mid * log2(mid) - (1 - mid) * log2(1 - mid)
        if h < 0.5:
            lo = mid
        else:
            hi = mid
    return lo


def check_ex_heuristic():
    c = 2 * (1 - Hinv_half())
    assert abs(c - 1.7799) < 1e-4
    assert round(11 * c, 1) == 19.6 and round(23 * c, 1) == 40.9
    for p, Mp in ((11, 16), (23, 40)):
        de, _ = weight_dist(p)  # weights of the words c_S with |S| even
        d_ev = min(w for w in range(1, 2 * p + 1) if de[w])
        assert 2 * p + 2 - d_ev == Mp  # Proposition on C_ev
    print("Example (heuristic): c = %.6f, 11c = %.2f, 23c = %.2f  OK"
          % (c, 11 * c, 23 * c))


if __name__ == "__main__":
    check_ex_B7()
    check_ex_pm1_p7()
    check_ex_pm3_p5()
    check_ex_heuristic()
