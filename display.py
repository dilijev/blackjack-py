# TODO implement display logic in a single class here, think about being replaceable
# 1. interactive CLI line-based (the usual game mode basic implementation)
# 2. interactive CLI with ASCII-art display

from control import BlackjackGame
from display_ascii import AsciiGridDisplay


class BlackJackTableAsciiGridDisplayDriver(object):
    #     0         1         2         3         4         5         6         7         8
    #     012345678901234567890123456789012345678901234567890123456789012345678901234567890
    #     1234567     12345 123456789012345678901234   123456789012345678901234   123456   # length reference only
    # 01 '-------   +--------------------------------+--------------------------+ ------'
    #  2 'Player1 : | $_BET [ 1 2 3     ] (5/5) = __ |                          |       '
    #  3 '$_P1$_  : | $_DD_ (Double Down)            |                          |       '
    #  4 '        : |       <spacer>                 |                          |       '
    #  5 '        : | $____ [ 1 2 3 4 5 ] (5/5) = __ |                          |       '
    #  6 '        : |       <empty double down slot> | __ = (5/5) [ 1 2 3 4 5 ] | Dealer'  # centered vertically
    #  7 '-------   |                                |                          |       '
    #  8 'Player2 : | $____ [ 1 2 3 4 5 ] (5/5) = __ |                          |       '
    #  9 '$_P2$_  : |                                |                          |       '
    # 10 '-------   +--------------------------------+--------------------------+ ------'

    # HEIGHT = 1 + 3 * len(hands) + 1

    # dynamic longest player name
    # WIDTH_PLAYER = 2                      # 'Player1'
    # dynamic max money pool value
    PLAYER_CONNECTOR = 2                    # ' :'
    WIDTH_LEFT_BORDER = 3                   # ' | '
    WIDTH_MONEY_SIGN = 1                    # '$'
    # dynamic max bet length
    WIDTH_STATUS_SPACER = 1
    WIDTH_MAX_HAND_DISPLAY = 4 + 5 + 4      # '[ 1 2 3 4 5 ]'
    WIDTH_HAND_STATS = 3 + 1 + 2 + 5        # ' (5/5) = __'
    # sanity check: above two fields (and below two) total 24
    WIDTH_DEALER_HAND_STATS = WIDTH_HAND_STATS
    WIDTH_MAX_DEALER_DISPLAY = WIDTH_MAX_HAND_DISPLAY
    WIDTH_GAP = 3                           # ' | '
    WIDTH_RIGHT_BORDER = WIDTH_LEFT_BORDER  # ' | '
    # dynamic dealer name length

    def __init__(self, game: BlackjackGame):
        self.game = game
        self.grid_display = None

        self.start_player_field = 0
        self.width_player_field = 0
        self.start_bet_field = 0
        self.width_bet_field = 0
        self.start_player_status = 0
        self.width_player_status = 0

        self.start_dealer_status = 0
        self.width_dealer_status = 0
        self.dealer_name_start = 0
        self.dealer_name_length = 0
        self.dealer_row = 0

        self.table_left = 0
        self.table_divider_column = 0
        self.table_width = 0
        
        self.width = 0
        self.height = 0

    def configure(self) -> None:
        # get width in columns
        max_player_name_length = 0
        for player in self.game.players:
            player_name_length = len(player.get_name())
            if player_name_length > max_player_name_length:
                max_player_name_length = player_name_length
        max_player_money_pool_value = 1 + 5

        self.start_player_field = 0
        self.width_player_field = max(max_player_name_length, max_player_money_pool_value)

        self.table_left = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + 1

        self.start_bet_field = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN
        # TODO calculate max bet length from hands' bets
        self.width_bet_field = 4

        self.table_divider_column = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + 2 - 1

        self.table_width = 2 + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + 2

        self.dealer_name_start = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_RIGHT_BORDER

        # TODO Change len('Dealer') to len(dealer.get_name()) -- move get_name() to Person
        self.dealer_name_length = len('Dealer')

        # calculte width
        self.width = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_RIGHT_BORDER + \
            self.dealer_name_length

        # TODO update based on number of hands when splitting is implemented
        # self.height = len(hands) * 3 + 2
        self.height = len(self.game.players) * 3 + 1
        self.dealer_row = self.height // 2 - 1

        self.grid_display = AsciiGridDisplay(self.height, self.width)

    def render_boxes(self) -> None:
        # table
        self.grid_display.draw_rectangle(
            row=0, column=self.table_left,
            height=self.height, width=self.table_width)
        # table divider
        self.grid_display.draw_vertical_line(
            row=0, column=self.table_divider_column,
            height=self.height, end_character='+')

        # TODO remove debug table dimensions extreme
        self.grid_display.set_text(self.height - 1, self.width - 1, '.')

    def render_lines(self) -> None:
        # player area top line spacer
        self.grid_display.draw_horizontal_line(
            row=0, column=0, width=self.width_player_field)
        for x in range(len(self.game.players)):
            # line after every player
            row = (x + 1) * 3
            self.grid_display.draw_horizontal_line(
                row=row, column=0, width=self.width_player_field)

        # dealer area top line spacer
        self.grid_display.draw_horizontal_line(
            row=0, column=self.dealer_name_start,
            width=self.dealer_name_length)
        # dealer area bottom line spacer
        self.grid_display.draw_horizontal_line(
            row=self.height - 1,
            column=self.dealer_name_start,
            width=self.dealer_name_length)

    def render_names(self) -> None:
        for x in range(len(self.game.players)):
            player = self.game.players[x]
            name = player.get_name()
            row = 1 + x * 3
            self.grid_display.set_text(
                row=row, column = self.start_player_field, text=name)
        
        # dealer_name = self.game.dealer.get_name()
        # TODO update logic for dealer name
        dealer_name = 'Dealer'
        self.grid_display.set_text(
            row=self.dealer_row,
            column = self.dealer_name_start,
            text=dealer_name)

    def render(self) -> None:
        self.configure()
        self.render_boxes()
        self.render_lines()
        self.render_names()


    def display(self) -> None:
        self.grid_display.display()

    # TODO implement updates instead of full redraws,
    # which is also helpful for printing "what just happened"
    # particularly for a naive "UI" (CLI for testing)
    # that doesn't ever draw the board.
    def update_hand(self, index: int) -> None:
        pass


if __name__ == '__main__':
    game = BlackjackGame()
    game.default_settings()
    display_driver = BlackJackTableAsciiGridDisplayDriver(game)
    display_driver.render()
    display_driver.display()

