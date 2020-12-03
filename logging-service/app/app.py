import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import pika

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'logging_db',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

#set up receiver end of rabbitmq
credentials = pika.PlainCredentials(username='guest', password='guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',port=5672,credentials=credentials))

channel = connection.channel()

channel.queue_declare(queue='hello')



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

#don't need this any more
@app.route('/api/create_log', methods=['POST'])
def create_log(record):

    #record = json.loads(request.form)
    #record = request.form
    print('record is ', record)
    log = Logs(service=record['service'],timestamp=record['timestamp'],action=record['action'],content=record['content'])
    log.save()
    return jsonify(log.to_json())

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    record = json.loads(body)
    log = Logs(service=record['service'],timestamp=record['timestamp'],action=record['action'],content=record['content'])
    log.save()

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()



if __name__ == "__main__":
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)




