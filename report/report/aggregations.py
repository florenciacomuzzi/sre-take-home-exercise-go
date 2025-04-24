def get_uptime_percentage(pid, start=None, end=None):
    pipeline = [
        {
            '$match': {
                'pid': pid,
                'type': 'response',
            }
        }, {
            '$group': {
                '_id': None,
                'totalRecords': {
                    '$sum': 1
                },
                'success': {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$code', 200
                                ]
                            }, 1, 0
                        ]
                    }
                },
                'fail': {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$code', 500
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'totalRecords': 1,
                'success': 1,
                'fail': 1,
                'uptime': {
                    '$cond': [
                        {
                            '$eq': [
                                '$totalRecords', 0
                            ]
                        }, 0, {
                            '$divide': [
                                '$success', '$totalRecords'
                            ]
                        }
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'totalRecords': 1,
                'success': 1,
                'fail': 1,
                'uptime': 1,
                'uptimePercentage': {
                    '$multiply': [
                        '$uptime', 100
                    ]
                }
            }
        }
    ]
    # TODO validate type of start and end
    if not start and not end:
        return pipeline
    stage = pipeline[0]
    match = stage['$match']
    if start:
        match['timestamp']['$gte'] = start
    if end:
        match['timestamp']['$lt'] = end
    pipeline[0]['$match'] = match
    return pipeline


def get_unique_pids():
    pipeline = [
        {
            '$group': {
                '_id': '$pid'
            }
        },
        {
            '$sort': {
                '_id': 1
            }
        }
    ]
    return pipeline

def get_availability_by_domains():
    pipeline = [
    {
        '$group': {
            '_id': '$domain', 
            'available': {
                '$sum': '$available'
            }, 
            'total': {
                '$sum': '$total'
            }, 
            'start': {
                '$min': '$start'
            }, 
            'end': {
                '$max': '$end'
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'domain': '$_id', 
            'available': 1, 
            'total': 1, 
            'start': 1, 
            'end': 1, 
            'availableFraction': {
                '$divide': [
                    '$available', '$total'
                ]
            }, 
            'durationMs': {
                '$dateDiff': {
                    'startDate': '$start', 
                    'endDate': '$end', 
                    'unit': 'millisecond'
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'domain': '$domain', 
            'available': 1, 
            'total': 1,
            'start': 1,
            'end': 1,
            'availablePercentage': {
                '$multiply': [
                    '$availableFraction', 100
                ]
            }, 
            'durationMs': {
                '$dateDiff': {
                    'startDate': '$start', 
                    'endDate': '$end', 
                    'unit': 'millisecond'
                }
            }
        }
    },
    ]
    return pipeline

def get_availability_by_domain(domain):
        pipeline = [
        {
            '$group': {
                '_id': '$domain',
                'available': {
                    '$sum': '$available'
                },
                'total': {
                    '$sum': '$total'
                },
                'start': {
                    '$min': '$start'
                },
                'end': {
                    '$max': '$end'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'domain': '$_id',
                'available': 1,
                'total': 1,
                'start': 1,
                'end': 1,
                'availableFraction': {
                    '$divide': [
                        '$available', '$total'
                    ]
                },
                'durationMs': {
                    '$dateDiff': {
                        'startDate': '$start',
                        'endDate': '$end',
                        'unit': 'millisecond'
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'domain': '$domain',
                'available': 1,
                'total': 1,
                'start': 1,
                'end': 1,
                'availablePercentage': {
                    '$multiply': [
                        '$availableFraction', 100
                    ]
                },
                'durationMs': {
                    '$dateDiff': {
                        'startDate': '$start',
                        'endDate': '$end',
                        'unit': 'millisecond'
                    }
                }
            }
        },
        {
            '$match': {
                'domain': domain
            }
        }
    ]
        return pipeline
