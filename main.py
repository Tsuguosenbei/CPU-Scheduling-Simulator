from input_handler import read_processes
from scheduler import fcfs, sjf, srtf, priority_scheduling
from display import show_result

ALGORITHMS = {'1': fcfs, '2': sjf, '3': srtf, '4': priority_scheduling}


def main() -> None:
    processes = None
    while True:
        print('\n=== CPU SCHEDULING SIMULATOR ===')
        print('1. FCFS\n2. SJF\n3. SRTF\n4. Priority (Non-preemptive)')
        print('5. Compare All\n6. Enter / Replace Processes\n7. Exit')
        choice = input('Select option: ').strip()
        if choice == '7':
            print('Goodbye!')
            break
        if choice == '6':
            processes = read_processes()
            continue
        if choice not in (*ALGORITHMS, '5'):
            print('Invalid menu option.')
            continue
        if processes is None:
            print('Enter process data first.')
            processes = read_processes()
        selected = ALGORITHMS.values() if choice == '5' else [ALGORITHMS[choice]]
        summary = []
        for algorithm in selected:
            result = algorithm(processes)
            averages = show_result(processes, result)
            summary.append((result.algorithm, averages))
        if choice == '5':
            print('\n=== ALGORITHM COMPARISON (LOWER AVERAGE IS BETTER) ===')
            for name, avg in summary:
                print(f"{name:<10} TAT={avg['tat']:.2f} WT={avg['wt']:.2f} RT={avg['rt']:.2f}")
            for key in ('tat', 'wt', 'rt'):
                best = min(avg[key] for _, avg in summary)
                winners = ', '.join(name for name, avg in summary if abs(avg[key] - best) < 1e-9)
                print(f'Best average {key.upper()}: {winners} ({best:.2f})')


if __name__ == '__main__':
    main()
