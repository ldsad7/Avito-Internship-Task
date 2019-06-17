import unittest
import json

from q import merge_files

class TestMergeFiles(unittest.TestCase):
    def test_first_case(self):
        with open('newfile1.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json.loads("""
                    {
                        "logs": [
                            {
                                "time": "836954760",
                                "test": "Test output C",
                                "output": "success"
                            },
                            {
                                "time": "928537438",
                                "test": "Test output D",
                                "output": "fail"
                            }
                        ]
                    }
                    """)))
        with open('newfile2.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json.loads("""
                    {
                        "suites": [
                            {
                                "name": "suite1",
                                "tests": 1,
                                "cases": [
                                    {
                                        "name": "Test output A",
                                        "errors": 1,
                                        "time": "Monday, 11-Sep-12 05:12:30 UTC"
                                    }
                                ]
                            },
                            {
                                "name": "suite2",
                                "tests": 1,
                                "cases": [
                                    {
                                        "name": "Test output B",
                                        "errors": 0,
                                        "time": "Wednesday, 28-Feb-18 18:52:19 UTC"
                                    }
                                ]
                            }
                        ]
                    }
                    """)))
        with open('newfile3.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json.loads("""
                    {
                        "captures": [
                            {
                                "expected": "C",
                                "actual": "C",
                                "time": "1996-07-09T23:26:00+00:00"
                            },
                            {
                                "expected": "D",
                                "actual": "B",
                                "time": "1999-06-04T23:03:58+00:00"
                            },
                            {
                                "expected": "A",
                                "actual": "D",
                                "time": "2012-09-11T05:12:30+00:00"
                            },
                            {
                                "expected": "B",
                                "actual": "B",
                                "time": "2018-02-28T18:52:19+00:00"
                            }
                        ]
                    }
                    """)))
        self.assertEqual(merge_files('newfile1.json', 'newfile2.json', 'newfile3.json'), [{'name': 'Test output C', 'status': 'success', 'expected_value': 'C', 'actual_value': 'C'}, {'name': 'Test output D', 'status': 'fail', 'expected_value': 'D', 'actual_value': 'B'}, {'name': 'Test output A', 'status': 'fail', 'expected_value': 'A', 'actual_value': 'D'}, {'name': 'Test output B', 'status': 'success', 'expected_value': 'B', 'actual_value': 'B'}])

if __name__ == "__main__":
    unittest.main()