# Chunking decision

**Date:** 2026-10-13  **Decided by:** Rishi  **Corpus:** documents.py + corpus.py (16 documents)
**Eval set:** eval_set.py (29 answerable, 3 unanswerable)  **Embedding model:** voyage-3-lite

## Decision
We serve `sections_contextual` with a relevance floor of `0.50`.

## Evidence
| Strategy | R@1 | R@3 | MRR | Context words@3 | Answer acc. | Refusal acc. |
|---|---|---|---|---|---|---|
| whole_document | 0.690 | 1.000 | 0.845 | 862 | 0.72 | 1.00 |
| sections_contextual | 0.862 | 1.000 | 0.931 | 197 | 0.97 | 1.00 |
| fixed_overlap_25 | 0.517 | 0.931 | 0.668 | 277 | 0.59 | 1.00 |

Retrieval metrics come from `eval_results/retrieval.json` and describe top-three retrieval before floor filtering. All answer and refusal scores in this table come from the reported terminal run at the same floor, `0.50`: `python -m eval_answers whole_document sections_contextual fixed_overlap_25 --floor 0.50`.

## Why this one
`sections_contextual` matches whole-document R@3 of 1.000, improves MRR from 0.845 to 0.931, and reduces context words@3 from 862 to 197 (about 77%). Across tested floors 0.35, 0.40, 0.45, 0.50 and 0.55, 0.50 is the highest tested floor preserving 0.97 answer accuracy and 1.00 refusal accuracy, with 379 average input tokens per call versus 413 at 0.45. We accept more input tokens than the 315 at 0.55 because that floor adds false refusals on q06 and q09 and drops answer accuracy to 0.90; 0.50 is the best tested choice, not a proven optimum.

## Known weaknesses
q24, an exact-ID question ("What is matter LP-3307?"), is falsely refused at every reported floor despite the selected strategy having no retrieval misses at top three before floor filtering. Investigate whether floor filtering removes its evidence or the model refuses despite receiving it; exact-ID matching or hybrid lexical/vector retrieval is a candidate if identifier retrieval is the cause. At 0.50, the selected strategy reports no wrong or unrefused answers, but these results cover only 29 answerable and 3 unanswerable questions and use keyword checks rather than a full factual review.

## Revisit when
Re-run retrieval and answer evaluations when the corpus gains new document types or substantially longer documents, the embedding or answer model changes, or exact-ID failures and false refusals recur in real queries. Revisit the floor when an expanded unanswerable set exposes incorrect answers or token costs justify a different coverage tradeoff.
