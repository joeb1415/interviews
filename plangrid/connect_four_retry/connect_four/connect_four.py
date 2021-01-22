import logging


class ConnectFour:
    def __init__(self, row_count=6, column_count=7):
        self.row_count = row_count
        self.column_count = column_count

        self.board = []
        for _ in range(row_count):
            row = [0 for _ in range(column_count)]
            self.board.append(row)

    def print_board(self):
        board_str = "\n".join([" ".join([str(cell) for cell in row]) for row in self.board])
        logging.warning("\n" + board_str)

    def drop_piece(self, player, col):
        for row in range(self.row_count - 1, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = player
                return
        raise Exception("Column already full")

    def check_win(self, player, row, col):
        if self._check_horizontal(player=player, row=row, col=col):
            return True

    def _check_horizontal(self, player, row, col):
        left = 0
        for c in range(col - 1, -1, -1):
            if self.board[row][c] == player:
                left += 1
            else:
                break

        right = 0
        for c in range(col + 1, self.column_count, 1):
            if self.board[row][c] == player:
                right += 1
            else:
                break

        if left + right >= 3:
            return True
