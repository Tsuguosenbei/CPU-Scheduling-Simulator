from scheduler import Process, ScheduleResult
from calculations import metrics


def show_result(processes: list[Process], result: ScheduleResult) -> dict[str, float]:
    rows, averages = metrics(processes, result)
    print(f'\n=== {result.algorithm} ===')
    print('Gantt chart / timeline:')
    print(' | '.join(f'{s.start}--{s.pid}--{s.end}' for s in result.segments))
    print(f"{'PID':<8}{'AT':>5}{'BT':>5}{'PRI':>6}{'CT':>6}{'TAT':>6}{'WT':>6}{'RT':>6}")
    for r in rows:
        print(f"{r['pid']:<8}{r['at']:>5}{r['bt']:>5}{r['priority']:>6}{r['ct']:>6}{r['tat']:>6}{r['wt']:>6}{r['rt']:>6}")
    print(f"Average TAT: {averages['tat']:.2f} | WT: {averages['wt']:.2f} | RT: {averages['rt']:.2f}")
    return averages
