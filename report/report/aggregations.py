def uptime_percentage(pid):
    return [
    {
        '$match': {
            'pid': pid,
            'type': 'response'
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
