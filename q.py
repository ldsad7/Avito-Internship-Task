#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
from dateutil.parser import parse
from jsonschema import validate

first_schema = {
    'type': 'object',
    'properties': {
        'logs': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'time': {
                        'type': 'string'
                    },
                    'test': {
                        'type': 'string'
                    },
                    'output': {
                        'type': 'string',
                        'enum': ['success', 'fail']
                    }
                },
                'required': [
                    'time',
                    'test',
                    'output'
                ]
            }
        }
    },
    'required': [
        'logs'
    ]
}

second_schema = {
    'type': 'object',
    'properties': {
        'suites': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'name': {
                        'type': 'string',
                    },
                    'tests': {
                        'type': 'number',
                    },
                    'cases': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'name': {
                                    'type': 'string'
                                },
                                'errors': {
                                    'type': 'number'
                                },
                                'time': {
                                    'type': 'string'
                                }
                            },
                            'required': [
                                'name',
                                'errors',
                                'time'
                            ]
                        }
                    }
                },
                'required': [
                    'name',
                    'tests',
                    'cases'
                ]
            }
        }
    },
    'required': [
        'suites'
    ]
}

third_schema = {
    'type': 'object',
    'properties': {
        'captures': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'expected':  {
                        'type': 'string'
                    },
                    'actual': {
                        'type': 'string'
                    },
                    'time': {
                        'type': 'string'
                    }
                },
                'required': [
                    'expected',
                    'actual',
                    'time'
                ]
            }
        }
    },
    'required': [
        'captures'
    ]
}

result_schema = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'name': {
                'type': 'string'
            },
            'status': {
                'type': 'string'
            },
            'expected_value': {
                'type': 'string'
            },
            'actual_value': {
                'type': 'string'
            }
        },
        'required': [
            'name',
            'status',
            'expected_value',
            'actual_value'
        ]
    }
}

def read_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def merge_files(filepath1, filepath2, filepath3):
    """
    >>> merge_files('file1.json', 'file2.json', 'file3.json')
    [{'name': 'Test output A', 'status': 'fail', 'expected_value': 'A', 'actual_value': 'B'}, {'name': 'Test output B', 'status': 'success', 'expected_value': 'B', 'actual_value': 'B'}]
    """
    first_json = read_json(filepath1)
    validate(first_json, first_schema)

    second_json = read_json(filepath2)
    validate(second_json, second_schema)

    third_json = read_json(filepath3)
    validate(third_json, third_schema)

    tests = {}
    for dct in first_json['logs']:
        timestamp = float(dct['time'])
        tests[timestamp] = {}
        tests[timestamp]['name'] = dct['test']
        tests[timestamp]['status'] = dct['output']
        tests[timestamp]['expected_value'] = dct['test'].split()[-1]

    for dct in second_json['suites']:
        for inner_dct in dct['cases']:
            timestamp = parse(inner_dct['time']).timestamp()
            tests[timestamp] = {}
            tests[timestamp]['name'] = inner_dct['name']
            if inner_dct['errors']:
                tests[timestamp]['status'] = 'fail'
            else:
                tests[timestamp]['status'] = 'success'
            tests[timestamp]['expected_value'] = inner_dct['name'].split()[-1]

    for dct in third_json['captures']:
        timestamp = parse(dct['time']).timestamp()
        if timestamp not in tests:
            tests[timestamp] = {}
        tests[timestamp]['expected_value'] = dct['expected']
        tests[timestamp]['actual_value'] = dct['actual']

    objects = list(tests.values())
    validate(objects, result_schema)
    with open('result.json', 'w', encoding='utf-8') as f:
        json.dump(objects, f)
    return objects

if __name__ == "__main__":
    import doctest
    doctest.testmod()