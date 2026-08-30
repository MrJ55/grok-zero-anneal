## Run notes

- Worker Laguna a1 produced correct logic; sequencer extract_code truncated at inner ``` in docstring.
- Manager re-integrated full module from worker intent + contract; pytest green.
- Attempts 2–3: OpenRouter 429 rate limit on free model.
- Lesson: worker prompts should avoid triple-backticks inside docstrings, or sequencer needs balanced-fence parsing.
