from qqr import *

def polystr(m, p):
    return " + ".join(f"x^{i}" for i in range(p-1, -1, -1) if m >> i & 1)

p = 11
for S in ([1, 2, 3, 4], [1, 2, 3]):
    a, b = codeword(S, p)
    print(S, "rN rS =", polystr(a, p), "| rQ rS =", polystr(b, p), "| wt", wt((a, b)))
    print("   vector", [a >> i & 1 for i in range(p)] + [b >> i & 1 for i in range(p)])
    J = (1 << p) - 1
    Sc = [x for x in range(p) if x not in S]
    a2, b2 = codeword(Sc, p)
    print("   LQR 3rd,4th:", polystr(a2, p), "|", polystr(b2, p), " LQR wt", wt((a, b, a2, b2)))
X, s = npts([1, 2, 3, 4], 11); print("char sum S={1,2,3,4}:", s)
X, s = npts([x for x in range(11) if x not in (1, 2, 3)], 11); print("char sum S^c, S={1,2,3}:", s)

# LQR closure min distance for p=7,11
for p in (7, 11):
    de, do = weight_dist(p)
    d = min(w for w in range(1, 2*p+1) if de[w]+do[w])
    print(f"p={p}: QQR d={d}; LQR coset => min distance 2d={2*d}; claimed d_p uses max|X|")

# Voloch lemma + p=5 mod 8 extension
for p in [p for p in range(11, 200) if all(p % q for q in range(2, p))]:
    Q, N = sets(p)
    if p % 8 in (1, 3): S, lab = Q, "Q"
    elif p % 8 == 7: S, lab = N, "N"
    else: S, lab = Q+[0], "Q+{0}"
    X, _ = npts(S, p)
    if p < 60: print(p, p % 8, lab, X, round(X-1.5*p, 2))
