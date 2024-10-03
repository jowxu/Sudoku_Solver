import unittest
from sudoku import *
from boards import *

class TestSudoku(unittest.TestCase):

    def test_read_board_correct(self):
        self.assertEqual(read_board('boards/correct.txt'), correct_board)

    def test_read_board_incomplete(self):
        self.assertEqual(read_board('boards/incomplete.txt'), incomplete_board)

    def test_read_board_bad_subsquares(self):
        self.assertEqual(read_board('boards/bad_subsquares.txt'), bad_subsquares_board)

    def test_read_board_bad_rows(self):
        self.assertEqual(read_board('boards/bad_rows.txt'), bad_rows_board)

    def test_read_board_bad_columns(self):
        self.assertEqual(read_board('boards/bad_columns.txt'), bad_columns_board)

    def test_correct_rows(self):
        self.assertTrue(check_rows(correct_board))

    def test_correct_columns(self):
        self.assertTrue(check_columns(correct_board))

    def test_correct_columns(self):
        self.assertTrue(check_squares(correct_board))

    def test_incorrect_rows(self):
        self.assertFalse(check_rows(bad_rows_board))

    def test_incorrect_rows_correct_columns(self):
        self.assertTrue(check_columns(bad_rows_board))

    def test_incorrect_rows_correct_squares(self):
        self.assertTrue(check_squares(bad_rows_board))

    def test_incorrect_columns(self):
        self.assertFalse(check_columns(bad_columns_board))

    def test_incorrect_columns_correct_rows(self):
        self.assertTrue(check_rows(bad_columns_board))

    def test_incorrect_columns_correct_squares(self):
        self.assertTrue(check_squares(bad_columns_board))

    def test_incorrect_squares(self):
        self.assertFalse(check_squares(bad_subsquares_board))

    def test_incorrect_squares_correct_rows(self):
        self.assertTrue(check_rows(bad_subsquares_board))

    def test_incorrect_squares_correct_columnss(self):
        self.assertTrue(check_columns(bad_subsquares_board))

    def test_solve_nearly_full(self):
        self.assertTrue(solve(nearly_full_board))

    def test_solve_incomplete(self):
        self.assertTrue(solve(incomplete_board))

    def test_solve_unsolvable(self):
        self.assertFalse(solve(unsolvable_board))

    def test_solve_unsolvable_board(self):
        solve(unsolvable_board)
        self.assertEqual(unsolvable_board, unsolvable_board_original)

    def test_candidate_values_no_candidates(self):
        self.assertEqual(candidate_values(nearly_full_board, 0, 0), [])

    def test_candidate_values_nearly_full(self):
        self.assertEqual(candidate_values(nearly_full_board, 2, 5), [8])

    def test_candidate_values_unsolvable(self):
        self.assertEqual(candidate_values(unsolvable_board, 0, 8), [3, 7, 8])

    def test_candidate_values_incomplete(self):
        self.assertEqual(candidate_values(incomplete_board, 8, 8), [3, 4, 5, 8])

if __name__ == '__main__':
    unittest.main()