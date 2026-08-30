"""Task dependency helpers for sequencer waves."""
from __future__ import annotations

from typing import Any


def validate_tasks(tasks: list[dict[str, Any]]) -> None:
    ids = {t["id"] for t in tasks}
    if len(ids) != len(tasks):
        raise ValueError("duplicate task ids")
    for t in tasks:
        for d in t.get("deps") or []:
            if d not in ids:
                raise ValueError(f"task {t['id']} deps unknown id {d}")
    # cycle check
    visiting: set[str] = set()
    done: set[str] = set()
    by_id = {t["id"]: t for t in tasks}

    def walk(tid: str) -> None:
        if tid in done:
            return
        if tid in visiting:
            raise ValueError(f"cycle at {tid}")
        visiting.add(tid)
        for d in by_id[tid].get("deps") or []:
            walk(d)
        visiting.remove(tid)
        done.add(tid)

    for tid in ids:
        walk(tid)


def ready_tasks(tasks: list[dict[str, Any]], completed: set[str]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for t in tasks:
        tid = t["id"]
        if tid in completed:
            continue
        deps = t.get("deps") or []
        if all(d in completed for d in deps):
            out.append(t)
    return out


def wave_for_parallel(
    ready: list[dict[str, Any]], max_workers: int
) -> list[dict[str, Any]]:
    """Take up to max_workers ready tasks with unique target paths."""
    if max_workers <= 1:
        return ready[:1]
    wave: list[dict[str, Any]] = []
    seen_targets: set[str] = set()
    for t in ready:
        if len(wave) >= max_workers:
            break
        target = t.get("target") or t["id"]
        if target in seen_targets:
            continue
        seen_targets.add(target)
        wave.append(t)
    return wave or ready[:1]
