class AsciiGridDisplay(object):
    def __init__(self, rows: int, columns: int) -> None:
        super().__init__()
        self.grid = None
        self.clear(rows, columns)

    def clear(self, rows: int, columns: int) -> None:
        self.grid = []
        # TODO remove debugging edges
        # self.grid.append('v' * (columns + 2))
        for x in range(rows):
            # TODO remove debugging edges
            # self.grid.append('>' + ' ' * columns + '<')
            # s = str(x % 10)
            # s = ''
            # for y in range(columns):
                # placeholder = str(y % 10)
                # s += placeholder
                # s += ' '
            # s += str(x % 10)
            # self.grid.append(s)
            self.grid.append(' ' * columns)
        # TODO remove debugging edges
        # self.grid.append('^' * (columns + 2))

    def set_text(self, row: int, column: int, text: str):
        # column += 1  # TODO remove debugging edge adjustments
        # row += 1  # TODO remove debugging edge adjustments
        row_text = self.grid[row]
        row_text_prefix = row_text[:column]
        row_text_suffix = row_text[column + len(text):]
        # row_text = row_text[:column + 1] + text + row_text[column + len(text):]
        row_text = row_text_prefix + text + row_text_suffix
        self.grid[row] = row_text

    def draw_horizontal_line(self, row: int, column: int, width: int, \
            character: str = '-', end_character: str = None) -> None:
        if end_character is None:
            end_character = character
        self.set_text(row, column, end_character)
        end = column + width - 1
        for c in range(column + 1, end):
            self.set_text(row, c, character)
        self.set_text(row, end, end_character)

    def draw_vertical_line(self, row: int, column: int, height: int, \
            character: str = '|', end_character: str = None) -> None:
        if end_character is None:
            end_character = character
        self.set_text(row, column, end_character)
        end = row + height - 1
        for r in range(row + 1, end):
            self.set_text(r, column, character)
        self.set_text(end, column, end_character)

    def draw_rectangle(self, row: int, column: int, height: int, width: int, \
            horizontal_character: str = '-', vertical_character: str = '|',
            corner_character: str = '+') -> None:
        self.draw_horizontal_line(row, column, width, \
            character=horizontal_character, end_character=corner_character)
        self.draw_horizontal_line(row + height - 1, column, width, \
            character=horizontal_character, end_character=corner_character)
        self.draw_vertical_line(row, column, height, \
            character=vertical_character, end_character=corner_character)
        self.draw_vertical_line(row, column + width - 1, height, \
            character=vertical_character, end_character=corner_character)

    def display(self):
        # TODO implement display, just print the thing
        for line in self.grid:
            print(line)


if __name__ == '__main__':
    # Test the behavior of just this class.

    display = AsciiGridDisplay(13, 80)
    display.draw_horizontal_line(0, 0, 10, end_character='+')
    display.draw_horizontal_line(5, 5, 16)
    display.draw_horizontal_line(12, 79, 1, character='.')

    display.draw_vertical_line(0, 0, 10, end_character='*')

    display.draw_rectangle(8, 26, 3, 5)
    display.draw_rectangle(6, 34, 5, 7, \
        horizontal_character='=', vertical_character=':', corner_character='/')

    display.set_text(5, 45, '  Hello, World!  ')

    display.display()
