"""Additional verification cases for PT 101 CPU Scheduling Simulator."""
import unittest
from scheduler import Process, fcfs, sjf, srtf, priority_scheduling
from calculations import metrics


class AdditionalSchedulerTests(unittest.TestCase):
    def setUp(self):
        self.ps = [
            Process('P1', 0, 8, 3, 0),
            Process('P2', 1, 4, 1, 1),
            Process('P3', 2, 2, 2, 2),
        ]

    def test_fcfs_full_results(self):
        result = fcfs(self.ps)
        rows, avg = metrics(self.ps, result)
        self.assertEqual([(r['ct'], r['tat'], r['wt'], r['rt']) for r in rows],
                         [(8, 8, 0, 0), (12, 11, 7, 7), (14, 12, 10, 10)])
        self.assertAlmostEqual(avg['wt'], 17 / 3)

    def test_sjf_nonpreemptive(self):
        result = sjf(self.ps)
        self.assertEqual([(s.pid, s.start, s.end) for s in result.segments],
                         [('P1', 0, 8), ('P3', 8, 10), ('P2', 10, 14)])
        self.assertEqual(result.completion, {'P1': 8, 'P3': 10, 'P2': 14})

    def test_priority_nonpreemptive(self):
        result = priority_scheduling(self.ps)
        self.assertEqual([(s.pid, s.start, s.end) for s in result.segments],
                         [('P1', 0, 8), ('P2', 8, 12), ('P3', 12, 14)])

    def test_srtf_full_results(self):
        result = srtf(self.ps)
        self.assertEqual([(s.pid, s.start, s.end) for s in result.segments],
                         [('P1', 0, 1), ('P2', 1, 2), ('P3', 2, 4),
                          ('P2', 4, 7), ('P1', 7, 14)])
        rows, _ = metrics(self.ps, result)
        self.assertEqual([(r['ct'], r['tat'], r['wt'], r['rt']) for r in rows],
                         [(14, 14, 6, 0), (7, 6, 2, 0), (4, 2, 0, 0)])

    def test_all_algorithms_idle(self):
        ps = [Process('P1', 4, 2, 1, 0)]
        for algorithm in (fcfs, sjf, srtf, priority_scheduling):
            with self.subTest(algorithm=algorithm.__name__):
                result = algorithm(ps)
                self.assertEqual([(s.pid, s.start, s.end) for s in result.segments],
                                 [('IDLE', 0, 4), ('P1', 4, 6)])
                rows, _ = metrics(ps, result)
                self.assertEqual((rows[0]['tat'], rows[0]['wt'], rows[0]['rt']), (2, 0, 0))

    def test_simultaneous_arrival_input_order(self):
        ps = [Process('P1', 0, 3, 1, 0), Process('P2', 0, 3, 1, 1)]
        for algorithm in (fcfs, sjf, srtf, priority_scheduling):
            with self.subTest(algorithm=algorithm.__name__):
                self.assertEqual([s.pid for s in algorithm(ps).segments], ['P1', 'P2'])

    def test_original_processes_unchanged(self):
        snapshot = list(self.ps)
        for algorithm in (fcfs, sjf, srtf, priority_scheduling):
            algorithm(self.ps)
        self.assertEqual(self.ps, snapshot)


if __name__ == '__main__':
    unittest.main()
