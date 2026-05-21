# Agent Briefs

System prompts for the Nederly meta-build pipeline. Each `.md` here is the brief given to a subagent when it is spawned.

## Pipeline
```
Researcher ─→ [Gate 0] ─→ ┌─ Dutch Expert ─→ Phonetics ─┐
                          └─ Dyslexia Expert ────────────┴─→ [Gate 1] ─→ Designer ─→ [Gate 2] ─→ Builder ─→ [Final]
```

## Files

| Brief | Role | Inputs | Output |
|---|---|---|---|
| [manager.md](manager.md) | Orchestrator + reviewer (Claude Code itself) | All agent outputs | Gate decisions, revision requests |
| [researcher.md](researcher.md) | External evidence + lesson notes summary | Web sources + `Lesson Notes/` | `docs/agents/researcher.md` |
| [dutch_expert.md](dutch_expert.md) | A0 Dutch knowledge | Researcher | `docs/agents/dutch_expert.md` |
| [dyslexia_expert.md](dyslexia_expert.md) | UX principles for dyslexia | Researcher | `docs/agents/dyslexia_expert.md` |
| [phonetics.md](phonetics.md) | Dutch sound system, traps, drills | Researcher + Dutch + Dyslexia MDs | `docs/agents/phonetics.md` |
| [designer.md](designer.md) | Buildable app design spec | All 4 upstream MDs | `docs/agents/design_spec.md` |
| [builder.md](builder.md) | Working code | `design_spec.md` (+ refs) | Updates to `nederly.html` |

## Editing
Edit any brief before its agent runs to change scope/output. After it runs, edits won't retro-apply.

## Manager artifacts

| File | Purpose |
|---|---|
| `../manager_memory.md` | Cross-run ledger — Manager reads at start of every run, appends at end. Holds run index, persistent decisions, VERSION numbers used, recurring patterns, open follow-ups. |
| `../reports/YYYY-MM-DD-NN-report.md` | One per pipeline run, written after Gate 3 passes. Documents run metadata, gate decisions, app changes, files touched, deferred work. |
