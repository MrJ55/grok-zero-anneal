# scripts/

| File | Role |
|------|------|
| `cli.py` / `__main__.py` | `python -m scripts.cli` |
| `run_init.py` | Create run dir from template |
| `worker_client.py` | Pure-text workers (Muse default) |
| `sequencer.py` | Stages + parallel waves |
| `stages.py` / `rebrief.py` | Anneal helpers |
| `state_store.py` / `task_graph.py` / `brief_format.py` | Ledger |
| `codegen_parse.py` | Parse worker markdown |
| `openrouter_sequencer.py` | Historical |

```bash
python -m scripts.cli init-run runs/x --goal "..."
python -m scripts.cli check-auth
python -m scripts.cli run --run-dir runs/x --parallel 4
```
