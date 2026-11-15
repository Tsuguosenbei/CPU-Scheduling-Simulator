from scheduler import Process, ScheduleResult


def metrics(processes: list[Process], result: ScheduleResult) -> tuple[list[dict], dict[str, float]]:
    rows = []
    for p in sorted(processes, key=lambda x: x.input_order):
        ct = result.completion[p.pid]
        tat = ct - p.arrival_time
        wt = tat - p.burst_time
        rt = result.first_start[p.pid] - p.arrival_time
        rows.append({'pid': p.pid, 'at': p.arrival_time, 'bt': p.burst_time,
                     'priority': p.priority, 'ct': ct, 'tat': tat, 'wt': wt, 'rt': rt})
    averages = {key: sum(row[key] for row in rows) / len(rows) for key in ('tat', 'wt', 'rt')}
    return rows, averages
