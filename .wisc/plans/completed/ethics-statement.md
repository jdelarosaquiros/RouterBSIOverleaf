# Task: Add Ethics Statement

## Scope and rationale
Add a concise unnumbered Ethics Statement after Limitations and before References, based on saved ACL guidance and actual examples. Modify only main.tex and add sections/ethics_statement.tex. Preserve current paper, assets, tables, style, and anonymity. No commitment that licenses/IRB/consent/privacy guarantees were independently verified; no assertion that author review occurred. No commit of dirty inherited edits.

## Evidence
Saved requirements_and_examples.md lines 32,38-39,80-84: ethical discussion and truthful checklist/disclosure, separate from appendix. EASYTOOL PDF p9: dedicated Ethics Statement before references; discuss benchmark risks and disclose AI writing assistance, but its human annotation claims are not transferable. MemSkill PDF pp32-33: research-vs-deployment distinction, privacy/access/retention safeguards, AI assistance and author responsibility. RouterBSI appendix data_labels/data_corpus: reused SRA-Bench associations and web-collected skill contents. Limitations: dependence on labels and fallible predicate checker. Main experiments: existing benchmarks incl MedCalc-Bench, LLM inference. Current session establishes AI manuscript and artifact-code assistance.

## Proposed exact source
\section*{Ethics Statement}

Our experiments reuse existing SRA-Bench tasks, required-skill annotations, and skill content. Released annotations and web-collected skills may contain errors, biases, or harmful instructions; routing performance does not establish the safety of the underlying content. Reuse and redistribution should respect the licenses and access conditions of the constituent datasets, skills, and models. Public availability alone does not establish permission to transmit sensitive content to external model services. Deployment should minimize retained task data and apply appropriate consent, access controls, and retention policies to prompts, replay examples, and logs.

Incorrect predicate judgments can omit required skills or admit inappropriate ones, potentially propagating errors to downstream decisions. Bounded replay and held-out validation assess routing behavior, not factual correctness, fairness, or safety, and do not guarantee reliable behavior outside the evaluated tasks. In particular, results on MedCalc-Bench do not establish clinical validity or suitability for patient care. High-stakes applications require domain-specific validation and qualified human oversight. Retrieved instructions and generated code should be treated as untrusted content, with permission controls and isolated execution before use.

Repeated model calls for predicate optimization incur computational and environmental costs. Our token-use comparisons do not quantify energy consumption or emissions and should not be interpreted as evidence of environmental savings. Generative AI tools assisted manuscript drafting and editing and the preparation of artifact-generation code. Responsibility for the scientific claims, results, and references remains with the authors.

## Verification
Read current main before patching. Independent source equality except one include; source-hash preservation; make rebuild; make check; final log warnings and PDF text order; render ethics and adjacent pages and inspect. Report exact page count/placement. Archive plan on completion. Hermes todo substitutes for unavailable TaskMaster.
