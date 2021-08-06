# import os

from cards import *
from people import Dealer, Player
from display import BlackJackTableAsciiGridDisplayDriver
from table import BlackJackTable

class BlackJackController:
    def __init__(self) -> None:
        self.table = BlackJackTable()
        self.display_driver = BlackJackTableAsciiGridDisplayDriver(self.table)

    def display(self, message: str = '', pause: bool = True) -> None:
        # os.system('cls')
        print()
        print(message)
        self.display_driver.display()
        if pause:
            self.any_key()

    def any_key(self) -> None:
        input('Press any key to continue...')

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

    #
    # TODO move renderings into display drivers
    #

    def render_dealer_blind(self):
        dealer_visible_score = self.table.dealer.report_visible_score()
        return f'Dealer is showing {dealer_visible_score} and a face down card'

    def render_dealer_showing(self):
        dealer_score = self.table.dealer.report_score()
        dealer_hand = self.table.dealer.render_hand()
        dealer_num_cards = self.table.dealer.get_num_cards()
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
                self.display(f'{player_name} busted!')
                player.bust()
                playing = False
                break
            elif player_score == 21:
                if player_num_cards == 2:
                    self.display(f'{player_name} has blackjack and wins!')
                    player.win()  # pays out right away
                    # TODO display payout update when bets are implemented
                else:
                    self.display(f'{player_name} has 21! Stay!')
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
                self.display(f'{player_name} hits!', pause=False)
            else:
                playing = False
                self.display(f'{player_name} stays!')

    def dealer_turn(self, deck):
        self.display("Dealer's Turn")

        self.table.dealer.unblind_hand()
        self.display("Dealer flips up their face-down card.")

        dealer_playing = True
        while dealer_playing:
            dealer_score = self.table.dealer.report_score()
            print(self.render_dealer_showing())
            if dealer_score >= 17:
                dealer_playing = False
                if dealer_score > 21:
                    self.display("Dealer busts!")
                    self.table.dealer.bust()
                    break

                self.display("Dealer stays.")
                break

            self.table.dealer.hit(deck)
            self.display("Dealer hits!")

    def play_game(self):
        # Prime the loop and start the first game.
        user_response = 'Y'
        while user_response == "Y" or user_response == "y":
            ## initialize deck
            self.table.deck.init_deck()
            ## initialize a player amd dealer and get two cards per player
            player_name = input("What's your name?: ")
            print()

            self.table.players = [Player(self.table.deck, player_name)]
            self.table.dealer = Dealer(self.table.deck)

            self.display(pause=False)

            # """All control should take a place here"""

            # update for multiple active hands (Players)
            for player in self.table.players:
                self.player_turn(player, self.table.deck)

            # Are there any players left? If so, Dealer needs to play.
            dealer_should_play = False
            for player in self.table.players:
                if not player.is_bust():
                    dealer_should_play = True
                    break

            if dealer_should_play:
                self.dealer_turn(self.table.deck)

            # TODO update for multiple players
            player = self.table.players[0]

            print(self.render_dealer_showing())
            print(self.render_player(player))

            dealer_score = self.table.dealer.report_score()
            # TODO update for multiple players
            player_score = player.report_score()

            # who won?
            # TODO update for multiple players
            if self.table.dealer.is_bust() or player_score > dealer_score:
                self.display(f'{player_name} wins!')
            elif player.is_bust() or dealer_score > player_score:
                self.display('Dealer wins (against all players still on the board)!')
            else:
                # scores equal
                self.display('Push!')

            user_response = self.prompt_user('Play again?')
            # go back to top for a new game

        print(f"Thanks for playing! Goodbye, {player_name}!")
