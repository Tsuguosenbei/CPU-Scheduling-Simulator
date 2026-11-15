# PT 101 — CPU Scheduling Simulator (Python)

Simulates FCFS, non-preemptive SJF, preemptive SRTF, and **non-preemptive Priority** scheduling using actual calculations. Lower priority number means higher priority. Ties use earlier arrival, then input order; SRTF only preempts for strictly shorter remaining time.

## Run the graphical version (Tkinter)

Install Python 3.10 or newer, including Tkinter support. For smooth rounded buttons, install Pillow with `python -m pip install -r requirements.txt` (without Pillow, standard buttons are used). From the project folder:

```bash
python gui.py
```

On some Windows installations use `py gui.py`. Tkinter is bundled with most Python distributions. On Linux, a separate `python3-tk` system package may be necessary.

1. Use **Load Sample** or add processes with unique IDs, nonnegative arrival and priority, and positive burst.
2. Click **Run All Algorithms**.
3. Explore each algorithm tab for the Gantt timeline, per-process metrics, and averages.
4. Open **Comparison** to compare average TAT, WT, and RT.
5. Edit processes and click **Run All Algorithms** again to update results.

## Run the original console version

```bash
python main.py
```

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Calculation rules

- CT: completion time
- TAT = CT - AT
- WT = TAT - BT
- RT = first execution start - AT
- Averages are arithmetic means over all processes.

## Code organization

- `gui.py`: Tkinter interface, input table, Gantt canvas, result tabs and comparison
- `scheduler.py`: algorithms and validation (independent of GUI)
- `calculations.py`: metrics and averages
- `main.py`, `input_handler.py`, `display.py`: optional original console interface
- `tests/`: automated algorithm tests
- `docs/`: user guide, testing and contribution documentation

The application requires a desktop graphical environment; a headless terminal or online code runner may not be able to open Tkinter windows.

For the course contribution record, document actual work performed by each student.

## Refined Tkinter interface

Run `python gui.py` to launch the desktop interface. It features a process workspace, four algorithm tabs, a comparison view, color-coded Gantt timelines, and summary metric cards. Editing the process list clears old simulation results so they cannot be mistaken for current outputs. The scheduler remains independent of the GUI.
