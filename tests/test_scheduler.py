import unittest
from scheduler import Process, fcfs, sjf, srtf, priority_scheduling
from calculations import metrics

class SchedulerTests(unittest.TestCase):
    def test_basic_fcfs(self):
        ps = [Process('P1', 0, 5, 2, 0), Process('P2', 1, 3, 1, 1), Process('P3', 2, 2, 3, 2)]
        result = fcfs(ps)
        self.assertEqual(result.completion, {'P1': 5, 'P2': 8, 'P3': 10})
        rows, avgs = metrics(ps, result)
        self.assertEqual([r['wt'] for r in rows], [0, 4, 6])
        self.assertAlmostEqual(avgs['tat'], 20 / 3)

    def test_idle_and_ties(self):
        ps = [Process('P1', 3, 4, 2, 0), Process('P2', 3, 2, 1, 1), Process('P3', 3, 2, 1, 2)]
        self.assertEqual([(s.pid, s.start, s.end) for s in sjf(ps).segments],
                         [('IDLE', 0, 3), ('P2', 3, 5), ('P3', 5, 7), ('P1', 7, 11)])
        self.assertEqual([s.pid for s in priority_scheduling(ps).segments], ['IDLE', 'P2', 'P3', 'P1'])

    def test_srtf_preemption(self):
        ps = [Process('P1', 0, 8, 2, 0), Process('P2', 1, 4, 1, 1), Process('P3', 2, 2, 3, 2)]
        result = srtf(ps)
        self.assertEqual([(s.pid, s.start, s.end) for s in result.segments],
                         [('P1', 0, 1), ('P2', 1, 2), ('P3', 2, 4), ('P2', 4, 7), ('P1', 7, 14)])
        self.assertEqual(result.completion, {'P3': 4, 'P2': 7, 'P1': 14})

    def test_equal_remaining_does_not_preempt(self):
        ps = [Process('P1', 0, 4, 2, 0), Process('P2', 2, 2, 1, 1)]
        self.assertEqual([s.pid for s in srtf(ps).segments], ['P1', 'P2'])

    def test_invalid(self):
        with self.assertRaises(ValueError):
            fcfs([Process('P1', 0, 0, 1, 0)])

if __name__ == '__main__':
    unittest.main()
