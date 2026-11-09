from qqr import *
import sympy as sp
from math import comb

def mds_coeffs(n, d, q=2):
    A = [0]*(n+1); A[0] = 1
    for w in range(d, n+1):
        A[w] = comb(n, w)*sum((-1)**j*comb(w, j)*(q**(w-d+1-j)-1) for j in range(w-d+1))
    return A

def zeta_poly(A, d, dperp, q=2):
    n = len(A)-1
    r = n+2-d-dperp
    ps = sp.symbols('p0:%d' % (r+1))
    Ms = [mds_coeffs(n, d+i, q) for i in range(r+1)]
    eqs = [sp.Eq(sum(ps[i]*Ms[i][w] for i in range(r+1)), A[w]) for w in range(n+1)]
    sol = sp.solve(eqs, ps, dict=True)[0]
    return [sp.Rational(sol[x]) for x in ps]

def report(name, A, d, dperp):
    P = zeta_poly(A, d, dperp)
    T = sp.symbols('T')
    poly = sp.Poly(sum(c*T**i for i, c in enumerate(P)), T)
    roots = sp.Poly(poly, T).nroots(n=30)
    mods = [abs(complex(z)) for z in roots]
    on = sum(1 for m in mods if abs(m-2**-0.5) < 1e-8)
    print(f"{name}: deg P={poly.degree()}, P(1)={sum(P)}, P1/P0={P[1]/P[0]}, roots on |T|=1/sqrt2: {on}/{len(roots)}")
    return P, mods

# p=7
de, do = weight_dist(7)
A7 = [a+b for a, b in zip(de, do)]
P7, _ = report("p=7 C_NQ", A7, 4, 4)
print("   P7 =", P7)

for p in [11, 19, 23]:
    de, do = weight_dist(p)
    A = [a+b for a, b in zip(de, do)]
    d = min(w for w in range(1, 2*p+1) if A[w])
    if p == 23: print("p=23 dist", A)
    report(f"p={p} C_NQ (self-dual)", A, d, d)

# p = 1 mod 4: C' = C_NQ + <1>
for p in [5, 13, 17, 29]:
    de, do = weight_dist(p)
    A = [(a+b)//2 for a, b in zip(de, do)]
    Ap = [A[w]+A[2*p-w] for w in range(2*p+1)]
    d = min(w for w in range(1, 2*p+1) if Ap[w])
    # check formal self-duality via MacWilliams
    n = 2*p
    x, y = sp.symbols('x y')
    W = sum(Ap[w]*x**(n-w)*y**w for w in range(n+1))
    Wd = sp.expand(W.subs({x: (x+y), y: (x-y)}, simultaneous=True)/2**p)
    fsd = sp.expand(Wd - W) == 0
    print(f"p={p}: C' dist={Ap}, d={d}, formally self-dual={fsd}")
    if p in (13, 17, 29):
        P, mods = report(f"p={p} C'", Ap, d, d)
        if p == 13: print("   P13 =", P)
