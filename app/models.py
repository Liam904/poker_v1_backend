from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Alias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cards = db.relationship("Card", backref="alias")
    games = db.relationship("Game", backref="alias")


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    suit = db.Column(db.String(10), nullable=False)
    alias_id = db.Column(db.Integer, db.ForeignKey("alias.id"), nullable=True)
    computer_id = db.Column(db.Integer, db.ForeignKey("computer.id"), nullable=True)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    deck = db.Column(db.PickleType, nullable=False)
    table_card = db.Column(db.PickleType, nullable=False)
    game_state = db.Column(db.PickleType, nullable=False)
    winner = db.Column(db.String(100), nullable=False, default="Undecided")
    alias_id = db.Column(db.Integer, db.ForeignKey("alias.id"), nullable=True)
    computer_id = db.Column(db.Integer, db.ForeignKey("computer.id"), nullable=True)
    computer_hand = db.Column(db.PickleType, nullable=True)
    player_hand = db.Column(db.PickleType, nullable=True)

    ##add playerhand and computerhand


class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship("Card", backref="computer")
    games = db.relationship("Game", backref="computer")
