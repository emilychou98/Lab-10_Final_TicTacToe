from typing import List, Dict, Optional
from player import Player
from database import Database

class Board:
    def __init__(self) -> None:
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None],
        ]
        
    def get_board(self) -> List[List[Optional[str]]]:
        """get board values
        """
        return self.board

    def write_move(self,player_char:str,move_tuple:tuple)->None:
        """write player move to database
        """
        self.board[move_tuple[0]][move_tuple[1]] = player_char
    
    def set_board(self, new_board : List[List[Optional[str]]]) -> None:
        """set what the board should be
        """
        self.board = new_board
        
    def print_board(self)->None:
        """prints what the board is currently
        """
        for row in self.board:
            printLine = [x if x is not None else '_' for x in row]
            print(printLine[0],printLine[1],printLine[2])
        print()


class Game:

    def __init__(self, player1: Player,
             player2: Player, database: Database) -> None:
        self.game_id = (
            player1.get_name()+player2.get_name()
            +database.get_time()
        )
        self.board = Board()
        self.current_player = player1
        self.other_player = player2
        self.database = database

    def run(self) -> None:
        """core game loop
        """
        winner = None
        while winner is None:            
            self.board.print_board()
            #check if all spaces are filled and it's a draw
            if self.check_draw(self.board):
                self.conclude_game(
                    self.current_player,'draw',
                    self.other_player,'draw',
                    None
                )
                break
            
            #have current player make move
            player_move = self.current_player.make_move(
                    self.board.get_board()
            )
            self.board.write_move(
                self.current_player.get_char(),
                player_move
            )
            self.database.record_move(
                self.current_player,
                self.game_id,
                player_move
            )

            #check winner
            winner = self.get_winner(self.board)
            
            #Winner found, print end result
            if winner is not None:
                self.board.print_board()
                self.conclude_game(
                    self.current_player,'win',
                    self.other_player,'lose',
                    self.current_player.get_name()
                )
                break

            self.switch_players()
            
    def switch_players(self)->None:
        """switches player turn
        """
        placeholder = self.current_player
        self.current_player = self.other_player
        self.other_player = placeholder
        
    def check_draw(self, board_obj: Board) -> bool:
        """checks if the game is a draw
        """
        #check if its a draw
        isDraw = True
        for row in board_obj.get_board():
            #if there is space left in the board, it's not a draw
            if None in row:
                isDraw = False
        return isDraw
    
    def get_winner(self, board_obj: Board) -> Optional[str]:
        """Determines the winner of the given board.
        Returns 'X', 'O', or None."""
        
        board = board_obj.get_board()
        
        for i in range(3):
            if ((board[i][0]==board[i][1])
                    and (board[i][1]==board[i][2])
                    and (board[i][0] is not None)):
                return board[i][0] #return row winner
            if ((board[0][i]==board[1][i])
                    and (board[1][i]==board[2][i])
                    and (board[0][i] is not None)):
                return board[0][i] #return col winner
        if ((board[0][0]==board[1][1]) 
                    and (board[1][1]==board[2][2])
                    and (board[0][0] is not None)):
            return board[0][0]
        elif ((board[2][0]==board[1][1]) 
                    and (board[1][1]==board[0][2])
                    and (board[2][0] is not None)):
            return board[2][0]

        return None
    
    def get_board(self)->Board:
        """return board object
        """
        return self.board

    def conclude_game(
                self,player1:Player,result1:str,
                player2:Player,result2:str,
                winner_name:str
            ) -> None:
        """prints game result, statistics, and records said statistics
        """
        if winner_name is None:
            print('Draw')
        else:
            print(f'{winner_name} wins!')
        self.database.end_game(self.game_id,winner_name)
        self.database.update_player_stats(player1,result1)
        self.database.update_player_stats(player2,result2)
        self.database.write_records_to_disk()
        print('Win Ratio Leaderboard:')
        print(self.database.get_leaderboard())
        
def static_check_draw(board:List) -> bool:
    #check if its a draw
    isDraw = True
    for row in board:
        #if there is space left in the board, it's not a draw
        if None in row:
            isDraw = False
    return isDraw

def static_get_other_players(current:str)->str:
    if current=='X':
        return 'O'
    else:
        return 'X'
    
def static_get_winner(board: list) -> Optional[str]:
    """Determines the winner of the given board.
    Returns 'X', 'O', or None."""
    
    for i in range(3):
        if ((board[i][0]==board[i][1])
                and (board[i][1]==board[i][2])
                and (board[i][0] is not None)):
            return board[i][0] #return row winner
        if ((board[0][i]==board[1][i])
                and (board[1][i]==board[2][i])
                and (board[0][i] is not None)):
            return board[0][i] #return col winner
    if ((board[0][0]==board[1][1]) 
                and (board[1][1]==board[2][2])
                and (board[0][0] is not None)):
        return board[0][0]
    elif ((board[2][0]==board[1][1]) 
                and (board[1][1]==board[0][2])
                and (board[2][0] is not None)):
        return board[2][0]

    return None