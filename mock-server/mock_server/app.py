from flask import Flask, request, jsonify
from .database import Database
from datetime import datetime

app = Flask(__name__)
db = Database()

@app.route('/', methods=['GET', 'POST'])
def handle_request():
    request_data = {
        'url': request.url,
        'method': request.method,
        'headers': dict(request.headers),
        'timestamp': datetime.utcnow(),
        'data': request.get_json() if request.is_json else request.form.to_dict()
    }

    # Log request to MongoDB
    db.db.requests.insert_one(request_data)

    return jsonify({
        'status': 'success',
        'message': f'Request logged successfully',
        'method': request.method
    })

if __name__ == '__main__':
    app.run(debug=True) 