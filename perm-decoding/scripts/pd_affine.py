#!/usr/bin/env python3
"""
Exhaustive test of AGL(1,p) as a full permutation-decoding (PD) set for the
full-length Reed--Solomon codes RS(F_p, k), relative to every information set.

For RS(F_p,k) (an MDS code) every k-subset I of F_p is an information set;
J = F_p \\ I is the set of check positions, and t = floor((p-k)/2).
AGL(1,p) is a full PD-set relative to I iff for every t-subset T of F_p
there is an affine map s with s(T) contained in J, i.e. s(T) & I == 0.

Two symmetry reductions are used:
  * The answer depends only on the AGL(1,p)-orbit of I.
  * For fixed I, "T is covered" depends only on the AGL(1,p)-orbit of T
    (if s(T) lies in J then (s r^{-1})(r(T)) does too).
So we test one representative I per orbit against all images of one
representative T per orbit.  Subsets are stored as integer bit masks.

Usage:  python3 pd_affine.py p [kmin kmax]
Requires numpy.  Runs in Sage as well (use `sage -python`).
"""
import sys, time
from itertools import combinations
from math import comb
import numpy as np

def affine_maps(p):
    return [[(u*x + b) % p for x in range(p)]
            for u in range(1, p) for b in range(p)]

def mask(S):
    m = 0
    for i in S:
        m |= 1 << i
    return m

def image(mp, S):
    return mask(mp[i] for i in S)

def orbit_reps(p, k, maps):
    """One representative (as a tuple) and orbit size for each AGL-orbit of k-subsets."""
    seen, reps = set(), []
    for S in combinations(range(p), k):
        m = mask(S)
        if m in seen:
            continue
        orb = {image(mp, S) for mp in maps}
        seen |= orb
        reps.append((S, len(orb)))
    return reps

def analyze(p, k, maps):
    t = (p - k) // 2
    Ireps = orbit_reps(p, k, maps)
    Treps = orbit_reps(p, t, maps)
    # all images of all T-representatives, grouped by representative
    imgs = np.array([[image(mp, T) for mp in maps] for T, _ in Treps],
                    dtype=np.int64)            # shape (#Treps, |AGL|)
    bad = []
    for I, size in Ireps:
        Im = np.int64(mask(I))
        covered = ((imgs & Im) == 0).any(axis=1)   # per T-representative
        if not covered.all():
            T = Treps[int(np.argmin(covered))][0]
            J = tuple(sorted(set(range(p)) - set(I)))
            bad.append((J, T, size))
    return t, Ireps, bad

def main():
    p = int(sys.argv[1])
    kmin = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else p - 2
    maps = affine_maps(p)
    G = len(maps)
    print(f"p = {p}, |AGL(1,p)| = {G}")
    for k in range(kmin, kmax + 1):
        t0 = time.time()
        t, Ireps, bad = analyze(p, k, maps)
        nb = sum(s for _, _, s in bad)
        cnt = "ok" if G*comb(p-k, t) >= comb(p, t) else "FAILS"
        print(f"k={k:2d} t={t:2d}  failing orbits {len(bad):5d}/{len(Ireps):6d}"
              f"  failing info sets {nb:8d}/{comb(p,k):8d}"
              f"  counting bound {cnt}  ({time.time()-t0:.1f}s)")
        for J, T, _ in bad[:3]:
            print(f"      e.g. J = {list(J)}  uncovered T = {list(T)}")
        sys.stdout.flush()

if __name__ == "__main__":
    main()
