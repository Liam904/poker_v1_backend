from .game_engine import GameEngine
from flask import Blueprint, jsonify, request
from .models import Game
from flask_jwt_extended import jwt_required, get_jwt_identity

# Create an instance of the GameEngine class
game = GameEngine()

views = Blueprint("views", __name__)


@views.route("/new_game", methods=["POST"])
@jwt_required()
def new_game():
    return jsonify(game.new_game()), 201


@views.route("/player_moves", methods=["POST"])
@jwt_required()
def player_moves():
    body = request.get_json()
    rank = body.get("rank")
    suit = body.get("suit")

    return jsonify(game.player_moves(rank=rank, suit=suit)), 201


@views.route("/game", methods=["GET"])
@jwt_required()
def game_state():
    return jsonify(game.serialize_game_state()), 200


@views.route("/pick", methods=["POST"])
@jwt_required()
def pick_card():
    return jsonify(game.pick_card()), 201
