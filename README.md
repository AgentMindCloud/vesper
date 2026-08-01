# Vesper

**Next-generation voice presence agent for X.**

Real-time companion. Governed memory. Live X context. Reactive visual presence. Built on the full xlOS + grok-yaml-standards stack.

> Speak. It remembers with contracts. It sees the live timeline. It can appear. It never ships without your approval.

---

## What Vesper is

Vesper elevates the original voice-companion pattern into a full presence layer:

- **Real-time voice** with emotion-aware TTS, barge-in, speaker diarization, and sub-second first-audio budgets.
- **Governed memory** — every memory item carries provenance, confidence, scope, retention rule, and write permissions. Cross-session when you allow it, fully auditable and revocable.
- **Live X context** — every turn can silently pull relevant recent posts, mentions, or trends and weave them into the spoken response.
- **Reactive visual presence** (optional) — Grok Imagine avatar that updates expression and status in real time.
- **Proactive mode** — Vesper can initiate a voice session when something important happens on your timeline.
- **Full safety Constitution** — Articles I, III, VII enforced. Kill switches, rate limits, human approval on every external write.
- **xlOS native** — installable as a first-class agent.

## Quick start

```bash
# Once xlOS is installed
xlos install github.com/AgentMindCloud/vesper

# Or via grok-install
grok-install install github.com/AgentMindCloud/vesper
```

## Architecture (high level)

```
User voice / X event
        ↓
┌───────────────────────┐
│  Coordinator Agent    │  ← real-time, latency budget, live X context
│  (grok-4.20-multi)    │
└──────────┬────────────┘
           │
     ┌─────┴─────┐
     ↓           ↓
Memory Keeper   Visual Presence
(governed)      (Imagine avatar)
     ↓
Governed Memory Store
(session + optional cross-session contracts)
```

## Safety

- Profile: `standard` (voice real-time) with non-approval safety controls + full Constitution.
- Every external write still requires human approval.
- Kill switch: `VESPER_DISABLED=1`
- Memory is encrypted at rest. Cross-session memory is opt-in and revocable.

## Status

MVP scaffold live. Core voice loop + governed memory contracts + live context injection + xlOS integration.

Built by AgentMindCloud · Independent community project. Not affiliated with xAI, Grok, or X.

---

**Vesper.** Presence, not just chat.
