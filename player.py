from typing import List, Optional
import random 

class Player:
    def __init__(self, player_char:str, player_name:str) -> None:
        self.char = player_char
        self.name = player_name
        
    def get_char(self) -> str:
        """get the type of marker the player is using
        """
        return self.char

    def get_name(self) -> str:
        """get player name
        """
        return self.name
    
class Human(Player):
    
    def make_move(self, board: List[List[Optional[str]]]
            ) -> tuple:
        """have player chose where to set marker
        """
        noValidInput = True
        while(noValidInput):
            y = input(
                f'Player {self.get_name()}\'s turn! Type row you want to mark\n'
            )
            x = input(
                f'Player {self.get_name()}\'s turn! Type column you want to mark\n'
            )
            
            try:
                x = int(x)-1
                y = int(y)-1
                if (x<0) or (x>2) or (y<0) or (y>2):
                    print('row or column selected out of bounds, try again\n')
                    continue                
                if board[y][x] is not None:
                    print('This spot is already marked!, try again\n')
                    continue
                noValidInput=False
            except:
                print('Invalid input, input must be a single digit number, try again\n')

        return (y,x)        
        
        
class Bot(Player):
    
    def __init__(self, player_char: str, player_name: str = 'Bot') -> None:
        super().__init__(player_char, player_name)

    def make_move(self, board: List[List[Optional[str]]]
            ) -> tuple:
        """choose where to set marker
        """
        
        #Middle space is the best
        #take it if available
        if board[1][1] is None:
            print('Bot has made a move!')
            return (1,1)
        
        available_spaces = []
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col] is None:
                    available_spaces.append((row,col))
                    
        selected = random.choice(available_spaces)
        print('Bot has made a move!')
        return (selected[0],selected[1])