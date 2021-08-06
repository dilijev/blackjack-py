from cards import *

class Person:
    def __init__(self, deck: Deck) -> None:
        """set hand and get two initial cards from the deck"""
        self.hand = Hand()
        self.hand.add_card(deck)
        self.hand.add_card(deck)

    def hit(self, deck: Deck) -> None:
        """add a card from the deck to hand"""
        self.hand.add_card(deck)

    def get_num_cards(self) -> int:
        return self.hand.get_num_cards()

    def bust(self) -> None:
        print('Bust!')
        self.hand = Hand()

    def win(self) -> None:
        print('Win!')
        self.hand = Hand()

    def is_bust(self) -> bool:
        return self.hand.get_num_cards() == 0

    def render_hand(self) -> str:
        return self.hand.render_player_hand()

    def report_score(self) -> int:
        """report total values of the hand"""
        return self.hand.get_total_value()

    def report_first_card_score(self) -> int:
        value = self.hand.get_first_card().get_num_value()
        if value == 1:
            value += 10
        return value


class Dealer(Person):
    def __init__(self, deck: Deck) -> None:
        """inherit Person Class and set self.name as 'Dealer'"""
        super().__init__(deck)
        self.blind_hand = True

    def report_visible_score(self) -> None:
        return super().report_first_card_score()

    def render_hand(self) -> str:
        return self.hand.render_dealer_hand(self.blind_hand)

    def unblind_hand(self) -> None:
        self.blind_hand = False


class Player(Person):
    def __init__(self, deck: Deck, name: str) -> None:
        """inheirt Person Class and set self.name as what a user typed in"""
        super().__init__(deck)
        self.name = name

    def get_name(self) -> None:
        return self.name

    def render_hand(self) -> str:
        return self.hand.render_player_hand()
