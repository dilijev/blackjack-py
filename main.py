"""You should not share this solution with anyone.
   Please remember that you signed an Academic Honesty Agreement."""

import random


class PlayingCard:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def get_num_value(self):
        if self.value == "ace":
            return 1
        elif self.value == "jack":
            return 10
        elif self.value == "queen":
            return 10
        elif self.value == "king":
            return 10
        else:
            return self.value


class Deck:
    def __init__(self):
        self.cards = []

    def draw_card(self):
        selected_card = random.choice(self.cards)
        self.cards.remove(selected_card)
        return selected_card

    def init_deck(self):
        suits = ["hearts", "diamonds", "spades", "clubs"]
        values = ["ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "jack", "queen", "king"]
        for suit in suits:
            for value in values:
                self.cards.append(PlayingCard(suit, value))


class Hand:
    def __init__(self):
        """set self.cards as an empty list"""
        self.cards = []

    def get_cards(self, deck):
        """draw two initial cards from the deck and append them to self.cards"""
        self.add_card(deck)
        self.add_card(deck)

    def get_total_value(self):
        """get total value of cards in the hand"""
        sum = 0
        aces = 0
        for card in self.cards:
            value = card.get_num_value()
            sum += value
            if value == 1:
                aces += 1
        if aces > 0 and sum < 21:
            sum += 10
        return sum

    def get_first_card(self):
        return self.cards[0]

    def get_num_cards(self):
        return len(self.cards)

    def render_hand(self):
        hand = '[ '
        for card in self.cards:
            hand += str(card.get_value()) + ' '
        hand += ']'
        return hand

    def add_card(self, deck):
        """draw one card from the deck and append them to self.cards"""
        self.cards.append(deck.draw_card())


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


class BlackjackGame:
    def __init__(self):
        """initialize deck and player"""
        self.deck = Deck()
        self.player = None
        self.dealer = None

    def prompt_user(self, prompt, answers = None):
        if answers == None:
            answers = ['y', 'n']
        answers_string = '/'.join(answers)
        good = False
        while not good:
            user_response = str(input(f"{prompt} [{answers_string}] ")).strip().lower()
            if user_response in answers:
                return user_response
            else:
                print('Invalid selection')
        return ''

    def render_dealer_blind(self):
        dealer_visible_score = self.dealer.report_visible_score()
        return f'Dealer is showing {dealer_visible_score} and a face down card'

    def render_dealer_showing(self):
        dealer_score = self.dealer.report_score()
        dealer_hand = self.dealer.render_hand()
        dealer_num_cards = self.dealer.get_num_cards()
        return f'Dealer has {dealer_score} : {dealer_hand} ({dealer_num_cards})'

    def render_player(self, player):
        player_name = player.get_name()
        player_score = player.report_score()
        player_hand = player.render_hand()
        player_num_cards = player.get_num_cards()
        return f'{player_name} has {player_score} : {player_hand} ({player_num_cards})'

    def player_turn(self, player, deck):
        player_name = player.get_name()
        playing = True
        while playing:
            print(self.render_dealer_blind())
            print(self.render_player(player))
            player_score = player.report_score()
            player_num_cards = player.get_num_cards()
            if player_score > 21:
                print(f'{player_name} busted!')
                player.bust()
                playing = False
                break
            elif player_score == 21:
                if player_num_cards == 2:
                    print(f'{player_name} has blackjack and wins!')
                    player.win()  # pays out right away
                else:
                    print(f'{player_name} has 21! Stay!')
                    # doesn't pay yet because might push if the dealer has 21
                playing = False
                break
            elif player_num_cards == 5:
                print(f'{player_name} has a 5-card Charlie and wins!')
                player.win()  # 5 cards without busting is an automatic win
                playing = False
                break

            # self.prompt_user('Do you want another card? Hit (y), stay (n), double down (d), or split (s)?', ['y', 'n', 'd', 's'])
            user_response = self.prompt_user('Do you want another card? Hit (y), stay (n)')
            if user_response == 'y':
                player.hit(deck)
            else:
                playing = False

    def dealer_turn(self, deck):
        dealer_playing = True
        while dealer_playing:
            dealer_score = self.dealer.report_score()
            print(self.render_dealer_showing())
            if dealer_score >= 17:
                if dealer_score > 21:
                    self.dealer.bust()
                dealer_playing = False
                break
            self.dealer.hit(deck)

    def play_game(self):
        # Prime the loop and start the first game.
        user_response = 'Y'
        while user_response == "Y" or user_response == "y":
            ## initialize deck
            self.deck.init_deck()
            ## initialize a player amd dealer and get two cards per player
            player_name = input("What's your name?: ")
            print()

            self.player = Player(self.deck, player_name)
            self.dealer = Dealer(self.deck)

            # """All control should take a place here"""

            # update for multiple active hands (Players)
            for player in [self.player]:
                self.player_turn(player, self.deck)
                print()

            # update to "are there any players left?"
            if not self.player.is_bust():
                self.dealer_turn(self.deck)
            print()

            print(self.render_dealer_showing())
            print(self.render_player(self.player))

            dealer_score = self.dealer.report_score()
            player_score = self.player.report_score()

            # who won?
            print()

            if self.dealer.is_bust() or player_score > dealer_score:
                print(f'{player_name} wins!')
            elif self.player.is_bust() or dealer_score > player_score:
                print('Dealer wins (against all players still on the board)!')
            else:
                # scores equal
                print('Push!')

            user_response = self.prompt_user('Play again?')
            # go back to top for a new game

        print(f"Thanks for playing! Goodbye, {player_name}!")


game = BlackjackGame()
game.play_game()
