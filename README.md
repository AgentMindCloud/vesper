<p align="center">
  <img src="docs/logo.svg" alt="Vesper logo" width="140">
</p>

<h1 align="center">Vesper</h1>

<p align="center">
  <strong>Next-generation voice presence agent for X</strong><br>
  Real-time companion · Governed memory · Live X context · Reactive visual presence
</p>

<p align="center">
  <em>Speak. It remembers with contracts. It sees the live timeline. It can appear. It can initiate.</em>
</p>

---

## What Vesper is

Vesper is a voice-first presence agent built on the xlOS + grok-yaml-standards stack.  
It elevates the original voice-companion pattern into something that feels like a real presence rather than a chatbot.

- **Real-time voice** — emotion-aware TTS, barge-in, speaker diarization, strict latency budgets
- **Governed memory** — every fact carries provenance, confidence, scope, retention, and write permissions
- **Live X context** — silently pulls relevant recent posts/mentions into the conversation
- **Reactive visual presence** — optional Grok Imagine avatar that updates expression & status
- **Proactive mode** — can initiate a voice session on mention spikes or high-signal events (opt-in)
- **Full safety Constitution** — Articles I, III, VII enforced + kill switch + rate limits

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/AgentMindCloud/vesper.git
cd vesper
```

### 2. Look at the agent

The actual agent lives here:

```bash
cd agents/vesper-core
ls .grok/
```

<p align="center">
  <img src="docs/screenshots/01-clone-and-structure.svg" alt="Clone and inspect the agent structure" width="680">
</p>

You will see all the YAML files that define the swarm, memory contracts, voice settings, safety, proactive policy, etc.

### 3. Install with grok-install (recommended)

```bash
grok-install install github.com/AgentMindCloud/vesper/agents/vesper-core
```

Or if you already have xlOS:

```bash
xlos install github.com/AgentMindCloud/vesper/agents/vesper-core
```

<p align="center">
  <img src="docs/screenshots/02-install.svg" alt="Successful install of Vesper" width="680">
</p>

### 4. Configure secrets

Create a `.env` file (or copy from `.env.example` if present) with at least:

```bash
XAI_API_KEY=your_key_here
X_BEARER_TOKEN=your_token_here
GROK_VOICE_API_KEY=your_voice_key_here
```

### 5. Run (when the runtime is available)

```bash
grok-install run
# or
xlos run vesper
```

> **Note:** Full end-to-end voice runtime still depends on the Grok multi-agent + voice endpoints being available in your environment. The YAML + Python stubs are ready; the live loop is what the runtime provides.

---

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

---

## Safety

- Profile: `standard` (real-time voice) + full Constitution (Articles I, III, VII)
- Kill switch: `VESPER_DISABLED=1`
- Memory is encrypted at rest. Cross-session memory is opt-in only.
- Every external write still requires human approval.

---

## Status

**Core is complete.**  
See [STATUS.md](STATUS.md) for the full checklist of what has been implemented.

Built by AgentMindCloud · Independent community project.  
Not affiliated with xAI, Grok, or X.

---

**Vesper.** Presence, not just chat.
