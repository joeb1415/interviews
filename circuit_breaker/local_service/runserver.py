import json

from flask import Flask, request, Response

from api import API

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/remote_post', methods=['POST'])
def remote_post():
    args = request.args
    wait = int(args['wait'])
    status_code = int(args['status_code'])

    data = api.remote_post(wait, status_code)
    response = json.dumps(
        {
            'data': data
        }
    )
    r = Response(response=response, status=status_code)

    return r


if __name__ == '__main__':
    api = API()
    app.run(debug=True, host='localhost', port=5000)
