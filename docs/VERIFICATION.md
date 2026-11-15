# Step 4.5 — Verification Record

Run: `python -m unittest discover -s tests -v`

Verified on 2026-11-15: **12 tests passed**.

## Case A — Three processes, staggered arrivals

| PID | AT | BT | Priority |
|---|---:|---:|---:|
| P1 | 0 | 8 | 3 |
| P2 | 1 | 4 | 1 |
| P3 | 2 | 2 | 2 |

Expected timelines (and actual, confirmed by automated tests):

- FCFS: P1 0–8, P2 8–12, P3 12–14.
- SJF: P1 0–8, P3 8–10, P2 10–14.
- SRTF: P1 0–1, P2 1–2, P3 2–4, P2 4–7, P1 7–14.
- Priority (non-preemptive): P1 0–8, P2 8–12, P3 12–14.

SRTF expected and actual per-process metrics:

| PID | CT | TAT | WT | RT |
|---|---:|---:|---:|---:|
| P1 | 14 | 14 | 6 | 0 |
| P2 | 7 | 6 | 2 | 0 |
| P3 | 4 | 2 | 0 | 0 |

## Case B — CPU initially idle

Input: P1 AT=4, BT=2, priority=1.
Expected and actual for all algorithms: IDLE 0–4, P1 4–6; CT=6, TAT=2, WT=0, RT=0.

## Case C — Simultaneous arrivals and ties

Input: P1 and P2 both AT=0, BT=3, priority=1; P1 input first.
Expected and actual for all algorithms: P1 0–3, P2 3–6.

## Additional checks

- Original process data is unchanged by simulation.
- Invalid zero burst time is rejected.
- SRTF does not preempt when remaining times are equal.

These are automated test results, not evidence of a user-operated live demonstration. Run the console application separately before presenting.
