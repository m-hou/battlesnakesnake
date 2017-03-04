from flask import Flask, request, jsonify
import json
import random
from snake import best, update_board, GameState
import datetime

app = Flask(__name__)
N = 15
moves = ["up", "down", "left", "right"]



@app.route("/start", methods=["POST"])
def start():
    # NOTE: 'request' contains the data which was sent to us about the Snake game
    # after every POST to our server 
    print(request.__dict__) 
    
    snake = {
        "color": "#123456",
        "name": "snak3",
        "taunt": "X D X D X D",
        "head_type": "pixel",
        "secondary_color": "#00000F"
    }

    return jsonify(snake)

@app.route("/move", methods=["POST"])
def move():
    t0 = datetime.datetime.now()
    data = json.loads(request.data)
    
    state = get_params(data)
    board = update_board(state)

    move = best(state, board)
    response = {
        "move": move
    }
    t1 = datetime.datetime.now()
    print("Time to run: ", (t1 - t0).total_seconds())
    print(move)
    
    return jsonify(response)

def get_params(data):
    print(data.keys())
    snakes = data['snakes']
    food = data['food']
    width = data['width']
    height = data['height']
    my_id = data['you']

    mysnake = [snake for snake in snakes if snake['id'] == my_id][0]
    head = mysnake['coords'][0]

    return GameState(mysnake, snakes, food, width, height, head)




if __name__ == "__main__":
    app.run(port=8080, debug=True)


