# Style guide for mathematical papers (D. Joyner)

Draft 2, November 11, 2026. Compiled from instructions given to Claude and ChatGPT during the 2026 revisions.

**How to use this file.** Paste it into the first prompt of any chat that drafts, revises or referees a paper. Instructions in the prompt override this file. Rules marked **[DECIDE]** have varied between papers and need a ruling from David. Until then, follow the stated default and say which default you used.

Sections 1 to 5 apply to all papers. Section 6 applies only to revisions of older papers. Section 7 applies to referee reports. Section 8 covers workflow. Section 9 lists paper-specific rules.

---

## 1. Typesetting (mandatory)

1. 12pt, Times for text and math, US Letter paper, one-inch margins.
2. The file must compile with pdflatex. Compile it before sending. Fix every error, undefined reference and overfull box.
3. Do not hide overfull boxes with manual line breaks. Reword or reflow instead.
4. American English spelling everywhere, including comments.
5. Use `\label` and `\ref` for every cross-reference. Use `\cite` for every citation. Never type a reference number or citation by hand.
6. Number theorems, propositions, lemmas and equations within sections (Theorem 4.2, equation (4.3)). Do not number subsections that do not need a number.
7. Citation keys and bibliography labels are author initials plus two-digit year: `Jo99`, `KP84`, `DS18`. When keys change, update every `\cite` in the document.
8. Declare operators with `\DeclareMathOperator` or use `\operatorname`.
9. Keep theorem labels stable across drafts so that references do not break.

**[DECIDE] Document class.** ChatGPT's revisions used `amsart`. Several of Claude's used `article`. Default: keep the class of the existing file, and use `amsart` for a new paper.

**[DECIDE] Times package.** `newtxtext` with `newtxmath` gives better math. `mathptmx` is the fallback when newtx is not installed. Default: newtx.

Default preamble for a new paper:

```latex
\documentclass[12pt,letterpaper]{amsart}
\usepackage[T1]{fontenc}
\usepackage{newtxtext,newtxmath}
\usepackage[letterpaper,margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{microtype}
\usepackage[hidelinks]{hyperref}
```

## 2. Structure (mandatory unless the prompt says otherwise)

A paper has these parts, in this order.

1. **Abstract.** Opens with an AI-disclosure sentence (Section 5). Then states the contributions plainly.
2. **Introduction.** The problem, the motivation and the main results.
3. **Literature review.** Short summaries of related papers, saying how the present results fit in. A bare list of citations is not enough. For a revision, split it into work before and after the original paper's date.
4. **Background.** The facts and prerequisite concepts the paper needs. The background explains each concept in more detail than the glossary does. Each section of the background contains at least one example of the concepts it explains.
5. **Notation.** A table or section of notation near the beginning.
6. **Body.** See Section 3.
7. **Summary of results**, near the end. Add open questions or future directions when there are any.
8. **Glossary** of technical terms.
9. **Acknowledgments**, at the end. They state each AI contribution clearly, naming the system and its role (referee, co-author, reviser and so on). See Section 5.
10. **References.**

**[DECIDE] Glossary placement.** Most papers have the glossary at the end. One prompt put it just before the references. The metaplectic Jacquet–Langlands series merged it into an early "Notation and glossary" section. Default: notation near the beginning, glossary at the end just before the acknowledgments.

## 3. Exposition (mandatory)

1. Write for a mathematically mature reader who is not a specialist in the exact topic. Keep full rigor. Give enough background, motivation and examples that the argument can be learned from the paper.
2. Begin every section and subsection with a short orienting paragraph. It says what the section does and why.
3. Every section contains at least one example of the concepts it explains. Prefer concrete worked examples. In a series, use one running example throughout.
4. Motivate each substantial definition. Pair each definition with an explicit concrete example whenever possible. Explain each difficult formula. Explain specialist concepts (orbital integrals, genuine representations, invariant distributions and the like) before relying on them.
5. Define every nonstandard symbol at first use, even if it is in the glossary.
6. State all hypotheses before each major theorem.
7. Do not skip nontrivial steps in proofs.
8. Use short, direct sentences. Each argument is a chain of related sentences leading to its conclusion. Avoid semicolons.

## 4. Correctness and honesty (mandatory)

1. Every result must be visibly one of four kinds. It is proved in the paper, or cited from a source, or conditional on stated hypotheses, or conjectural. Computational evidence and open problems are labeled as such.
2. Never upgrade a status silently. A change of status goes in the revision log.
3. Check every citation against the source, including theorem and page numbers. Cite the precise theorem, proposition or page. If you could not consult the source, say so in the revision log.
4. Do not accept a computational claim because a manuscript says a script checks it. Run the script or check the claim independently. Prefer hand proofs. A computation that a proof depends on must be exhaustive and exact, with its script in the repository.
5. Verify claims made by another AI independently before using them.

## 5. Authorship and AI disclosure

1. David's address on the author line is `wdjoyner@gmail.com`. Remove old institutional addresses.
2. Always open the abstract with an AI-disclosure sentence, and refer to the Acknowledgments for further details.
3. The acknowledgments name each AI system that contributed and describe its role (drafting, revising, refereeing, co-authoring, independent proofs).
4. The acknowledgments state that AI review is not an independent certification of the results.
5. The acknowledgments state that further details on the AI usage can be found in the revision log.

**[DECIDE] AI systems on the author line.** Some papers list AI systems as authors, with a paper-specific order. arXiv and most journals do not accept an AI as an author, so a version meant for submission needs the credit in the acknowledgments instead. Default: follow the prompt for the author line, and always include the acknowledgment, and state there that further details on the AI usage can be found in the revision log.

## 6. Revisions of older papers

1. Preserve the mathematical content, the approach and, where possible, the wording and structure of the original. Correct errors. Do not replace the central argument with a different paper. Never leave an incorrect statement standing.
2. Keep the original title. Add a subtitle "Draft <number>". Also add to the subtitle: "Corrected and expanded version". Add to the date line: "Original draft: <year of publication>. Corrected and expanded draft: 2026".
3. Identify the original publication or manuscript and the date of the revision on the title page. Put the note about the original in a `\thanks` footnote.
4. Keep revision history out of the body. Referee responses and comparisons between drafts go in the revision log (Section 8).
5. In the revision log file, separate the original results from results newly established in the revision.
6. Mark anything not fully verified as "Remark 2026.n". Do not put dates or color in the label.
7. If only a PDF of the original exists, first make a literal LaTeX transcription with no corrections. Record typos and errors in a separate log. Additions by an AI in the transcription source appear only as comments marked with the AI's name.
8. If numbering changes, put a concordance table (old number to new number) in the revision log.

## 7. Instructions to AI referees

1. Referee for correctness first and readability second.
2. Read the attached files. Do not rely on memory of earlier drafts. State plainly what you read and what you did not.
3. For each point you check, state the level of verification. Level 1 is an independent derivation. Level 2 is a check against a source you actually consulted. Level 3 is reliance on memory.
4. Check each claim of another referee independently before agreeing or disagreeing with it.
5. Give a verdict on each issue: correct, misprint, fixable gap, or false.
6. Report violations of Sections 1 to 6 as well as mathematical errors.

## 8. Workflow and deliverables

1. Deliver the editable `.tex` source and the compiled PDF. When asked, deliver a ZIP archive of source, PDF, revision log and scripts.
2. Keep a revision log as a separate LaTeX file. It records every change from the previous draft and every response to a referee. It also records the AI usage in detail, any source that could not be consulted (4.3), and which results are original and which are new (6.5).
3. Each draft carries a draft number. Cross-references to related manuscripts cite their current drafts.
4. Computational scripts go in the repository. The paper refers to them by commit hash where possible.
5. Repository licenses are MIT for code and CC BY 4.0 for LaTeX.
6. Do not post a corrected version of a published paper publicly until the copyright position is clear.

## 9. Paper-specific rules

These apply only to the named project.

- **Metaplectic Jacquet–Langlands series and book.** Status labels are written with parentheses, not square brackets, so that they cannot be mistaken for citations: (P) proved, (E) established elsewhere, (O) proof outlined, (C) conjectural, (P^c) proved modulo an exhaustive exact computation. In the book, a statement proved in the chapter carries no visible tag in the body, and (P) appears only in the status tables. Hypothesis tags are (Hyp) and (Hyp_D), not (H) and (H_D). Write the p-adic absolute value as |·|_p with |p|_p = p^{-1}. Each new draft is a new file with its own revision log. Ask before changing anything mathematical during an exposition pass.
- **Trace formula repository.** Work proceeds in stages recorded in `revision_log.md`. File names carry no draft number, and git history tracks the drafts.
- **1981 zeta operators paper.** The corrected edition uses only results known in 1981. Modern material goes in a separate review.
- **Satake paper.** The corrected version keeps the original style. Extra details go in a separate companion paper.

---

## Provenance of this draft

Most rules appear in the recollections of both Claude and ChatGPT. Draft 2 adds David's own changes of November 11, 2026.

The following come only from ChatGPT's recollection and were not found in the Claude chats searched: the `amsart` class, the citation-key examples `KP84` and `DS18`, the three verification levels in Section 7, and the ZIP archive.

The following were proposed by ChatGPT and are not known to be David's stated rules: 1.8, 1.9, 3.5 and 3.6. Rule 1.3 is ChatGPT's proposal added to David's request for no overfull boxes.

Rule 1.7 was stated to Claude for one paper only (the local trace formula paper). ChatGPT recalls it as a general rule. The no-semicolon part of 3.8 was stated to Claude for one paper only.
