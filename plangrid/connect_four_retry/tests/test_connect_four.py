import unittest

from connect_four.connect_four import ConnectFour


class TestConnectFour(unittest.TestCase):
    def test_print_empty_board(self):
        connect_four = ConnectFour()
        self.assertEqual(connect_four.board[0][0], 0)

        connect_four.print_board()

    def test_drop_piece(self):
        connect_four = ConnectFour()
        connect_four.drop_piece(player=1, col=0)
        self.assertEqual(connect_four.board[5][0], 1)
        connect_four.drop_piece(player=2, col=0)
        self.assertEqual(connect_four.board[4][0], 2)

        connect_four.print_board()

    def test_drop_piece_raise_column_full(self):
        connect_four = ConnectFour()
        for row in range(connect_four.row_count):
            connect_four.drop_piece(player=1, col=0)

        connect_four.print_board()

        with self.assertRaises(Exception) as e:
            connect_four.drop_piece(player=1, col=0)
        self.assertEqual(str(e.exception), "Column already full")

        connect_four.print_board()

    def test_check_win_horizontal(self):
        connect_four = ConnectFour()
        connect_four.drop_piece(player=1, col=0)
        connect_four.drop_piece(player=1, col=1)
        connect_four.drop_piece(player=1, col=2)
        self.assertFalse(connect_four.check_win(1, 5, 2))
        connect_four.drop_piece(player=1, col=3)
        self.assertTrue(connect_four.check_win(1, 5, 3))
        self.assertTrue(connect_four.check_win(1, 5, 2))
        self.assertTrue(connect_four.check_win(1, 5, 1))
        self.assertTrue(connect_four.check_win(1, 5, 0))


if __name__ == "__main__":
    unittest.main()
