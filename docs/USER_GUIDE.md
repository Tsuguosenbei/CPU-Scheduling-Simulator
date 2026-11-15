# User Guide

## CPU Scheduling Simulator — PT 101

### 1. Requirements

- Python 3.10 or later
- Tkinter (included with most standard Python installations)
- A computer running Windows, macOS, or Linux with graphical desktop support

### 2. How to Run the Application

1. Download or clone the GitHub repository.
2. Extract the ZIP file if downloaded.
3. Open a terminal in the project folder.
4. Run:

   `python gui.py`

   On some systems, use `python3 gui.py`.

5. Wait for the CPU Scheduling Simulator window to appear.

### 3. Entering Process Information

The simulator accepts the following inputs:

| Input | Description |
|---|---|
| Process ID (PID) | Unique identifier for each process |
| Arrival Time (AT) | Time when a process becomes available |
| Burst Time (BT) | CPU execution time required |
| Priority | Scheduling priority; smaller number means higher priority |

**Input rules:**
- Arrival Time must be zero or greater.
- Burst Time must be greater than zero.
- Priority must be zero or greater.
- Process IDs must be unique.

### 4. Managing Processes

- **Load Sample:** Load predefined sample processes.
- **Add Process:** Add a process to the input table.
- **Remove Process:** Delete the selected process.
- **Run All Algorithms:** Execute all four scheduling algorithms.

### 5. Scheduling Algorithms

The application implements:

1. **FCFS (First Come, First Served):** Processes execute in arrival order.
2. **SJF (Shortest Job First):** Selects the available process with the shortest burst time; non-preemptive.
3. **SRTF (Shortest Remaining Time First):** Selects the available process with the shortest remaining execution time; preemptive.
4. **Priority Scheduling:** Selects the available process with the highest priority (lowest number); non-preemptive.

Tie-breaking follows earliest arrival time and original input order. In SRTF, the currently running process continues when remaining times are equal.

### 6. Understanding the Results

After clicking **Run All Algorithms**, select an algorithm tab to view its results.

**Gantt Chart**

The Gantt chart displays the execution order of processes, their start and end times, and CPU idle periods where applicable.

**Per-Process Metrics**

| Metric | Meaning | Formula |
|---|---|---|
| CT | Completion Time | Time when the process finishes |
| TAT | Turnaround Time | CT − AT |
| WT | Waiting Time | TAT − BT |
| RT | Response Time | First Start Time − AT |

**Average Metrics**

The application calculates the average Turnaround Time, Waiting Time, and Response Time across all processes.

### 7. Comparing Algorithms

Open the **Comparison** tab to view the results of FCFS, SJF, SRTF, and Priority Scheduling.

Compare their average metrics to evaluate performance for the given process inputs.

Lower average waiting and turnaround times generally indicate better performance for those particular inputs.

### 8. Closing the Application

Close the application using the window's close button.

### 9. Troubleshooting

**Application does not start**
- Verify that Python is installed.
- Confirm that Tkinter is available.
- Ensure that all required project files are present.

**Invalid process input**
- Check that the arrival time, burst time, and priority satisfy the input rules.
- Ensure that process IDs are unique.

**No results displayed**
- Add at least one valid process.
- Click **Run All Algorithms** again.
