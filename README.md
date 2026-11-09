# qrcodes-hyperelliptic

*On quadratic residue codes and hyperelliptic curves*: the original 2006 manuscript and a 2026 revision.

## Files

| File | What it is |
| --- | --- |
| `original/qrcodes-hyperell-dmtcs2.tex` | The version submitted to *Discrete Mathematics & Theoretical Computer Science*, received 20 Oct 2006 (David Joyner, sole author) |
| `qrcodes-hyperelliptic.tex` / `.pdf` | The revised paper (David Joyner and Claude), 12pt Times, US letter |
| `revision-log.tex` / `.pdf` | Change-by-change log from the 2006 file to the revision |
| `code/` | Python scripts that check every numerical claim (weight distributions, duality, examples, Duursma zeta zeros, Voloch's constructions) |

A different revision of the 2006 submission was published as D. Joyner, *DMTCS* 10:1 (2008), [doi:10.46298/dmtcs.429](https://doi.org/10.46298/dmtcs.429) (arXiv:math/0609562). This repository revises the 2006 file, not the published one.

## Building

```
pdflatex qrcodes-hyperelliptic.tex && pdflatex qrcodes-hyperelliptic.tex
pdflatex revision-log.tex && pdflatex revision-log.tex
```

## Checking the numbers

The scripts need Python 3.10+, plus `sympy` for the zeta check.

```
cd code
python3 check_weights_duality.py   # weight distributions, Prop. 3.6, self-duality / LCD
python3 check_examples_voloch.py   # worked examples, Voloch's constructions for p < 200
python3 check_zeta.py              # Duursma zeta polynomials and zeros (about 1.5 minutes)
```

## Authors

- David Joyner (wdjoyner@gmail.com): original paper
- Claude (Anthropic): co-author of the 2026 revision; see the Acknowledgements and the revision log
