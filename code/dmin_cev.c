/*
 * dmin_cev.c -- exact minimum distance of the even subcode
 *     C_ev = { (r_N u, r_Q u) : u in R, wt(u) even },  R = F_2[x]/(x^p - 1),
 * for primes p = +-3 (mod 8) with p <= 127.  Prints d(C_ev) and M_p = 2p+2-d.
 *
 * Method.  For p = +-3 (mod 8), r_N acts invertibly on the even-weight ideal,
 * so C_ev = { (a, L a) : a of even weight } for a linear map L.  The multiplier
 * x -> n x (n a non-residue) swaps r_Q and r_N, so it maps (a, b) to a codeword
 * whose first half is n*b.  Hence a minimum-weight word may be assumed to have
 * wt(a) <= wt(b).  We enumerate all even-weight a with wt(a) <= t, for
 * t = 2, 4, 6, ...  A word not yet seen has both halves of weight >= t+2, so
 * weight >= 2t+4; once the lightest word found is at most 2t+4, d is exact.
 *
 * Symmetry reductions: cyclic shifts let us put 0 in supp(a).  When
 * p = 3 (mod 4), the maps x -> q x + b (q a residue) also preserve C_ev and,
 * since -1 is a non-residue, any two points of supp(a) can be sent to {0, 1}.
 *
 * Build:  gcc -O3 -march=native -o dmin_cev dmin_cev.c
 * Run:    ./dmin_cev p [tmax]     (default tmax = 12)
 * Timing on one core: p <= 67 in seconds to minutes, p = 83 about 75 minutes.
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned __int128 W;
static int p;
static W MASK;

static int pc(W x) {
    return __builtin_popcountll((unsigned long long)x) +
           __builtin_popcountll((unsigned long long)(x >> 64));
}
static W rot(W a, int k) {
    k %= p;
    if (!k) return a;
    return ((a << k) | (a >> (p - k))) & MASK;
}
static W mul(W a, W b) {
    W r = 0;
    for (int k = 0; k < p; k++)
        if ((b >> k) & 1) r ^= rot(a, k);
    return r;
}

static W col[128];
static int best;

static void dfs(int start, int w, W acc, int target) {
    if (w == target) {
        int c = target + pc(acc);
        if (c < best) best = c;
        return;
    }
    for (int i = start; i < p; i++) dfs(i + 1, w + 1, acc ^ col[i], target);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s p [tmax]\n", argv[0]); return 1; }
    p = atoi(argv[1]);
    int tmax = argc > 2 ? atoi(argv[2]) : 12;
    if (p > 127 || (p % 8 != 3 && p % 8 != 5)) {
        fprintf(stderr, "need a prime p = +-3 (mod 8), p <= 127\n");
        return 1;
    }
    MASK = (((W)1) << p) - 1;
    int isQ[128] = {0};
    for (int i = 1; i < p; i++) isQ[(i * i) % p] = 1;
    W rN = 0, rQ = 0;
    for (int i = 1; i < p; i++) {
        if (isQ[i]) rQ |= ((W)1) << i; else rN |= ((W)1) << i;
    }
    /* Basis u_i = 1 + x^(i+1) of the even-weight ideal; images (r_N u_i, r_Q u_i). */
    int n = p - 1;
    W A[128], B[128];
    int pivbit[128], r = 0;
    for (int i = 0; i < n; i++) {
        W u = 1 | (((W)1) << (i + 1));
        A[i] = mul(rN, u);
        B[i] = mul(rQ, u);
    }
    /* Row-reduce the first halves, carrying the second halves along. */
    for (int bit = 0; bit < p && r < n; bit++) {
        int s = -1;
        for (int i = r; i < n; i++) if ((A[i] >> bit) & 1) { s = i; break; }
        if (s < 0) continue;
        W t = A[s]; A[s] = A[r]; A[r] = t;
        t = B[s]; B[s] = B[r]; B[r] = t;
        for (int i = 0; i < n; i++)
            if (i != r && ((A[i] >> bit) & 1)) { A[i] ^= A[r]; B[i] ^= B[r]; }
        pivbit[r++] = bit;
    }
    if (r != n) { printf("unexpected rank %d\n", r); return 1; }
    /* col[j] = L(1 + x^j); for even a with 0 in supp(a), L a = XOR of col[j], j in supp(a)\{0}. */
    col[0] = 0;
    for (int j = 1; j < p; j++) {
        W v = 1 | (((W)1) << j), out = 0;
        for (int i = 0; i < n; i++)
            if ((v >> pivbit[i]) & 1) { v ^= A[i]; out ^= B[i]; }
        if (v) { printf("vector not in image\n"); return 1; }
        col[j] = out;
    }
    int both = (p % 4 == 3); /* fix {0,1} in supp(a) */
    best = 1000;
    for (int t = 2; t <= tmax; t += 2) {
        if (both) dfs(2, 2, col[1], t); else dfs(1, 1, 0, t);
        int lb = 2 * (t + 2);
        printf("p=%d: lighter half <= %d searched, lightest word %d, lower bound %d%s\n",
               p, t, best, lb, best <= lb ? "  => exact" : "");
        fflush(stdout);
        if (best <= lb) {
            printf("RESULT p=%d d(C_ev)=%d M_p=%d M_p/p=%.3f\n",
                   p, best, 2 * p + 2 - best, (2.0 * p + 2 - best) / p);
            return 0;
        }
    }
    printf("RESULT p=%d: %d <= d(C_ev) <= %d (not settled; raise tmax)\n",
           p, 2 * (tmax + 2), best);
    return 0;
}
