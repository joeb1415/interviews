from connect_four import ConnectFour
from flask import Flask, request, Response, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


# TODO: This should be a post
@app.route('/insert_piece')
def insert_piece():
    args = request.args
    player_id = int(args['player_id'])
    column = int(args['column'])

    winning_player_id, squares = connect_four.insert_piece(player_id, column)

    # annoyingly, we can't to_dict() with int column headers, need to convert to strings first
    board = connect_four.board.rename(index=str, columns=str)

    r = jsonify(
        {
            'winner': winning_player_id,
            'squares': squares,
            'board': board.values.tolist(),
        }
    )

    return r


@app.route('/return_board')
def return_board():
    data = connect_four.return_board()
    r = Response(data)

    return r


@app.route('/clear_board')
def clear_board():
    connect_four.clear_board()

    data = connect_four.return_board()
    r = Response(data)

    return r


if __name__ == '__main__':
    connect_four = ConnectFour()
    app.run(debug=True)
