from flask import Flask, request
from event_publisher import Publisher
import json

app = Flask(__name__)
dispatcher = Publisher(app.logger) #TODO: There's probably a better way to encapsulate logging

@app.route("/")
def index():
    return "This is the event generator.  To send an event to the stats processor POST to the /events endpoint."

@app.route("/events", methods=['POST'])
def post_event():
    message = request.get_json()
    app.logger.debug("request had the following data: {0}".format(message))
    dispatcher.push(message)
    return json.dumps({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
