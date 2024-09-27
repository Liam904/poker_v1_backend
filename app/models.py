from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Alias(db.Model):
    __tablename__ = 'aliases'  # Use a specific table name for PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    alias = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  # Ensure email is unique
    password = db.Column(db.String(100), nullable=False)
    cards = db.relationship("Card", backref="alias", lazy=True)
    games = db.relationship("Game", backref="alias", lazy=True)

class Card(db.Model):
    __tablename__ = 'cards'  # Use a specific table name for PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(10), nullable=False)
    suit = db.Column(db.String(10), nullable=False)
    alias_id = db.Column(db.Integer, db.ForeignKey("aliases.id"), nullable=True)
    computer_id = db.Column(db.Integer, db.ForeignKey("computers.id"), nullable=True)

class Game(db.Model):
    __tablename__ = 'games'  # Use a specific table name for PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    deck = db.Column(db.JSON, nullable=False)  # Use JSON type for structured data
    table_card = db.Column(db.JSON, nullable=False)  # Use JSON type for structured data
    game_state = db.Column(db.JSON, nullable=False)  # Use JSON type for structured data
    winner = db.Column(db.String(100), nullable=False, default="Undecided")
    alias_id = db.Column(db.Integer, db.ForeignKey("aliases.id"), nullable=True)
    computer_id = db.Column(db.Integer, db.ForeignKey("computers.id"), nullable=True)
    computer_hand = db.Column(db.JSON, nullable=True)  # Use JSON type for structured data
    player_hand = db.Column(db.JSON, nullable=True)  # Use JSON type for structured data

class Computer(db.Model):
    __tablename__ = 'computers'  # Use a specific table name for PostgreSQL
    id = db.Column(db.Integer, primary_key=True)
    cards = db.relationship("Card", backref="computer", lazy=True)
    games = db.relationship("Game", backref="computer", lazy=True)
