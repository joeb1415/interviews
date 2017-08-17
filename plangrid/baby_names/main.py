from baby_api import BabyAPI
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/frequency')
def frequency():
    args = request.args
    name = args['name']
    gender = args['gender']

    data = baby_api.get_freq(name, gender)

    r = Response(data)

    return r


if __name__ == '__main__':
    baby_api = BabyAPI()
    baby_api.load_data()
    app.run(debug=True)
