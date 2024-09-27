import random
from app.models import Card, Game, db, Alias
from flask_jwt_extended import get_jwt_identity


class GameEngine:
    def __init__(self):
        self.deck = []
        self.player_hand = []
        self.computer_hand = []
        self.table_card = []
        self.winner = None

    def create_deck(self):
        cards = Card.query.all()
        joker = ("Joker", "Joker")
        self.deck = [(card.rank, card.suit) for card in cards]
        self.deck.append(joker)
        random.shuffle(self.deck)
        return self.deck

    def deal_cards(self):

        for _ in range(4):
            self.player_hand.append(self.deck.pop())
            self.computer_hand.append(self.deck.pop())

        self.table_card.append(self.deck.pop())
        return {
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.table_card,
        }

    def player_moves(self, rank, suit):
        play = (rank, suit)
        if play[0] == "Joker":
            self.player_hand.remove(play)
            for _ in range(5):
                cards = self.deck.pop()
                self.computer_hand.append(cards)

        if play in self.player_hand and (
            play[0] == self.table_card[-1][0] or play[1] == self.table_card[-1][1]
        ):
            if play[0] in ["J", "K", "Q", "A"]:
                self.player_hand.remove(play)
                self.table_card.append(play)
                return

            self.table_card.append(play)
            self.player_hand.remove(play)

            if play[0] in ["2", "3"]:
                for _ in range(2):
                    if self.deck:
                        card = self.deck.pop()
                        self.computer_hand.append(card)
            winner_logic = self.winner_logic()
            if winner_logic:
                print(self.winner)

                return winner_logic

            return {
                "player_hand": self.player_hand,
                "valid": True,
                "computer_moves": self.computer_moves(),
                "computer_hand": self.computer_hand,
                "table_card": self.table_card,
            }

        else:

            if self.deck:
                self.player_hand.append(self.deck.pop())
                self.computer_moves()
            return {
                "valid": False,
                "player_hand": self.player_hand,
                "computer_hand": self.computer_hand,
                "table_card": self.table_card,
                "computer_moves": self.computer_moves(),
                "message": "invalid move, penalty awarded",
            }

    def computer_moves(self):
        playable_cards = []

        for card in self.computer_hand:
            if card[0] == self.table_card[-1][0] or card[1] == self.table_card[-1][1]:
                playable_cards.append(card)
        if playable_cards:
            play = random.choice(playable_cards)

            self.table_card.append(play)
            self.computer_hand.remove(play)

            if play[0] in ["2", "3"]:
                for _ in range(2):
                    if self.deck:
                        cards = self.deck.pop()
                        self.player_hand.append(cards)
            if play[0] in ["J", "K", "Q", "A"]:
                return self.computer_moves()

            if play[0] == ["Joker"]:
                for _ in range(5):
                    if self.deck:
                        cards = self.deck.pop()
                        self.player_hand.append(cards)

        else:
            if self.deck:
                cards = self.deck.pop()
                self.computer_hand.append(cards)

        winner_logic = self.winner_logic()
        if winner_logic:
            print(self.winner)
            return winner_logic

    def new_game(self):
        self.deck = []
        self.player_hand = []
        self.computer_hand = []
        self.table_card = []

        if not self.deck:
            self.create_deck()

        self.deal_cards()

        new_game = Game(
            deck=self.deck,
            table_card=self.table_card,
            winner=self.winner,
            alias_id=get_jwt_identity(),
            computer_id=1,
            game_state=self.serialize_game_state(),
            computer_hand=self.computer_hand,
            player_hand=self.computer_hand,
        )

        db.session.add(new_game)
        db.session.commit()

        return {"message": "successfully created a new game"}

    def pick_card(self):

        picked_card = []

        if self.deck:
            card = self.deck.pop()
            self.player_hand.append(card)
            picked_card.append(card)

        return {
            "picked_card": picked_card,
            "computer_moves": self.computer_moves(),
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.table_card,
        }

    def serialize_game_state(self):

        return {
            "deck": self.deck,
            "player_hand": self.player_hand,
            "computer_hand": self.computer_hand,
            "table_card": self.table_card,
            "winner": self.winner,
        }

    def winner_logic(self):
        if not self.player_hand:
            self.winner = "Player"
            db.session.commit()
            return {"winner": self.winner}

        if not self.computer_hand:
            self.winner = "Computer"
            db.session.commit()
            return {"winner": self.winner}

        if len(self.player_hand) > 7:
            self.winner = "Computer"
            db.session.commit()
            return {"winner": self.winner}

        if len(self.computer_hand) > 7:
            self.winner = "Player"
            db.session.commit()
            return {"winner": self.winner}

        return
