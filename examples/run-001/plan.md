# Plan — scripts/codegen_parse helper

Goal: Add a pure Python helper used by manager/sequencer loops to parse no-tool worker output.

Units:
1. `parse_worker_response` in `scripts/codegen_parse.py`
2. Tests in `tests/test_codegen_parse.py` (manager may author tests; worker implements library)

Done when: `python -m pytest tests/test_codegen_parse.py -q` passes in workspace.
