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
    WIDTH_MAX_HAND_DISPLAY = 13             # '[ 1 2 3 4 5 ]'
    WIDTH_HAND_STATS = 11                   # ' (5/5) = __'
    # sanity check: above two fields (and below two) total 24
    WIDTH_DEALER_HAND_STATS = WIDTH_HAND_STATS
    WIDTH_MAX_DEALER_DISPLAY = WIDTH_MAX_HAND_DISPLAY
    WIDTH_GAP = 3                           # ' | '
    WIDTH_RIGHT_BORDER = WIDTH_LEFT_BORDER  # ' | '
    # dynamic dealer name length

    HEIGHT_PLAYER = 3

    def __init__(self, game: BlackjackGame) -> None:
        self.game = game
        self.grid_display = None

        self.needs_render = True

        self.start_player_field = 0
        self.width_player_field = 0
        self.start_player_connector = 0
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

        self.start_player_connector = self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR

        self.table_left = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + 1

        self.start_bet_field = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER
        # TODO calculate max bet length from hands' bets
        self.width_bet_field = 4

        self.start_player_status = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER

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
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + 2

        self.start_dealer_status = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
                0

        self.dealer_name_start = \
            self.width_player_field + \
            BlackJackTableAsciiGridDisplayDriver.PLAYER_CONNECTOR + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_LEFT_BORDER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MONEY_SIGN + \
            self.width_bet_field + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_STATUS_SPACER + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_HAND_DISPLAY + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + \
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
            BlackJackTableAsciiGridDisplayDriver.WIDTH_GAP + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_DEALER_HAND_STATS + \
            BlackJackTableAsciiGridDisplayDriver.WIDTH_MAX_DEALER_DISPLAY + \
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
            row = (x + 1) * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
            self.grid_display.draw_horizontal_line(
                row=row, column=0, width=self.width_player_field)
            # draw player connector (graphically connect two hands belonging to one player)
            self.grid_display.draw_vertical_line(
                row=(x * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER) + 1,
                column=self.start_player_connector - 1,
                height=2,  # TODO change to calculation involving hands
                character=':'
            )

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
            row = 1 + x * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
            self.grid_display.set_text(
                row=row, column = self.start_player_field, text=name)
        
        # dealer_name = self.game.dealer.get_name()
        # TODO update logic for dealer name
        dealer_name = 'Dealer'
        self.grid_display.set_text(
            row=self.dealer_row,
            column = self.dealer_name_start,
            text=dealer_name)

    def render_player_hands(self) -> None:
        index = 0
        for player in self.game.players:
            for hand in [player.hand]:
                status = hand.render_player_hand()
                row = 1 + index * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
                self.grid_display.set_text(
                    row=row, column=self.start_player_status,
                    text=status)

    def render_dealer_hand(self) -> None:
        hand = self.game.dealer.hand
        status = hand.render_player_hand()
        row = self.dealer_row
        self.grid_display.set_text(
            row=row, column=self.start_dealer_status,
            text=status)

    def render_pools(self) -> None:
        for x in range(len(self.game.players)):
            # player = self.game.players[x]
            # TODO get money value from player
            money = 0
            money_string = f'${money:4d}'
            row = 2 + x * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
            self.grid_display.set_text(
                row=row, column=self.start_player_field,
                text=money_string)

    def render_bets(self) -> None:
        for x in range(len(self.game.players)):
            # TODO get bet value from player's hands
            money = 0
            money_string = f'${money:4d}'
            row = 1 + x * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
            self.grid_display.set_text(
                row=row, column=self.start_bet_field,
                text=money_string)

    def render_double_down(self) -> None:
        for x in range(len(self.game.players)):
            # TODO get double-down bet value from player's hands
            # TODO change to no display if there's no double-down
            money = 0
            money_string = f'${money:4d}'
            row = 2 + x * BlackJackTableAsciiGridDisplayDriver.HEIGHT_PLAYER
            self.grid_display.set_text(
                row=row, column=self.start_bet_field,
                text=money_string)

    def render(self) -> None:
        self.configure()
        self.render_boxes()
        self.render_lines()
        self.render_names()
        self.render_player_hands()
        self.render_dealer_hand()
        self.render_pools()
        self.render_bets()
        self.render_double_down()

    def display(self) -> None:
        # TODO shouldn't always be necessary but for now we always need it
        if self.needs_render:
            self.render()
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

