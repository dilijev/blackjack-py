import random

class PlayingCard:
    def __init__(self, suit: str, value: str) -> None:
        self.suit = suit
        self.value = value

    def get_suit(self) -> str:
        return self.suit

    def get_value(self) -> str:
        return self.value

    def get_num_value(self) -> int:
        if self.value == "A":
            return 1
        elif self.value == "J":
            return 10
        elif self.value == "Q":
            return 10
        elif self.value == "K":
            return 10
        else:
            return self.value


class Deck:
    def __init__(self) -> None:
        self.cards = []

    def draw_card(self) -> PlayingCard:
        selected_card = random.choice(self.cards)
        self.cards.remove(selected_card)
        return selected_card

    def init_deck(self) -> None:
        suits = ["hearts", "diamonds", "spades", "clubs"]
        values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10, "J", "Q", "K"]
        for x in range(5):
            for suit in suits:
                for value in values:
                    self.cards.append(PlayingCard(suit, value))


class Hand:
    def __init__(self) -> None:
        """set self.cards as an empty list"""
        self.cards = []

    def get_cards(self, deck: Deck) -> None:
        """draw two initial cards from the deck and append them to self.cards"""
        self.add_card(deck)
        self.add_card(deck)

    def get_total_value(self) -> int:
        """get total value of cards in the hand"""
        sum = 0
        aces = 0
        card: PlayingCard  # type annotation
        for card in self.cards:
            value = card.get_num_value()
            sum += value
            if value == 1:
                aces += 1
        if aces > 0 and sum < 21:
            sum += 10
        return sum

    def get_first_card(self) -> PlayingCard:
        return self.cards[0]

    def get_num_cards(self) -> int:
        return len(self.cards)

    def render_hand(self) -> str:
        hand = '[ '
        for card in self.cards:
            hand += str(card.get_value()) + ' '
        for x in range(5 - len(self.cards)):
            hand += '  '
        hand += ']'
        return hand

    def add_card(self, deck) -> None:
        """draw one card from the deck and append them to self.cards"""
        self.cards.append(deck.draw_card())
