# Skill-Pro: condition versus executable content

## Primary source

Mi et al., *Skill-Pro: Learning Reusable Skills from Experience via Non-Parametric PPO for LLM Agents*, ICML 2026, PMLR 306:88574–88595. Existing citation key: `pmlr-v306-mi26d`.

- Official page: https://proceedings.mlr.press/v306/mi26d.html
- PDF linked by that page: https://raw.githubusercontent.com/mlresearch/v306/main/assets/mi26d/mi26d.pdf
- Read the official page and linked 22-page PDF. Page numbers below are the PDF's printed page numbers, which match PDF page positions. Quotes join line wraps and normalize mathematical subscripts; wording is retained, including the paper's “expressed as in natural language.”

## Exact evidence

### Skill representation — §3.2, p. 3

> “We define a Skill ω ∈ Ω as a reusable, natural-language procedural unit that specifies when to activate, how to act while active, and when to return control.”

The displayed definition is `ω = ⟨I_ω, π_ω, β_ω⟩`, followed by:

> “representing its activation condition, execution procedure, and termination condition.”

### Applicability / activation condition — §3.2, pp. 3–4

On p. 3:

> “The activation condition specifies when a Skill is invoked. Rather than a learned classifier in latent space, I_ω is a natural-language description of observable context patterns where the Skill applies.”

The next sentence begins on p. 3 and ends on p. 4:

> “During decision making, the Skill-selection policy µ uses I_ω to select Skills based on the current state or interaction history.”

Thus, “applicability condition” can describe the role of the original paper's *activation condition*: natural-language context for when to invoke a skill, distinct from the procedure that is executed.

### Executable content — §3.2, p. 4

> “The execution procedure π_ω specifies an ordered sequence of actions to be executed while the Skill ω is active, expressed as in natural language.”

> “At each time step t, the LLM generates a primitive action conditioned on the current state s_t and π_ω (Eq. (1)), enabling the agent to reuse procedural steps without re-deriving deliberative reasoning from scratch.”

The original executable content is therefore a natural-language action procedure interpreted by the LLM, not necessarily program code.

### Concrete separation — §3.2 example, p. 4

For the example skill `StrategicPlanning`, the activation-condition text is:

> “When the task begins and no prior information or feedback is available.”

The execution-procedure text is:

> “Step 1: Establish an initial hypothesis space based on the task constraints.”
>
> “Step 2: Generate a diverse exploratory action that maximally reduces uncertainty.”

The paper separately defines a termination condition; that third component should not be conflated with the activation condition.

### Original method does not freeze the skill pool — §3.4, p. 4

> “The Skill pool is learned from interaction experience and evolves over time.”

The pool-evolution operator is described as one:

> “which synthesizes new Skills, refines existing Skills, and prunes those that underperform empirically.”

The frozen-skill statement belongs to the author-confirmed local adaptation, not to the original method. No local PPO training, optimization, or hyperparameter settings follow from these source passages.

## Concise appendix wording

> Following Skill-Pro's distinction between activation conditions and execution procedures~\cite{pmlr-v306-mi26d}, we keep the existing skills fixed and generate only a natural-language applicability condition for each skill. Each condition describes the contexts in which its corresponding skill should be invoked, while the skill's executable content remains unchanged.

This wording uses the supplied author-confirmed adaptation and introduces no local training or selection settings.

## Scope and retrieval

No manuscript files were edited. The web-extraction tool was unavailable for URL extraction; direct HTTPS retrieval of the official page and PDF succeeded. No arXiv fallback was needed. PDF validation (`file`, `pdfinfo`) and layout-text extraction succeeded; source passages were cross-checked against page-specific PDF text.
