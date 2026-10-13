"""Independent content checks for this prompt-only ACL/ARR migration."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[3]
EXPECTED = [
    "01-iclr2027_critics_agent 3.md",
    "02-iclr2027_fix-critics_agent 3.md",
]
SOURCES = {
    "requirements_and_examples.md": "e3af9e7a64bc26f429eb990edfaed5475c520b6c2d735d9110a37c79801a5317",
    "appendix_requirements.md": "3a8c15ee985885065ba2cc553851754a958638df3e3b9863865c25b02ed392c2",
    "appendix_outline.md": "b6bec6bf3a9478b41f4a96fc34dee7b2cf3ebc2d49bcb0a4e4990fa326c5bcaa",
}
FORBIDDEN = {
    "old_json_keys": r'"(?:iclr_compliance|iclr_scores|tenth_page_plan|discussion_phase_prep|pages_remaining_of_9|feasible_by_sept_25)"',
    "old_deadline": r"Sept(?:ember)?\.?\s+(?:18|25)|Nov(?:ember)?\.?\s+5\s*[-–]\s*18",
    "old_style": r"ICLR\s+2027\s+(?:style|LaTeX)|ICLR.standard conventions",
    "old_review_budget": r"9.page\s+(?:submission|main\s+text)|9\s+pre.submission|10\s+discussion",
}
REQUIRED = {
    "acl_arr_context": r"ACL[/ /-]+ARR|ACL Rolling Review",
    "naacl_source_scope": r"NAACL 2027",
    "limitations": r"Limitations",
    "checklist": r"Responsible NLP",
    "two_columns": r"two.column",
    "a4": r"\bA4\b",
    "anonymity": r"anonym",
    "self_containment": r"self.contain|stands? alone",
    "acceptance_contract": r"acceptance_criteria",
    "issue_anchor": r"quoted_text",
    "dependency_order": r"depends_on",
    "review_source": r"requirements_and_examples\.md",
    "appendix_source": r"appendix_requirements\.md",
    "no_fabrication": r"(?:NEVER|not|no|without)[^\n]{0,80}fabricat",
}

def main():
    results = {}
    actual = sorted(p.name for p in (ROOT / ".temp/agents").glob("*.md"))
    results["exact_prompt_inventory"] = actual == EXPECTED
    for name in EXPECTED:
        text = (ROOT / ".temp/agents" / name).read_text()
        checks = {key: not bool(re.search(pattern, text, re.I)) for key, pattern in FORBIDDEN.items()}
        checks.update({key: bool(re.search(pattern, text, re.I)) for key, pattern in REQUIRED.items()})
        results[name] = checks
    results["requirements_unchanged"] = {
        name: hashlib.sha256((ROOT / ".temp/acl_requirements" / name).read_bytes()).hexdigest() == digest
        for name, digest in SOURCES.items()
    }
    flat = [v for item in results.values() for v in (item.values() if isinstance(item, dict) else [item])]
    results["passed"] = all(flat)
    print(json.dumps(results, indent=2))
    return 0 if results["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
