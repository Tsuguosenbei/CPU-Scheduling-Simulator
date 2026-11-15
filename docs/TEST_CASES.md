# Manual Testing Evidence

The expected scheduling results were checked against the actual Tkinter output. Full screenshots are in `screenshots/`. The editable formal report is `PT101_CPU_Scheduling_Testing_Report.docx`.

| Case | Scenario | FCFS | SJF | SRTF | Priority |
|---|---|---|---|---|---|
| TC1 | Normal process arrivals | PASS | PASS | PASS | PASS |
| TC2 | Same arrival times and tie-breaking | PASS | PASS | PASS | PASS |
| TC3 | CPU idle time and preemption | PASS | PASS | PASS | PASS |

## Input datasets

- **TC1**: P1(AT=0, BT=5, priority=2), P2(1,3,1), P3(2,2,3).
- **TC2**: P1(0,6,2), P2(0,3,1), P3(0,3,1), P4(0,2,3).
- **TC3**: P1(2,7,3), P2(4,3,1), P3(5,1,2), P4(12,2,1).

## Expected and observed averages (TAT / WT / RT)

| Case | FCFS | SJF | SRTF | Priority |
|---|---|---|---|---|
| TC1 | 6.67 / 3.33 / 3.33 | 6.33 / 3.00 / 3.00 | 5.67 / 2.33 / 0.67 | 6.67 / 3.33 / 3.33 |
| TC2 | 10.25 / 6.75 / 6.75 | 7.25 / 3.75 / 3.75 | 7.25 / 3.75 / 3.75 | 8.75 / 5.25 / 5.25 |
| TC3 | 6.50 / 3.25 / 3.25 | 6.00 / 2.75 / 2.75 | 4.75 / 1.50 / 0.25 | 6.75 / 3.50 / 3.50 |

All three test cases also include a comparison screenshot.
