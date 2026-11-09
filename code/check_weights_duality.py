from qqr import *
import random
random.seed(1)

# 1. weight distributions, dimension, parity structure
for p in [5, 7, 11, 13, 17, 19]:
    de, do = weight_dist(p)
    tot = [a+b for a, b in zip(de, do)]
    # dimension = log2(#distinct codewords); count zero codewords
    zeros = tot[0]
    print(f"p={p} (p%4={p%4}, p%8={p%8}) zero-count={zeros}  dist={tot}")
    print("   even-S weights:", {w: c for w, c in enumerate(de) if c and w}, )
    print("   odd-S  weights:", {w: c for w, c in enumerate(do) if c and w})
    nz = [w for w in range(1, 2*p+1) if tot[w]]
    d = min(nz)
    print("   d =", d, " Rains-type bound 4[p/12]+6 =", 4*(p//12)+6 if p % 4 == 3 else '-')
    # max/min |X_T| over even nonempty T (when weight formula 2p+2-|X_T| applies)
    evw = [w for w in range(1, 2*p+1) if de[w]]
    if p % 4 == 3:
        M = 2*p+2-min(evw); m = 2*p+2-max(evw)
        print(f"   even T: max|X_T|={M}, min|X_T|={m}, M+m={M+m}, 2p+2={2*p+2}, 5p/3-4={5*p/3-4:.2f}")
        print("   all even-S weights = 0 mod 4?", all(w % 4 == 0 for w in evw), " odd-S = 2 mod 4?", all(w % 4 == 2 for w in range(2*p+1) if do[w]))
    else:
        M = 2*p+2-min(evw); m = 2*p+2-max(evw)
        print(f"   even T: max|X_T|={M}, min|X_T|={m}")

# 2. Proposition check on random S
for p in [11, 13, 17, 19, 23, 29]:
    bad = 0
    for _ in range(300):
        k = random.randint(1, p)
        S = random.sample(range(p), k)
        w = wt(codeword(S, p))
        if len(S) % 2 == 0:
            X, s = npts(S, p); pred = 2*p+2-X
        else:
            Sc = [x for x in range(p) if x not in S]
            if not Sc: pred = 0 if p % 4 == 1 else 2*p
            else:
                X, s = npts(Sc, p)
                pred = 2*p+2-X if p % 4 == 1 else X-2
        bad += (w != pred)
    print("Prop check p=%d mismatches=%d" % (p, bad))

# 3. self-duality / LCD
for p in [5, 7, 11, 13, 17, 19, 23, 29]:
    Q, N = sets(p)
    rows = [(rot(mask(N), i, p) << p) | rot(mask(Q), i, p) for i in range(p)]
    k = rank_gf2(rows)
    gram_zero = all((a & b).bit_count() % 2 == 0 for a in rows for b in rows)
    # LCD test: C cap C^perp = 0 iff Gram matrix of a basis is nonsingular
    # take basis rows (first k independent)
    basis = []
    for r in rows:
        if rank_gf2(basis+[r]) > len(basis): basis.append(r)
    G = [sum(((basis[i] & basis[j]).bit_count() % 2) << j for j in range(len(basis))) for i in range(len(basis))]
    print(f"p={p}: k={k}, self-orthogonal={gram_zero}, Gram rank={rank_gf2(G)} of {len(basis)}")
