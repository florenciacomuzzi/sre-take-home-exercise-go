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
