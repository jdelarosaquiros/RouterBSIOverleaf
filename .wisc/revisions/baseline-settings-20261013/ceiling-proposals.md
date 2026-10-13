# Backbone claim proposals — not applied

Location: `sections/ablations.tex`, §7.3, final two sentences of line 24.

## Current text

> Overall, these results demonstrate that RouterBSI can significantly improve the routing performance of predicates across LLMs. They also suggest that predicates reach a plateau that cannot be overcomed with more capable LLMs, where it's difficult for the predicate to be narrow enough to be false for irrelevant tasks but broad enough to be true for all relevant tasks

## Recommended replacement

> Overall, RouterBSI improves routing performance across all three evaluated backbones. Within this comparison, stronger cold-start performance does not consistently translate into higher optimized performance, and Qwen3.5 4B approaches GPT-OSS 120B after optimization.

This reports the observed pattern without asserting statistical significance, an intrinsic ceiling, or a general relationship between capability and performance.

## Alternative emphasizing model choice

> These results show that predicate optimization can substantially improve a smaller backbone: optimized Qwen3.5 4B approaches optimized GPT-OSS 120B, while Qwen3.8 27B achieves the highest final nDCG@1 among the evaluated models.

Evidence: current §7.3; Figure 7; `sections/appendix/ablation_backbones.tex` (initial/final nDCG@1: Qwen3.5 4B 0.520/0.742; Qwen3.8 27B 0.635/0.802; GPT-OSS 120B 0.686/0.745). No numerical results changed. Both proposals replace the final two sentences to remove the unsupported ceiling and avoid an untested significance claim. Neither proposal has been applied.
