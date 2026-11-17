# Emprico

Emprico derives GitHub collaboration automation from observed cases.

Each case records facts, a judgment, the smallest resulting rule, and later evidence. Repositories keep their own vocabulary; shared automation begins only where repeated cases agree.

## Current loop

1. A pull request names at least one Issue with a closing reference.
2. The Issue supplies the native Project context.
3. Pull request and Issue events advance conservative status labels.
4. Ambiguous transitions remain visible for a person or agent to judge.

The reusable workflows implement this loop without deployment or runtime authority. See [`docs/adoption.md`](docs/adoption.md).

## Evidence

[`evidence/re8ch-2026-11-17.json`](evidence/re8ch-2026-11-17.json) is the first aggregate inventory. [`cases/`](cases/) contains the decisions already supported by repository history.
