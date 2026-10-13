# Audit A — procedure, prompts, data

**Read-only result:** 16 files, 13 subsections, 3 section wrappers and 4 worked-example paragraph headings audited. Four minimal editorial edits proposed; none applied. Full per-heading assessments, exact main quotations and unresolved items are in `audit_A.json`.

## Blocked scientific mismatches
- **Replay membership:** main `sections/method.tex:24–40` defines historical-only replay with two N-bounded groups; `procedure_replay.tex:7–11` includes the current task and permits 2N+1. Preserve the latter; do not claim exact equation alignment. This propagates to MBR and algorithm descriptions.
- **Replay support ambiguity:** main `method.tex:44` says error is over tasks retrieving the skill; appendix lazy buckets replay already-seen global history without a stated retrieval filter. Report ambiguity, not an invented implementation match.
- **Split allocation:** main `experiments.tex:12` says each dataset is 70/15/15. `data_splits.tex:5,18–25` specifies a constrained global target, including BigCodeBench 813/123/123 and TheoremQA 259/106/105. Keep counts and labels unchanged.
- **Ranking scope:** main `experiments.tex:39,47` uses arithmetic label-plus-score generally; `procedure_routing.tex:18` uses lexicographic selected-first ranking and only establishes equivalence for SkillSight 1/j scores. Keep this meaningful distinction.
- **Cross-scope initialization caption:** directly read `figs/mbr_replay_test_ndcg@1_std/description.text:1`, which says all three runs share initialization. Parent reports differences among saved initial predicate libraries conflict with that assertion; those runs were not re-audited here. Frozen caption stays blocked, not propagated into prompt prose.

## Per-file heading audit
All paths below are under `sections/appendix/`. Main evidence references are repository-relative. Source-level quotations are in the JSON.

### `data.tex` — Benchmark and Skill Corpus Details
Wrapper retained; four included subsections audited below.
Main evidence: `sections/experiments.tex:12`.

### `data_corpus.tex` — Shared Skill Corpus and Data Access
Retain exact corpus/gold/distractor counts, public access and mapping details. Main rounded 26k is compatible; metadata MIT is qualified by constituent licenses in data_scope.
Main evidence: `sections/introduction.tex:29`, `sections/experiments.tex:12`, `sections/ethics_statement.tex:3`.

### `data_labels.tex` — Required-Skill Labels and Task Types
Retain multi-skill counts, entire required-set denominator and unannotated-usefulness distinction. These are evaluation definitions, not artifact caveats.
Main evidence: `sections/experiments.tex:12`, `sections/experiments.tex:20`.

### `data_scope.tex` — Artifact Coverage and Reuse
Rename to Dataset Coverage and Reuse; delete only the credential-archive sentence. Retain language/representation limits, component licenses, identifying-information risks and untrusted-content warnings.
Main evidence: `sections/ethics_statement.tex:3`, `sections/experiments.tex:12`.

### `data_splits.tex` — Task Filtering and Split Construction
Retain filtering, exact table, seed and represented-skill generalization boundary. BLOCKED: global constrained proportions differ from main per-dataset wording; exact counts take precedence over forced textual agreement.
Main evidence: `sections/experiments.tex:12`, `tables/skill_routing_performance_average/table.tex:4`.

### `procedure.tex` — Routing and Improvement Procedure
Wrapper retained; five included subsections audited below.
Main evidence: `sections/method.tex:16`, `sections/method.tex:56`, `sections/method.tex:80`.

### `procedure_algorithm.tex` — Optimization Procedure
Remove the misleading “main” adjective from the appendix cross-reference. Retain sequence, provisional commits and iteration-end rollback. Current-inclusive replay mismatch remains blocked.
Main evidence: `sections/method.tex:56`, `sections/method.tex:80`, `sections/related_works.tex:8`.

### `procedure_mbr.tex` — Candidate Admission and Minimum-Risk Selection
Retain mean-risk formula and unchanged candidate; individual-error tradeoffs, ties and unspecified tie-break are scientifically necessary. Same formula does not resolve different replay-set membership.
Main evidence: `sections/method.tex:36`, `sections/method.tex:56`, `sections/method.tex:28`.

### `procedure_replay.tex` — Bounded Replay Construction
Retain sampling mechanics, global versus bounded histories and prompt-example versus scoring-set distinction. BLOCKED: current-inclusive 2N+1 versus historical-only main definition; retrieval-support scope also needs clarification.
Main evidence: `sections/method.tex:28`, `sections/method.tex:44`, `sections/method.tex:56`.

### `procedure_routing.tex` — Initialization and Online Routing
Retain strict routing, failure set, retrieval-miss boundary and sequential task updates. BLOCKED: lexicographic ranking agrees with the main arithmetic sum for stated SkillSight scores, not proven for arbitrary retrievers.
Main evidence: `sections/method.tex:16`, `sections/problem_definition.tex:8`, `sections/experiments.tex:47`.

### `procedure_validation.tex` — Held-Out Gate and Partial Rollback
Retain strict rejection of ties, cold-start comparator, partial rollback, unsupported-skill behavior, test exclusion and score-phase distinctions. Explicit main equation and method caption support these qualifications.
Main evidence: `sections/method.tex:80`, `sections/related_works.tex:8`.

### `prompts.tex` — Prompts and a Worked Repair
Wrapper retained; literal prompts and worked-example content remain immutable.
Main evidence: `sections/method.tex:16`, `sections/method.tex:36`, `sections/method.tex:56`, `sections/limitations.tex:8`.

### `prompts_evaluator.tex` — Boolean Predicate Evaluation
Retain full prompt and one-Boolean schema. Predicate truth independent of desirability is the evaluator instruction; use of that truth for selection is a separate router operation.
Main evidence: `sections/method.tex:16`, `sections/limitations.tex:8`, `sections/method.tex:56`.

### `prompts_initialization.tex` — Initial Predicate Generation
Delete only editorial “preserve prompt wording” sentence outside template. Keep inputs/schema and every prompt token. Do not import the blocked shared-all-runs initialization assertion.
Main evidence: `sections/method.tex:16`, `sections/method.tex:36`, `figs/mbr_replay_test_ndcg@1_std/description.text:1`.

### `prompts_proposal.tex` — Replacement Proposals
Retain exact fields, candidate template, retry and copied-predicate corrections. Generation goals to fix/preserve examples are not stronger hard admission guarantees than the main argmin.
Main evidence: `sections/method.tex:36`, `sections/method.tex:56`, `sections/method.tex:28`.

### `prompts_trace.tex` — A Complete Replay Decision
Retain the worked example, exact-versus-condensed distinction, all table values and cold-start/current separation. Local example behavior must not be generalized into a universal MBR guarantee.
Main evidence: `sections/method.tex:56`, `sections/method.tex:80`, `sections/related_works.tex:8`.
- **Predicate before repair.** (line 5): Retain exact current predicate string. It is not the cold-start baseline used later by validation; the main separates p_f and p_si.
- **Generated alternatives.** (line 12): Retain all three exact candidate strings, ordering, and labels. Their content is observed example evidence, not prose to harmonize with ideal prompt instructions.
- **Replay evidence.** (line 32): Retain five relevant/five irrelevant tasks, table, caption, and risk explanation. All-candidates-correct/preserve claim is explicitly local to this example, not a general MBR guarantee. Condensed task descriptions versus exact question/predicates is scientifically useful disclosure.
- **Held-out retention.** (line 55): Retain exact cold-start predicate, same 44-task support, 33/44 to 39/44 correctness, and iteration-end timing. Distinct initial/current predicates and partial-pass timing clarify rather than contradict main strict gate.

## Exact minimal proposed replacements
All replacements are outside literal prompt bodies; all old spans match exactly once. An empty `new` means delete that span. Trailing spaces in the JSON old strings deliberately prevent doubled inter-sentence spaces.

### `sections/appendix/data_scope.tex`
Old:
```tex
\subsection{Artifact Coverage and Reuse}
```
New:
```tex
\subsection{Dataset Coverage and Reuse}
```
Use dataset-focused heading; retain label app:artifact-scope and all scientific coverage/licensing statements.

### `sections/appendix/data_scope.tex`
Old:
```tex
Credential-file exclusion from a software archive is distinct from reviewing and de-identifying task content or model traces. 
```
New:
```tex

```
Remove redundant code-archive caveat. Adjacent sentences still identify privacy risks and the need not to equate public access with absence of identifying information.

### `sections/appendix/procedure_algorithm.tex`
Old:
```tex
The update loop below follows the main minimum-average-risk formulation in Section~\ref{app:procedure-mbr}.
```
New:
```tex
The update loop below follows the minimum-average-risk formulation in Section~\ref{app:procedure-mbr}.
```
The reference targets an appendix subsection; remove the misleading main designation without changing the algorithm.

### `sections/appendix/prompts_initialization.tex`
Old:
```tex
We preserve the prompt wording below, with paragraph wrapping for readability. 
```
New:
```tex

```
Delete editorial provenance/formatting commentary outside the prompt; preserve the complete literal prompt and schema description.

## Verification and limits
- Read complete main context, all scoped current files and corresponding before snapshots, main entrypoint, all six external main float TeX files, and the three nested caption texts. Embedded introduction/method captions were read with the main context.
- All scoped files matched `R/before`; all 20 source headings have explicit entries. Split-table column sums and retained/task split arithmetic check; trace risks check as 0.50/0.40/0.20/0.30.
- This is manuscript-source alignment, not revalidation of run artifacts or source-code behavior. No web, experiments, implementation exploration, manuscript edits or asset changes.
- Repository already had substantial changes. Initial git reads hit dubious ownership; command-local `git -c safe.directory=...` allowed inspection without changing git configuration.
- Created only `audit_A.json` and `audit_A.md` under this revision directory.
