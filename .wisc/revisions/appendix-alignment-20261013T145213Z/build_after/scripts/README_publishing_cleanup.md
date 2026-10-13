# Explicit publishing cleanup for figure/table presentation artifacts

Run `scripts/publishing_cleanup.py` **after any figure/table raw-source generator**
and before publishing the paper. Do not remove source-validation guards or weaken
their tests to make generated files look clean. This is an editorial projection,
not experimental certification, and never sets `reportable=true`.

From the paper root (Python 3.9+):

```sh
# Use a new, unused ledger filename for each regeneration/revision.
# The revision backup directory must already exist.
python -B scripts/publishing_cleanup.py plan \
  --record .wisc/revisions/author-alignment-20261013/publishing-cleanup-ledger.json \
  --backup .wisc/revisions/author-alignment-20261013/backup

# Review every entry in the ledger's files[].changes before applying.
python -B scripts/publishing_cleanup.py apply \
  --record .wisc/revisions/author-alignment-20261013/publishing-cleanup-ledger.json \
  --backup .wisc/revisions/author-alignment-20261013/backup

python -B scripts/publishing_cleanup.py verify \
  --record .wisc/revisions/author-alignment-20261013/publishing-cleanup-ledger.json \
  --backup .wisc/revisions/author-alignment-20261013/backup

python -B scripts/test_publishing_cleanup.py
```

The checked-in revision ledger already exists: use its `verify` command, not
`plan`, unless a fresh ledger filename is supplied. Relative paths resolve from
the current directory; `--root /absolute/paper/path` supports another working
directory. The default root is the script's parent paper directory.

## Scope and guarantees

- Recursively reads **all** `figs/` and `tables/` `.json`, `.text`, `.tex`, `.md`,
  and `.txt` presentation files, including inactive figures. Exact reviewed
  phrases and scalar JSON keys are removed, not arbitrary caveat paragraphs.
  Unknown flag wording fails closed and needs a reviewed policy update.
- Every deleted JSON pointer/value, replaced JSON string, and changed text line
  is retained in the ledger, together with before/after file SHA256s. Full
  original bytes are preserved under the existing backup directory's
  `publishing-cleanup/<original-sha256>/<relative-file>` subtree. Existing
  backups, the parent baseline, and old ledgers are never overwritten.
- Checks the entire artifact inventory for drift before writes. Each file is
  rechecked immediately before its write. Reapplying an already-complete plan
  is a no-op; partial/concurrent drift is refused. A multi-file write is not a
  filesystem transaction: an interrupted write requires inspection and a fresh
  plan or restoration from the archived originals, not blind continuation.
- JSON numeric values and their paths, text numeric tokens (except the removed
  audit-reason setting `=1`), complete TeX table bodies, and every embedded
  SHA256 value are invariant. Source identities, task/run counts, scientific
  uncertainty, candidate-pool limitations, mixed run families, unavailable
  checkpoints, and known-only/incomplete token-accounting limits remain.
- CSVs, PDFs/PNGs, artifact code/tests, raw experiments and external snapshots
  are not written. All paper CSVs outside revision archives and sibling
  `BayesGSI/tables` CSVs are hash-bound for verification. No build, model call,
  inference, source regeneration or manuscript-section edit is performed.

## Hash interpretation and previews

Embedded generator/source/snapshot hashes are deliberately preserved, including
historical output bindings: they describe the generating snapshot, not the
post-cleanup projection. The revision ledger's `after_sha256` values are the
current presentation bindings; do not claim the older manifests authenticate
new caption/provenance bytes. This cleanup does not repair pre-existing stale
hashes or refresh preview renderings.

For this revision only, the parent task owns rerendering
`tables/retrieval_and_reranking_performance/preview.pdf` and `preview.png` to
remove its embedded old caption. After that independent refresh, add
`--allow-preview-refresh` to **verify only**. It permits exactly these two
existing paths, records their before/after hashes in verification output, and
still rejects changes to every other file. It does not authorize this script to
write previews. The parent must independently validate the new preview content.

## Source and presentation validation remain separate

Run original source-generator tests against their raw outputs or disposable
fixtures. Those tests may intentionally require source reportability flags;
they are not replaced by the publishing projection's no-flag check. The
publishing verifier checks editorial/numeric invariance, not scientific
validity. After changing the cleanup policy, create a new ledger (old ledgers
remain pinned to the exact script SHA256 that created them).
