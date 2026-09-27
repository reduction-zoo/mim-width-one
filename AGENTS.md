# Research instructions

Read the [fixed question](campaigns/mim-width-one/question.md), [prior state](campaigns/mim-width-one/state.md) and [preparation notes](campaigns/mim-width-one/work/preparation.md). The fixed [test corpus](campaigns/mim-width-one/work/cases.json) and [verifier](campaigns/mim-width-one/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/mim-width-one/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Scope and budgets in the state describe earlier work and do not limit a new campaign. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
