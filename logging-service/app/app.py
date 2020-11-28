import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'logging_db',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class Logs(db.Document):
    service = db.StringField()
    content = db.StringField()
    timestamp = db.StringField()
    action = db.StringField()
    def to_json(self):
        return {"service": self.service,
                "timestamp": self.timestamp,
                "action": self.action,
                "content": self.content}

@app.route('/', methods=['GET'])
def query_records():
    service = request.args.get('service')
    log = Logs.objects(service=service).all()
    if not log:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(log.to_json())

@app.route('/api/create_log', methods=['POST'])
def create_log():

    #record = json.loads(request.form)
    record = request.form

    log = Logs(service=record['service'],timestamp=record['timestamp'],action=record['action'],content=record['content'])
    log.save()
    return jsonify(log.to_json())



if __name__ == "__main__":
    app.run(debug=True)