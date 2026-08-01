# Vesper Examples

## sample_memory_contracts.json

Three realistic governed memory contracts showing the required fields:

- `content` — the fact itself
- `source` — `user_said` | `x_context` | `derived` | `system`
- `confidence` — 0.0–1.0
- `scope` — `session` | `user` | `global`
- `retention_days` — 0 = session only
- `write_permission` — `user_only` | `agent` | `system`
- timestamps

Load them in Python:

```python
import json
from vesper.memory import MemoryStore, validate_contract

with open("examples/sample_memory_contracts.json") as f:
    facts = json.load(f)

store = MemoryStore(cross_session_enabled=True)
for fact in facts:
    # Cross-session facts need consent
    consent = fact["scope"] != "session"
    store.write(fact, user_consent_for_cross_session=consent)

print(store.query(max_records=5))
```
