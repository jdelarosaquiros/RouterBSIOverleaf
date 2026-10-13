# Task: Current RouterBSI ACL critique and approval-ready proposals

## What
Review the current main.pdf using acl_critic, then use fix_acl_critic to propose issue-mapped solutions. No paper/source/figure/result changes before author approval.

## Why
Provide an independent, evidence-calibrated review of the revised manuscript rather than repeating stale findings.

## Scope and inputs
- Paper root: /workspace/storage/healthcare_workspace/project_skill_selection/RouterBSIPaper
- Immutable snapshot and outputs: .wisc/reviews/acl-critic-proposals-20261013T133137Z-a13feaa0/
- PDF SHA256: a13feaa06ce9697e5d4d44119ea46f4403aff73a8743d3bb51bcc616dd3174e5
- 29 total PDF pages; main content ends on page 8.
- Exact local prompts match loaded skill full prompts; all three local ACL requirements guides read.
- Venue/year/track/cycle/stage unknown; long paper is an assumption. No inferred upload permission or active deadline.
- EXPERIMENTAL_RESULTS = []; existing manuscript/artifact evidence may be inspected read-only, no new experiments.

## Files to create
Only review artifacts under the output directory and this WISC plan. No manuscript, source, data, figure, prompt, or policy edits. No rebuild/commit/upload.

## Key decisions
- Repeated user request authorizes non-destructive review/proposals following the earlier confirmation checkpoint; it does not authorize edits.
- Separate necessary evidence/claim corrections from optional exposition. In particular do not relabel the correctly scoped replay-risk inequality or initial-predicate validation gate as errors.
- Independent science, presentation/compliance, and narrative/self-containment scouts; parent verifies final issues.
- Keep strict reviewer/fixer JSON contracts; fixer logs every item as not_executed and puts proposed edits in separate proposal fields/artifact.
- TaskMaster unavailable; Hermes todo is the tracking substitute. Code-implementation/commit phases are inapplicable to proposal-only scope.

## Validation
- Validate strict JSON, issue IDs, dependencies and full proposal/acceptance-criterion coverage.
- Mechanically verify source anchors against immutable source snapshot; cross-check PDF pages.
- Numerically check material claims with Python and distinguish measurements from proposals.
- Compare hashes of 332 original non-temporary paper-tree files at completion; report any concurrent drift rather than claiming unchanged blindly.
- Deliver REVIEW_JSON.json, REVIEW.md, PROPOSALS.md, REVISION_REPORT.json, verification.json and WISC_REPORT.md.

## Completion and concurrent-version reconciliation
- Initial 29-page PDF changed outside this review-only action set. Final review is bound to the 30-page PDF SHA-256 e68ac3a31d892feb1141089312c51d2a70929281cbfb57aa4cf5825088d91779; main content still ends on page 8.
- 12 preexisting paper files changed and two appendix sources were added concurrently. Nothing was reverted and no actor is inferred. See concurrent_changes.json.
- ISSUE-001 resolved by concurrent revision; ISSUE-006 narrowed/downgraded; ISSUE-007 credits the new statistical disclosure. Final active set: 12 issues, 6 major and 6 minor, with matching proposals.
- Verification passed for current PDF/source anchors, dependencies, JSON contracts, eight figures, all 12 initial-policy files and 334 current-snapshot protected files. No paper edit, rebuild, model run, commit or upload performed by this review.
- Shared acl_critic/fix_acl_critic skill guidance now records version-drift handling and explicit proposal-only execution boundaries.
- Ready for author review. Apply no proposals until explicit approval.
