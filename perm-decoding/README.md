# Permutation decoding of AG codes from y² = xᵖ − x

This folder accompanies

> D. Joyner, ChatGPT (OpenAI), Claude (Anthropic),
> *Conjectural permutation decoding of some AG codes — corrected and expanded version* (2026),

which revises

> D. Joyner, *Conjectural permutation decoding of some AG codes*,
> ACM SIGSAM Bulletin **39**(1) (2005), 26–32,
> [doi:10.1145/1080368.1080374](https://dl.acm.org/doi/10.1145/1080368.1080374).

The 2005 note made two conjectures about permutation decoding of one-point AG
codes on the hyperelliptic curve y² = xᵖ − x. The revision shows that both
fail as universal statements. It also proves what does hold and lists open
problems.

## Contents

**Current version**

| Path | Description |
|---|---|
| `paper/perm_decoding_step2_revision.tex` / `.pdf` | The corrected and expanded version, Draft 2 (12pt Times, US letter), including the p = 23 results |
| `paper/revision-log.tex` / `.pdf` | Revision log: a reconstructed account of the changes from the 2005 note to Draft 1, and every change in Draft 2, with a concordance of numbers |
| `scripts/pd_affine.py` | Exhaustive test of AGL(1,p) as a full PD-set for RS(F_p, k) |
| `scripts/check_examples_draft2.py` | Checks every number in the examples added in Draft 2 |
| `scripts/check_body_numbers.py` | Rechecks the other numerical statements of the paper (Example 7.7, Theorem 7.8, Remark 7.9, Section 8) |
| `results/agl_pd_p*.txt` | Output of `pd_affine.py` for p = 5, 7, 11, 13, 17, 19, 23 |

**History**

| Path | Description |
|---|---|
| `perm_decoding1.tex`, `perm_decoding2.tex` (+ `.dvi`) | Earlier drafts of the 2005 note |
| `perm_decoding3.tex` / `.pdf` (+ `.dvi`) | The 2005 note, the starting point for the 2026 revision |
| `perm_decoding_step1_mathematical_revision.tex` / `.pdf` | Step 1: first mathematical revision, prepared with ChatGPT |
| `perm-decoding_revision-2026.tex` / `.pdf` | An intermediate Step 2 draft (before the title was restored and the p = 23 results were added); superseded by `paper/` |

The Step 1 revision was refereed by Claude. ChatGPT's response to that report and the referee's corrections were then combined into Step 2, the version in `paper/`.

## The computation

For p prime, the length-p one-point codes over F_p are the Reed–Solomon codes
RS(F_p, k). Their permutation group is the affine group AGL(1,p) =
{x ↦ ux + b}, of order p(p − 1). Every k-subset I of F_p is an information
set (the code is MDS). Let J be its complement and t = ⌊(p − k)/2⌋.

AGL(1,p) is a **full PD-set relative to I** if every t-subset T of F_p
can be moved into J by some affine map.

`pd_affine.py` decides this for **every** information set and every
2 ≤ k ≤ p − 2, using two reductions:

1. The answer depends only on the AGL(1,p)-orbit of I, so one
   representative per orbit is enough.
2. For a fixed I, whether T can be moved into J depends only on the
   AGL(1,p)-orbit of T. (If σ(T) ⊆ J, then (σρ⁻¹)(ρ(T)) ⊆ J.) So one
   representative T per orbit is enough, tested against all of its p(p − 1)
   images at once.

Subsets are stored as integer bit masks, and the inner test
`(images & I) == 0` is vectorized with numpy.

### Running it

```
python3 pd_affine.py 23          # all k
python3 pd_affine.py 23 9 13     # only 9 <= k <= 13
sage -python pd_affine.py 23     # inside Sage
```

Requires Python 3 and numpy. Timings on a modest Linux machine: p ≤ 19 in
about 2 seconds, p = 23 in about 40 seconds.

For each k the output lists the number of failing orbits and of failing
information sets. For a few failing cases it also prints a witness: the check
set J and an error pattern T that no affine map moves into J.

### Results (Proposition 7.5 of the paper)

* For every p ≤ 23 and every k, **some** information set works.
* For p ≤ 13, **every** information set works.
* From p = 17 on, some information sets fail, even though the counting bound
  |AGL(1,p)|·C(p−k, t) ≥ C(p, t) holds. At p = 23 and k = 11, about 79% of all
  information sets fail.
* The "interval" information set {0, 1, …, k−1} works for every k when
  p ≤ 17. It fails for k ∈ {7, 9, 11} at p = 19, and for k ∈ {7, 9, 10, …, 15}
  at p = 23.
* At p = 37, k = 17, the counting bound shows that **no** information set
  works (Theorem 7.8).

## Open: p = 29 and p = 31 (Problem 10.2)

These are the remaining primes below 37, where the counting bound decides
nothing. The same algorithm applies, but it needs a compiled implementation
(C, say). The costs below are counted in 64-bit AND operations.

| p | k-subsets, worst k | coverage tests, all k | worst single k |
|---|---|---|---|
| 23 | 1.4 × 10⁶ | 1.7 × 10⁹ | 4.0 × 10⁸ (k = 9) |
| 29 | 7.8 × 10⁷ | 2.1 × 10¹² | 4.3 × 10¹¹ (k = 11) |
| 31 | 3.0 × 10⁸ | 2.4 × 10¹³ | 4.5 × 10¹² (k = 13) |
| 37 | 1.8 × 10¹⁰ | 3.3 × 10¹⁶ | — (counting bound already settles k = 17) |

So p = 29 costs about 1,000 times as much as p = 23, and p = 31 about 10,000
times as much. Python stops being practical at p = 29, for two reasons.
The seen-set of orbit representatives would hold about 78 million Python
integers, which is several GB. And the pure-Python loop over all k-subsets
is too slow.

### What a C implementation needs

1. **Subsets as `uint32_t` bit masks** (p ≤ 31 fits in 32 bits). The
   affine images of a mask can be computed with a precomputed table: for
   each map σ, an array `img[σ][x]`, or byte-sliced lookup tables mapping
   8 input bits to their image bits.

2. **Orbit representatives without a big hash set.** AGL(1,p) is sharply
   2-transitive, so every orbit of k-sets (k ≥ 2) has a member containing
   both 0 and 1. It is therefore enough to scan the C(p−2, k−2) subsets
   containing {0,1}. Duplicates can be removed with a **bitmap of 2^(p−2)
   bits** indexed by the remaining bits: 64 MB for p = 31. Alternatively,
   a subset is the canonical representative if its mask is the smallest
   among its p(p − 1) images. That needs no memory but costs p(p − 1)
   image computations per subset. For counting failing information sets,
   record each orbit's size, p(p − 1)/|stabilizer|.

3. **Error-pattern representatives** are found the same way (t ≤ 14).
   Store all p(p − 1) images of each representative in one contiguous
   `uint32_t` array, of about C(p, t) entries. This peaks at about 1 GB
   for p = 31 and the smallest k (where t = 14); for middle k it is much
   smaller.

4. **The inner loop.** For each representative I and each representative
   T, scan T's images for one with `(img & I) == 0`. Stop at the first hit,
   and abandon I as soon as some T has no hit. Early exit makes the typical
   cost far below the worst case in the table.

5. **Parallelism.** The representatives I are independent, so split them
   across cores with OpenMP (`#pragma omp parallel for`), or start one
   process per value of k. At roughly 10⁹ ANDs per core-second, and
   before any saving from early exit, a 16–24-core desktop should handle
   p = 29 in a few minutes and p = 31 in well under an hour.

6. **Validation.** Before trusting new results, reproduce the p ≤ 23
   tables in `results/` exactly.

### A cheap alternative: sampling

If only part (1) is wanted, namely whether **some** good information set
exists for each k, exhaustive enumeration is unnecessary. Pick random
k-subsets I and test each one exactly against the error-pattern
representatives. A single test costs about C(p, t) ANDs, roughly 10⁷ for
p = 31, which takes milliseconds in numpy. One good set settles the
question for that k. Sampling also gives statistical estimates of the
failing fraction. It cannot prove that **all** information sets fail.
For that the exhaustive search, or the counting bound, is needed.

## Authors and AI disclosure

The paper and this code were produced by David Joyner with substantial help
from two AI systems, ChatGPT (OpenAI) and Claude (Anthropic). Their roles
are described in the paper's Acknowledgments and in the revision log.
