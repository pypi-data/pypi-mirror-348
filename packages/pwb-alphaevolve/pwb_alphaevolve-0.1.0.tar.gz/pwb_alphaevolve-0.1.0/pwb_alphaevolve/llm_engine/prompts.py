"""
Generate chat messages given the current parent strategy and a hall-of-fame
snapshot.  The model is instructed to reply **only** with a JSON object:

    {
      "blocks": {
         "<block_name>": "<new python code...>",
         ...
      }
    }

If it decides a full rewrite is better, it can omit "blocks" and instead
return:

    { "code": "<full python code>" }
"""

import textwrap, json
from datetime import datetime
from typing import Dict, Any, List

from pwb_alphaevolve.store.sqlite import ProgramStore


SYSTEM_MSG = """\
You are Alpha-Trader Evolution-Engine.  You mutate algorithmic-trading
strategies written for Backtrader.  All editable regions are delimited
like this:

    # === EVOLVE-BLOCK: <block_name> =================================
    ...current implementation...
    # === END EVOLVE-BLOCK ===========================================

**Return ONLY valid JSON** with either:
  • "blocks": an object mapping <block_name> ➝ replacement code *inside*
    that block (keep indentation coherent), or
  • "code": a complete strategy (if a wholesale rewrite is easier).

NO additional keys, NO markdown, NO prose explanation.
"""

USER_TEMPLATE = """\
Today's date: {today}

Parent KPIs:
{metrics_tbl}

Parent code (trimmed):
```python
{parent_code}
```

Hall-of-fame excerpt (top {k} Sharpe):
{hof}

Task:
  1. Improve the risk-adjusted performance (Sharpe & Calmar) while keeping drawdown below -25 %.
  2. Modify ONLY the content of EVOLVE-BLOCKs shown above unless you choose to emit a full "code".
  3. Reply using the structured JSON schema described by the system prompt.
"""


def _format_metrics(metrics: Dict[str, Any] | None) -> str:
    if not metrics:
        return "  (none yet – seed strategy)"
    return "\n".join(f"  {k}: {v:.4g}" for k, v in metrics.items())


def _format_hof(store: ProgramStore, k: int = 3) -> str:
    rows = store.top_k(k=k)
    if not rows:
        return "  (empty – still warming up)"
    lines = []
    for r in rows:
        m = r["metrics"]
        lines.append(
            f"  Sharpe {m['sharpe']:.3f} | Calmar {m['calmar']:.3f} | "
            f"CAGR {m['cagr']:.2%}"
        )
    return "\n".join(lines)


def build(parent: Dict[str, Any] | None, store: ProgramStore) -> List[Dict[str, str]]:
    """Return messages list ready for openai.ChatCompletion."""
    today = datetime.utcnow().date().isoformat()
    parent_code = textwrap.indent(
        textwrap.dedent(parent["code"] if parent else ""), "    "
    )[
        :4000
    ]  # truncate for token safety
    user_msg = USER_TEMPLATE.format(
        today=today,
        metrics_tbl=_format_metrics(parent["metrics"] if parent else None),
        parent_code=parent_code or "(root seed – no parent)",
        hof=_format_hof(store, k=3),
        k=3,
    )
    return [
        {"role": "system", "content": SYSTEM_MSG},
        {"role": "user", "content": user_msg},
    ]
