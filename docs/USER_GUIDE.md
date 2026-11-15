# User Guide

1. Install Python 3.10 or later.
2. Open a terminal in the project folder.
3. Run `python main.py` (on some systems use `python3 main.py`).
4. Choose menu option 6 to enter or replace process data, or choose an algorithm and follow the input prompts.
5. Enter the number of processes (positive integer). For each process, enter arrival time (>=0), burst time (>0), and priority (>=0; smaller means higher priority).
6. Choose 1–4 for a single algorithm or 5 to compare all four.
7. Read the timeline (start--PID--end), per-process metrics and average metrics.
8. Choose 7 to exit.

AT = arrival time; BT = burst time; PRI = priority; CT = completion time; TAT = turnaround time; WT = waiting time; RT = response time. IDLE means no process was available.

Scheduling tie-breaking: earliest arrival then original input order. SRTF retains the running process when remaining times are equal.
