# RouterBSI — ACL critique and proposed revisions

**Status: for author review only. No manuscript changes authorized or applied by this workflow.**

## Read these first

1. [PROPOSALS.md](PROPOSALS.md) — issue-by-issue proposed changes, replacement wording, required inputs and acceptance checks.
2. [REVIEW.md](REVIEW.md) — full grounded critique of the frozen PDF.
3. [VERSION_NOTE.md](VERSION_NOTE.md) — live source/PDF changes and findings already removed externally.

Machine-readable contracts: [REVIEW_JSON.json](REVIEW_JSON.json) and [REVISION_REPORT.json](REVISION_REPORT.json). Verification: [verification.json](verification.json).

## Internal verdict

**Substantial revision, 2/5 overall**, using the skill's internal scale—not an official ARR rating or acceptance prediction. The review contains **15 issues: 13 major, 2 minor, no confirmed policy/fundamental-validity blockers**. Material publication-readiness work remains even though no automatic desk-rejection violation was established.

The contribution is relevant to language agents: explicit skill-applicability predicates refined without changing model weights. The core results are promising, and the appendix contains substantial replication detail. The main risks are the interpretation and status of that evidence, not absence of all methodological detail.

## Highest-priority decisions

| Issue | Finding | Proposal |
|---|---|---|
| ISSUE-006 | Main-result manifests explicitly label inputs nonreportable/analysis-only. | Resolve existing provenance/audit evidence first; otherwise qualify affected results as exploratory or authorize replacement evidence. Do not simply flip a metadata flag. |
| ISSUE-002 / 003 | The replay guarantee has the wrong direction; main replay/ranking/gate description omits implementation-critical qualifications. | State fixed-set non-increasing empirical risk, current-inclusive replay, cold-start gate comparator and iteration-end rollback. |
| ISSUE-004 | Figure 5 claims matched initial predicates; Appendix G describes unmatched initialization. | Correct the caption and narrow causal interpretation, or use an initialization-paired design if a stronger claim is retained. |
| ISSUE-005 | The 10.8% token saving compares incomplete totals with unequal initialization coverage. | Disclose single-run/known-only scope and use common-phase accounting where available; do not claim complete cost savings. |
| ISSUE-007 / 008 / 009 | Split scope, historical candidate pools and unequal downstream budgets limit the comparison. | Promote exact task counts and represented-skill scope; document baseline protocols; distinguish method-native outcomes from controlled mechanism claims. |
| ISSUE-010 / 013 | Three backbone endpoints do not prove an intrinsic plateau; headline comparisons lack paired uncertainty. | Narrow claims now; analyze saved task-level outputs before considering additional runs. |
| ISSUE-001 | The frozen PDF misinterprets 94.68%/93.75% error shares. | **Already removed in a later externally changed PDF.** Do not reapply the deletion; an accurate replacement summary is optional. |

Most headline percentage calculations checked out once their aggregation and run selection were distinguished. The review does not treat rounded-table discrepancies as proof of arithmetic error, nor nonreportable provenance as proof of fabricated results.

## Scope and verification boundary

- Frozen review input: `reviewed_main.pdf`, 28 pages, SHA256 `51ddab4b827e211879ecf8c936083ea5fa2a03f6b34a32d230f98b90f5910d6b`.
- Main content ends on page 8, fitting the **assumed** long-paper submission budget. Exact venue/year/track/cycle/stage remain unknown.
- A4, two-column prose, embedded fonts, review numbering, distinct Limitations before References and appendix placement were checked. `acl.sty` and `acl_natbib.bst` match the supplied official archive. This does not certify all submission-form requirements or every typography choice.
- Checklist, AI-use disclosure, supplementary anonymity, authorship/eligibility and portal logistics need human confirmation.
- Three read-only scouts checked methodology, empirical/numerical consistency and compliance/figures. Parent verified literal issue anchors, manifest flags and key calculations.
- No manuscript build, experiment/model run, paper upload or commit was performed. The live worktree changed externally, so no whole-tree-unchanged claim is made.

## Fixer refinements to the critic

The fixer did not apply the initial suggested wording mechanically. Its ISSUE-011 proposal distinguishes predicate rejection from retrieval misses and protects the separate H.1 adjudicator confusion matrix. ISSUE-012 credits JTPRO’s tool-selection role as well as argument instantiation. Figure proposals preserve already-readable assets and require a drift-aware check before changing newer renders. Use the final proposal payload for these refinements, not the critic’s shorter preliminary replacement text.

## Approval options

You may approve individual ISSUE IDs, approve an evidence-backed text-only subset, request changes to the proposals, or authorize a separately scoped provenance audit. **EXP-001–004 are conditional designs, not automatic requests to rerun everything.** Before implementation, select the current authoritative source/PDF pair and skip changes already made elsewhere.

The WISC specification is archived after final verification under `.wisc/plans/completed/acl-critic-proposals.md`. TaskMaster was unavailable; Hermes task tracking was used.
