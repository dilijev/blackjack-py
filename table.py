from cards import *
from people import *

class BlackJackTable:
    def __init__(self):
        """initialize deck and player"""
        self.deck = Deck()
        self.players: list[Player] = []
        # self.hands = []  # TODO implement
        self.dealer: Dealer = None

    def default_settings(self) -> None:
        self.deck.init_deck()
        player = Player(self.deck, 'Player1')
        self.players.append(player)
        self.dealer = Dealer(self.deck)
