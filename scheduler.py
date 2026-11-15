from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Process:
    pid: str
    arrival_time: int
    burst_time: int
    priority: int
    input_order: int


@dataclass(frozen=True)
class Segment:
    pid: str
    start: int
    end: int


@dataclass
class ScheduleResult:
    algorithm: str
    segments: list[Segment]
    completion: dict[str, int]
    first_start: dict[str, int]


def validate_processes(processes: list[Process]) -> None:
    if not processes:
        raise ValueError('Enter at least one process.')
    ids = set()
    orders = set()
    for p in processes:
        if not p.pid.strip() or p.pid == 'IDLE':
            raise ValueError('Process ID cannot be blank or IDLE.')
        if p.pid in ids or p.input_order in orders:
            raise ValueError('Process IDs and input orders must be unique.')
        ids.add(p.pid)
        orders.add(p.input_order)
        if any(type(v) is not int for v in (p.arrival_time, p.burst_time, p.priority, p.input_order)):
            raise ValueError('Arrival, burst, priority, and input order must be integers.')
        if p.arrival_time < 0 or p.burst_time <= 0 or p.priority < 0 or p.input_order < 0:
            raise ValueError('Arrival, priority and input order must be nonnegative; burst must be positive.')


def _add(segments: list[Segment], pid: str, start: int, end: int) -> None:
    if end <= start:
        return
    if segments and segments[-1].pid == pid and segments[-1].end == start:
        previous = segments[-1]
        segments[-1] = Segment(pid, previous.start, end)
    else:
        segments.append(Segment(pid, start, end))


def _nonpreemptive(processes: list[Process], algorithm: str) -> ScheduleResult:
    validate_processes(processes)
    pending = list(processes)
    time = 0
    segments: list[Segment] = []
    completion: dict[str, int] = {}
    first_start: dict[str, int] = {}
    while pending:
        ready = [p for p in pending if p.arrival_time <= time]
        if not ready:
            next_time = min(p.arrival_time for p in pending)
            _add(segments, 'IDLE', time, next_time)
            time = next_time
            ready = [p for p in pending if p.arrival_time <= time]
        if algorithm == 'FCFS':
            chosen = min(ready, key=lambda p: (p.arrival_time, p.input_order))
        elif algorithm == 'SJF':
            chosen = min(ready, key=lambda p: (p.burst_time, p.arrival_time, p.input_order))
        else:
            chosen = min(ready, key=lambda p: (p.priority, p.arrival_time, p.input_order))
        first_start[chosen.pid] = time
        end = time + chosen.burst_time
        _add(segments, chosen.pid, time, end)
        time = end
        completion[chosen.pid] = time
        pending.remove(chosen)
    return ScheduleResult(algorithm, segments, completion, first_start)


def fcfs(processes: list[Process]) -> ScheduleResult:
    return _nonpreemptive(processes, 'FCFS')


def sjf(processes: list[Process]) -> ScheduleResult:
    return _nonpreemptive(processes, 'SJF')


def priority_scheduling(processes: list[Process]) -> ScheduleResult:
    return _nonpreemptive(processes, 'Priority')


def srtf(processes: list[Process]) -> ScheduleResult:
    validate_processes(processes)
    remaining = {p.pid: p.burst_time for p in processes}
    completion: dict[str, int] = {}
    first_start: dict[str, int] = {}
    segments: list[Segment] = []
    time = 0
    current: Optional[Process] = None
    while len(completion) < len(processes):
        ready = [p for p in processes if p.arrival_time <= time and remaining[p.pid] > 0]
        if not ready:
            next_time = min(p.arrival_time for p in processes if remaining[p.pid] > 0)
            _add(segments, 'IDLE', time, next_time)
            time = next_time
            current = None
            continue
        shortest = min(ready, key=lambda p: (remaining[p.pid], p.arrival_time, p.input_order))
        if current is None or remaining[current.pid] == 0 or current.arrival_time > time:
            current = shortest
        elif remaining[shortest.pid] < remaining[current.pid]:
            current = shortest
        first_start.setdefault(current.pid, time)
        # The next arrival is the earliest possible preemption point.
        future = [p.arrival_time for p in processes if p.arrival_time > time and remaining[p.pid] > 0]
        next_arrival = min(future) if future else time + remaining[current.pid]
        duration = min(remaining[current.pid], next_arrival - time)
        _add(segments, current.pid, time, time + duration)
        time += duration
        remaining[current.pid] -= duration
        if remaining[current.pid] == 0:
            completion[current.pid] = time
            current = None
    return ScheduleResult('SRTF', segments, completion, first_start)
