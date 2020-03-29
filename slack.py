from flask import Flask, request, make_response
import re
app = Flask(__name__)

youtubeRE = r'youtube\.com'

def handleMessage(payload):
    if payload['event']['type'] == "mention":
        text = payload['event']['text']
        if re.match(youtubeRE, text):
            print('TODO: Scrape this text\n')
            print(text)


@app.route('/', methods=['get', 'post'])
def receiveMessage():
    payload = request.json
    handleMessage(payload)
    return make_response('Hello, world!', 200)

app.run(host='127.0.0.1', port="1234")
