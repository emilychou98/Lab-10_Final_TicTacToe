import unittest
from game import Game
from player import Bot

class TestGame(unittest.TestCase):
    
    def test_get_winner(self):
        """unit tests get_winner function of game.py
        """
        
        player1 = Bot('X')
        player2 = Bot('O')
        game = Game(player1,player2)
        board = game.get_board()
        
        board.set_board([
            ['X', None, 'O'],
            [None, 'X', None],
            [None, 'O', 'X'],
        ])
        self.assertEqual(game.get_winner(board), 'X')
        
        board.set_board([
            ['X', None, 'O'],
            [None, 'O', None],
            [None, 'O', 'X'],
        ])
        self.assertEqual(game.get_winner(board), None)
        
        board.set_board([
            [None, 'O', None],
            ['X', 'O', None],
            [None, 'O', 'X'],
        ])
        self.assertEqual(game.get_winner(board), 'O')
        
        board.set_board([
            ['O', None, 'O'],
            ['X', 'X', 'X'],
            [None, 'O', 'O'],
        ])
        self.assertEqual(game.get_winner(board), 'X')
        
        board.set_board([
            ['O', None, 'X'],
            ['O', 'X', 'O'],
            ['X', 'O', 'X'],
        ])
        self.assertEqual(game.get_winner(board), 'X')
        
        board.set_board([
            ['O', None, 'X'],
            ['O', 'O', 'X'],
            ['X', 'O', 'X'],
        ])
        self.assertEqual(game.get_winner(board), 'X')
        
        board.set_board([
            ['O', None, 'X'],
            ['O', 'X', 'X'],
            ['O', 'X', 'O'],
        ])
        self.assertEqual(game.get_winner(board), 'O')

    def test_check_draw(self):
        player1 = Bot('X')
        player2 = Bot('O')
        game = Game(player1,player2)
        board = game.get_board()
        board.set_board([
            ['X', 'O', 'X'],
            ['O', 'X', 'X'],
            ['O', 'X', 'O'],
        ])
        self.assertEqual(game.check_draw(board), True)
        
        board.set_board([
            ['X', None, 'X'],
            ['O', 'X', 'X'],
            ['O', 'X', 'O'],
        ])
        self.assertEqual(game.check_draw(board), False)

    def test_other_player(self):
        """unit tests other_player function of game.py
        """
        player1 = Bot('X')
        player2 = Bot('O')
        game = Game(player1,player2)
        self.assertEqual(game.current_player.get_char(),'X')
        game.switch_players()
        self.assertEqual(game.current_player.get_char(),'O')

if __name__ == '__main__':
    unittest.main()