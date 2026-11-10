# qrcodes-hyperelliptic

Two papers by David Joyner on error-correcting codes and hyperelliptic curves, each with a 2026 AI-assisted revision:

1. *On quadratic residue codes and hyperelliptic curves*: the original 2006 manuscript and a 2026 revision (this top-level folder).
2. *Conjectural permutation decoding of some AG codes* (ACM SIGSAM Bulletin, 2005): a corrected and expanded 2026 version, in [`perm-decoding/`](perm-decoding/).

## Quadratic residue codes: files

| File | What it is |
| --- | --- |
| `original/qrcodes-hyperell-dmtcs2.tex` | The version submitted to *Discrete Mathematics & Theoretical Computer Science*, received 20 Oct 2006 (David Joyner, sole author) |
| `qrcodes-hyperelliptic.tex` / `.pdf` | The revised paper (David Joyner and Claude), 12pt Times, US letter |
| `revision-log.tex` / `.pdf` | Change-by-change log from the 2006 file to the revision |
| `code/` | Python scripts that check every numerical claim (weight distributions, duality, examples, Duursma zeta zeros, Voloch's constructions, the mod-8 split), and a C program for exact minimum distances |

A different revision of the 2006 submission was published as D. Joyner, *DMTCS* 10:1 (2008), [doi:10.46298/dmtcs.429](https://doi.org/10.46298/dmtcs.429) (arXiv:math/0609562). This repository revises the 2006 file, not the published one.

### Update of 10 November 2026: the split by p mod 8 and a refined conjecture

A new Section 7 of the revised paper shows that the even subcode C_ev of the QQR code is a quadratic residue code in disguise. Write M_p for the largest number of points on y² = f_T(x) over sets T of even size, so that d(C_ev) = 2p + 2 − M_p.

- **p ≡ ±1 (mod 8)** (Proposition 7.1): C_ev is a direct sum of two binary QR codes, so M_p = 2p + 2 − d(extended binary QR code) exactly. Known QR distances then give M_p/p ≥ 1.787 for all such p with 31 ≤ p ≤ 199.
- **p ≡ ±3 (mod 8)** (Proposition 7.2): C_ev is the binary image of a quaternary QR code. An exact search gives M_p/p between 1.45 and 1.74 for every such p ≤ 83.

So the Bazzi–Mitter conjecture implies that binary or quaternary QR codes have minimum distance growing linearly in the length along an infinite set of primes (Theorem 7.4). The data suggest posing it only for p ≡ ±3 (mod 8):

> **Conjecture 7.5.** There is a constant c < 2 such that M_p ≤ cp for infinitely many primes p ≡ ±3 (mod 8).

This is equivalent to the quaternary QR codes of those lengths having minimum distance at least a fixed multiple of p. If it held with c < 2(1 − H⁻¹(1/2)) ≈ 1.7799, Goppa's conjecture would be false. We expect it to hold with c just above 1.78. A stronger form asks for M_p ≤ cp at all large safe primes p ≡ 3 (mod 8), where 2 is a primitive root.

Exact values of M_p/p at the three safe primes computed so far are 1.455 (p = 11), 1.695 (p = 59) and 1.735 (p = 83). For p = 107 the search gives only 1.682 ≤ M_p/p ≤ 1.794. Table 3 of the paper has the full data. The revision log's section "Additions of 10 November 2026" lists every change.

## Permutation decoding: summary

The 2005 note conjectured efficient permutation decoding for AG codes on y² = xᵖ − x. The 2026 version shows that both conjectures fail as universal statements, proves what does hold, and includes exhaustive computations for p ≤ 23. See [`perm-decoding/README.md`](perm-decoding/README.md) for its files, scripts and results.

## Building (quadratic residue codes paper)

```
pdflatex qrcodes-hyperelliptic.tex && pdflatex qrcodes-hyperelliptic.tex
pdflatex revision-log.tex && pdflatex revision-log.tex
```

## Checking the numbers (quadratic residue codes paper)

The scripts need Python 3.10+, plus `sympy` for the zeta check.

```
cd code
python3 check_weights_duality.py   # weight distributions, Prop. 3.6, self-duality / LCD
python3 check_examples_voloch.py   # worked examples, Voloch's constructions for p < 200
python3 check_zeta.py              # Duursma zeta polynomials and zeros (about 1.5 minutes)
python3 check_mod8.py              # Props. 7.1 and 7.2 (the split by p mod 8) for small p
```

Exact minimum distances of C_ev for p ≡ ±3 (mod 8), Table 3 of the paper (needs a C compiler with 128-bit integers, such as gcc or clang):

```
cd code
gcc -O3 -march=native -o dmin_cev dmin_cev.c
./dmin_cev 59        # prints d(C_ev) and M_p; seconds to minutes for p <= 67
./dmin_cev 83 12     # about 75 minutes on one core
```

## Authors

- David Joyner (wdjoyner@gmail.com): original paper
- Claude (Anthropic): co-author of the 2026 revisions of both papers; see their Acknowledgements and, for the quadratic residue codes paper, the revision log
- ChatGPT (OpenAI): co-author of the 2026 permutation-decoding revision; see its Acknowledgments
