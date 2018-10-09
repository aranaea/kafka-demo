from flask import Flask, request
from event_reader import Reader, ConnectionException
import logging
import json


app = Flask(__name__)
reader = Reader()

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    logger.addHandler(logging.StreamHandler())

@app.route("/")
def index():
    return "This is the Event reader.  To read an event from the stream issue a GET on the /events endpoint."

@app.route("/events", methods=['GET'])
def read_event():
    message = None
    try:
        message = reader.next()
    except ConnectionException:
        return json.dumps({'status': 'connection_error', 'message': 'Unable to read from the message stream.'}), 500

    app.logger.debug("Read this data from the stream: {0}".format(message))
    if message:
        return json.dumps(message), 200
    return "", 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
