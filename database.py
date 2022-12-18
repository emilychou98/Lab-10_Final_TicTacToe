import pandas as pd
from typing import Dict
from player import Player

class Database:

    def __init__(self,games_file:str,players_file:str, moves_file:str) -> None:
        try:
            self.games = pd.read_csv(games_file)
        except:
            self.games = pd.DataFrame(
                columns=['game_id','player1','player2','winner']
            )

        try:
            self.players = pd.read_csv(players_file,index_col=0)
        except:
            self.players = pd.DataFrame(columns=['win','lose','draw'])
        
        try:
            self.moves = pd.read_csv(moves_file)
        except:
            self.moves = pd.DataFrame(
                columns=['game_id','player_name','player_char','move']
            )

    def get_time(self):
        """gets current time as a timestamp
        """
        return str(pd.to_datetime('today').timestamp())

    def df_add_row(self,df:pd.DataFrame,row_data:tuple)->pd.DataFrame:
        """adds new row to dataframe
        """
        new_row = pd.DataFrame([row_data],columns=df.columns)
        return pd.concat([df,new_row])

    def start_game(self,game_id:str,player1:Player,player2:Player)->None:
        """creates new game record
        """
        self.games = self.df_add_row(
            self.games,
            (game_id,player1.get_name(),player2.get_name(),None)
        )

    def end_game(self,game_id:str,winner:str)->bool:
        """updates winner in game record
        """
        if self.games.iloc[-1]['game_id'] == game_id:
            self.games.iat[self.games.shape[0]-1,3] = winner
            return True
        print('id string does not match')
        return False

    def write_records_to_disk(self)->None:
        """saves database as csv
        """
        self.games.to_csv('games.csv',index=False)
        self.players.to_csv('players.csv')
        self.moves.to_csv('moves.csv',index=False)

    def update_player_stats(self, player:Player,result:str)->None:
        """updates wins/losses/draws for specific player
        """
        player_dict = self.players.to_dict('index')
        if player.get_name() in player_dict.keys():
            player_dict[player.get_name()][result] += 1
        else:
            player_dict[player.get_name()] = {'win':0,'lose':0,'draw':0}
            player_dict[player.get_name()][result] += 1

        self.players = pd.DataFrame.from_dict(player_dict,orient='index')


    def get_leaderboard(self)->pd.DataFrame:
        """calculates win loss ratio and returns top 5 players
        """
        return self.players.join(
            self.players
            .apply(lambda x: round((x.win-x.lose)/sum(x),5),axis=1)
            .rename('win_loss_ratio')
        ).sort_values('win_loss_ratio',ascending=False).head(5)
        
    def record_move(self,player:Player,game_id:str,move:tuple):
        """records the move the player made
        """
        self.moves = self.df_add_row(
            self.moves,
            (game_id,player.get_name(),player.get_char(),move)
        )