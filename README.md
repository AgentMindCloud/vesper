# Vesper

**Next-generation voice presence agent for X.**

Real-time companion. Governed memory. Live X context. Reactive visual presence. Proactive initiation. Built on the full xlOS + grok-yaml-standards stack.

> Speak. It remembers with contracts. It sees the live timeline. It can appear. It can initiate. It never ships without your approval.

---

## What Vesper is

Vesper elevates the original voice-companion pattern into a full presence layer:

- **Real-time voice** with emotion-aware TTS, barge-in, speaker diarization, and sub-second first-audio budgets.
- **Governed memory** — every memory item carries provenance, confidence, scope, retention rule, and write permissions. Cross-session when you allow it, fully auditable and revocable.
- **Live X context** — every turn can silently pull relevant recent posts, mentions, or trends and weave them into the spoken response.
- **Reactive visual presence** (optional) — Grok Imagine avatar that updates expression and status in real time.
- **Proactive mode** — Vesper can initiate a voice session when something important happens on your timeline (mention spikes, opportunities).
- **Full safety Constitution** — Articles I, III, VII enforced. Kill switches, rate limits, human approval on every external write.
- **xlOS native** — installable as a first-class agent with runtime dispatch.

## Quick start

```bash
# Once xlOS is installed
xlos install github.com/AgentMindCloud/vesper

# Or via grok-install
grok-install install github.com/AgentMindCloud/vesper
```

## Architecture

```
User voice / X event / Proactive trigger
                ↓
┌───────────────────────────┐
│  Coordinator Agent        │  ← real-time + live X context injection
│  (grok-4.20-multi-agent)  │
└──────────┬────────────────┘
           │
     ┌─────┴─────┐
     ↓           ↓
Memory Keeper   Visual Presence
(governed)      (Imagine avatar)
     ↓
Governed Memory Store + Proactive Policy
```

## Safety

- Profile: `standard` (voice real-time) + full Constitution (I, III, VII)
- Kill switch: `VESPER_DISABLED=1`
- Memory encrypted at rest, contracts required, cross-session opt-in only
- Every external write still requires human approval

## Status

**Core complete.** All next layers (live context, avatar reactivity, proactive initiation, xlOS runtime wiring) are implemented and committed.

See [STATUS.md](STATUS.md) for the full checklist.

Built by AgentMindCloud · Independent community project. Not affiliated with xAI, Grok, or X.

---

**Vesper.** Presence, not just chat.
