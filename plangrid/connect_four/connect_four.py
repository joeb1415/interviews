import pandas as pd


class ConnectFour:
    def __init__(self):
        self.width = 7
        self.height = 6
        self.columns = [i for i in range(self.width)]
        self.rows = [i for i in range(self.height - 1, -1, -1)]  # rows are indexed with 0 at the bottom
        self.board = pd.DataFrame(data=0, index=self.rows, columns=self.columns)
        self.next_row = pd.Series(data=0, index=self.columns)

    def insert_piece(self, player_id, column):
        """

        :param player_id: i.e. 1 or 2
        :param column: int in range 0 to width-1
        :return:
        """
        if self.next_row[column] == self.height:
            raise Exception('Column already full')

        row = int(self.next_row[column])  # next_row is int64... ugh.

        self.board.loc[row, column] = player_id
        self.next_row[column] += 1

        winning_player_id, squares = self.check_win(player_id, column, row)  # 0 if no winner

        return winning_player_id, squares

    def return_board(self):
        """
        :return:
        [
            col_0: [
                row_0: 1, # i.e. "player 1"
                row_1: 2,
                row_2: 0
                ...
            ],
            ...
        ]

        """

        return self.board.to_json(orient='records')

    def check_win(self, player_id, column, row):
        """

        :param player_id: i.e. 1 or 2
        :param column: int in range 0 to width-1
        :param row: int in range 0 to height-1
        :return:
        """
        cardinals = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
        x_offset = dict(zip(cardinals, [0, 1, 1, 1, 0, -1, -1, -1]))
        y_offset = dict(zip(cardinals, [1, 1, 0, -1, -1, -1, 0, 1]))
        neighbors = dict(zip(cardinals, [[] for _ in range(8)]))  # will be list of locations of player neighbors
        expired = dict(zip(cardinals, [False for _ in range(8)]))

        for direction in cardinals:
            if expired[direction]:
                continue

            for distance in range(1, 4):
                neighbor_row = row + (y_offset[direction] * distance)
                neighbor_col = column + (x_offset[direction] * distance)
                if (
                    (0 <= neighbor_row < self.height) and
                    (0 <= neighbor_col < self.width) and
                    (self.board.loc[neighbor_row, neighbor_col] == player_id)
                ):
                    neighbors[direction].append((neighbor_row, neighbor_col))
                else:
                    expired[direction] = True

        # if 3 neighbors, then we have 4 (including new piece)
        squares = []
        if len(neighbors['n']) + len(neighbors['s']) >= 3:
            squares = [(row, column)] + neighbors['n'] + neighbors['s']
        elif len(neighbors['ne']) + len(neighbors['sw']) >= 3:
            squares = [(row, column)] + neighbors['ne'] + neighbors['sw']
        elif len(neighbors['nw']) + len(neighbors['se']) >= 3:
            squares = [(row, column)] + neighbors['nw'] + neighbors['se']
        elif len(neighbors['w']) + len(neighbors['e']) >= 3:
            squares = [(row, column)] + neighbors['w'] + neighbors['e']

        if not squares:
            return 0, squares

        squares.sort()

        return player_id, squares

    def clear_board(self):
        self.board = pd.DataFrame(data=0, index=self.rows, columns=self.columns)
