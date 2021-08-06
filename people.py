from cards import *

class Person:
    def __init__(self, deck):
        """set hand and get two initial cards from the deck"""
        self.hand = Hand()
        self.hand.add_card(deck)
        self.hand.add_card(deck)

    def hit(self, deck):
        """add a card from the deck to hand"""
        self.hand.add_card(deck)

    def get_num_cards(self):
        return self.hand.get_num_cards()

    def bust(self):
        print('Bust!')
        self.hand = Hand()

    def win(self):
        print('Win!')
        self.hand = Hand()

    def is_bust(self):
        return self.hand.get_num_cards() == 0

    def render_hand(self):
        return self.hand.render_hand()

    def report_score(self):
        """report total values of the hand"""
        return self.hand.get_total_value()

    def report_first_card_score(self):
        value = self.hand.get_first_card().get_num_value()
        if value == 1:
            value += 10
        return value


class Dealer(Person):
    def __init__(self, deck):
        """inherit Person Class and set self.name as 'Dealer'"""
        super().__init__(deck)

    def report_visible_score(self):
        return super().report_first_card_score()


class Player(Person):
    def __init__(self, deck, name):
        """inheirt Person Class and set self.name as what a user typed in"""
        super().__init__(deck)
        self.name = name

    def get_name(self):
        return self.name
