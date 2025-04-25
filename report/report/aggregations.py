def get_availability_by_server():
    pipeline = [
        {
            '$group': {
                '_id': {
                    'url': '$url',
                    'domain': '$domain'
                },
                'start': {
                    '$min': '$server_start_ts'
                },
                'end': {
                    '$max': '$timestamp'
                },
                'total': {
                    '$sum': 1
                },
                'success': {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$status', 'success'
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$_id.domain',
                'start': {
                    '$min': '$start'
                },
                'end': {
                    '$min': '$end'
                },
                'total': {
                    '$sum': '$total'
                },
                'success': {
                    '$sum': '$success'
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'domain': '$_id',
                'success': 1,
                'total': 1,
                'start': 1,
                'end': 1,
                'availabilityRatio': {
                    '$divide': [
                        '$success', '$total'
                    ]
                }
            }
        }, {
            '$addFields': {
                'availabilityPercentage': {
                    '$multiply': [
                        '$availabilityRatio', 100
                    ]
                }
            }
        }, {
            '$project': {
                'availabilityRatio': 0
            }
        }
    ]
    return pipeline


def get_availability_by_domain():
    """Gets all-time availability  for all domains."""
    pipeline = [
        {
            '$group': {
                '_id': '$domain',
                'success': {
                    '$sum': '$success'
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
                'success': 1,
                'total': 1,
                'start': 1,
                'end': 1,
                'availabilityRatio': {
                    '$divide': [
                        '$success', '$total'
                    ]
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'domain': 1,
                'success': 1,
                'total': 1,
                'start': 1,
                'end': 1,
                'availabilityPercentage': {
                    '$multiply': [
                        '$availabilityRatio', 100
                    ]
                }
            }
        }
    ]
    return pipeline


def get_availability_by_domain_since(dt):
    pipeline = [
        {
            '$match': {
                'type': 'response',
                'timestamp': {
                    '$gt': dt
                }
            }
        }, {
            '$group': {
                '_id': '$domain',
                'total': {
                    '$sum': 1
                },
                'success': {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$status', 'success'
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0,
                'domain': '$_id',
                'success': '$success',
                'total': '$total',
                'availabilityRatio': {
                    '$divide': [
                        '$success', '$total'
                    ]
                }
            }
        }, {
            '$project': {
                'domain': 1,
                'success': 1,
                'total': 1,
                'availabilityPercentage': {
                    '$multiply': [
                        '$availabilityRatio', 100
                    ]
                }
            }
        }
    ]
    return pipeline
