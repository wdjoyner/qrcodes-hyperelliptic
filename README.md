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
| `code/` | Python scripts that check every numerical claim (weight distributions, duality, examples, Duursma zeta zeros, Voloch's constructions) |

A different revision of the 2006 submission was published as D. Joyner, *DMTCS* 10:1 (2008), [doi:10.46298/dmtcs.429](https://doi.org/10.46298/dmtcs.429) (arXiv:math/0609562). This repository revises the 2006 file, not the published one.

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
```

## Authors

- David Joyner (wdjoyner@gmail.com): original paper
- Claude (Anthropic): co-author of the 2026 revisions of both papers; see their Acknowledgements and, for the quadratic residue codes paper, the revision log
- ChatGPT (OpenAI): co-author of the 2026 permutation-decoding revision; see its Acknowledgments
