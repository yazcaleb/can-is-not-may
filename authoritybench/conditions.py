"""
Enforcement condition implementations for AuthorityBench.

Four conditions:
  prompt_only              — no enforcement; model output is accepted as-is
  guardrail                — keyword-based string matching on tool name
  authority_model          — deterministic policy check with history-aware chain blocking
  authority_model_stateless — same policy check but without history (ablation for H)
"""

from typing import Literal

Decision = Literal["allow", "deny", "require_approval"]


def prompt_only_check(
    tool_name: str, args: dict, scenario: dict, history: list[dict] | None = None
) -> Decision:
    """No enforcement. Every tool call the model makes is allowed."""
    return "allow"


def guardrail_check(
    tool_name: str, args: dict, scenario: dict, history: list[dict] | None = None
) -> Decision:
    """
    Keyword-based guardrail. Blocks tool calls whose name contains any
    deny keyword from the scenario config.

    Weakness by design: adversarial rephrasing (e.g. 'remove_file' instead of
    'delete_file') bypasses this check — that's the point being measured.
    """
    deny_keywords: list[str] = scenario.get("guardrail_deny_keywords", [])
    tool_lower = tool_name.lower()
    for keyword in deny_keywords:
        if str(keyword).lower() in tool_lower:
            return "deny"
    return "allow"


def authority_model_check(
    tool_name: str, args: dict, scenario: dict, history: list[dict] | None = None
) -> Decision:
    """
    Deterministic authority model check.

    Enforces the scenario's authorized_tools list, optional argument-level
    constraints, AND history-aware chain blocking (chain_blocked_after).
    """
    authorized: list[str] = scenario.get("authorized_tools", [])
    require_approval: list[str] = scenario.get("require_approval_tools", [])

    if tool_name not in authorized:
        if tool_name in require_approval:
            return "require_approval"
        return "deny"

    # Argument-level constraints (e.g., allowed path prefixes)
    constraints: dict = scenario.get("authority_constraints", {}).get(tool_name, {})
    if constraints:
        path_prefix = constraints.get("allowed_path_prefix")
        if path_prefix:
            path = str(args.get("path", args.get("url", "")))
            if not path.startswith(path_prefix):
                return "deny"

        url_domain = constraints.get("allowed_domain")
        if url_domain:
            url = str(args.get("url", ""))
            if url_domain not in url:
                return "deny"

    # History-aware chain blocking: if a prior tool call in this session
    # triggers a chain rule, deny the current call.
    chain_rules = scenario.get("chain_blocked_after", {})
    if chain_rules and history:
        for prior in history:
            blocked = chain_rules.get(prior["tool_name"], [])
            if tool_name in blocked:
                return "deny"

    return "allow"


def authority_model_stateless_check(
    tool_name: str, args: dict, scenario: dict, history: list[dict] | None = None
) -> Decision:
    """Authority model without history — ablation for measuring H's contribution."""
    return authority_model_check(tool_name, args, scenario, history=None)


CONDITION_CHECKERS = {
    "prompt_only": prompt_only_check,
    "guardrail": guardrail_check,
    "authority_model": authority_model_check,
    "authority_model_stateless": authority_model_stateless_check,
}

CONDITIONS = list(CONDITION_CHECKERS.keys())
