from scheduler import Process, validate_processes


def read_integer(prompt: str, minimum: int = 0) -> int:
    while True:
        try:
            value = int(input(prompt).strip())
            if value >= minimum:
                return value
        except ValueError:
            pass
        print(f'Please enter an integer greater than or equal to {minimum}.')


def read_processes() -> list[Process]:
    count = read_integer('Number of processes: ', 1)
    processes = []
    for i in range(count):
        print(f'\nProcess P{i + 1}')
        at = read_integer('Arrival time: ')
        bt = read_integer('Burst time: ', 1)
        priority = read_integer('Priority (lower = higher): ')
        processes.append(Process(f'P{i + 1}', at, bt, priority, i))
    validate_processes(processes)
    return processes
