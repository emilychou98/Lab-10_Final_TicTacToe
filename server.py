from flask import Flask, render_template, redirect, url_for, request, session
from game import static_check_draw,static_get_winner,static_get_other_players
from database import Database
from player import Player
import numpy as np

app = Flask(__name__)
app.secret_key = b'university_of_washington'

@app.route("/", methods =["GET", "POST"])
@app.route("/index", methods =["GET", "POST"])
def index():
    if request.method == 'POST':
        player_type = request.form.get("player_type")
        player1_name = request.form.get("player1_name")
        if player_type == "singleplayer":
            player2_name = 'Bot'
        else:
            player2_name = request.form.get("player2_name")
            
        session['O'] = {
            'name':player1_name,
            'char':'O'
        }
        session['X'] = {
            'name':player2_name,
            'char':'X'
        }
        
        session['board'] = [[None,None,None],[None,None,None],[None,None,None]]
        session['turn'] = 'O'
        session['game_type'] = player_type
        return redirect(url_for('game'))
    return render_template("index.html")

@app.route("/game/")
@app.route("/game/<int:row>/<int:col>")
def game(row=None,col=None):    
    if row is not None:
        session['board'][row][col] = session['turn']
        winner = static_get_winner(session['board'])
        if winner:
            loser_name = session[static_get_other_players(winner)]['name']
            winner_name = session[winner]['name']
            return redirect(url_for(
                'end',
                winner_name=winner_name,
                loser_name=loser_name,
                is_draw=False
            ))
        if static_check_draw(session['board']):
            return redirect(url_for(
                'end',
                winner_name=session['O']['name'],
                loser_name=session['X']['name'],
                is_draw=True
            ))
        session['turn'] = static_get_other_players(session['turn'])
                
        #Bot
        if (session['game_type'] == 'singleplayer') and (session['turn']=='X'):
            # bot move
            if session['board'][1][1] is None:
                session['board'][1][1] = session['turn']
            else:
                avails = np.where(np.array(session['board']) == None)
                chosenY = avails[0][0]
                chosenX = avails[1][0]
                session['board'][chosenY][chosenX] = session['turn']
            #end bot move
            winner = static_get_winner(session['board'])
            if winner:
                loser_name = session[static_get_other_players(winner)]['name']
                winner_name = session[winner]['name']
                return redirect(url_for(
                    'end',
                    winner_name=winner_name,
                    loser_name=loser_name,
                    is_draw=False
                ))
            if static_check_draw(session['board']):
                return redirect(url_for(
                    'end',
                    winner_name=session['O']['name'],
                    loser_name=session['X']['name'],
                    is_draw=True
                ))
            session['turn'] = static_get_other_players(session['turn'])
    return render_template("game.html",board=session['board'],turn=session['turn'])

@app.route("/end/<string:winner_name>/<string:loser_name>/<int:is_draw>")
def end(winner_name,loser_name,is_draw):
    winnerPlayer = Player(None,winner_name)
    loserPlayer = Player(None,loser_name)
    
    database = Database('games.csv','players.csv','moves.csv')
    game_id = (
            session['O']['name']+session['X']['name']
            +database.get_time()
        )
    database.start_game(
        game_id,
        Player(None,session['O']['name']),
        Player(None,session['X']['name'])
    )

    if is_draw:
        database.end_game(game_id,None)
        database.update_player_stats(winnerPlayer,'draw')
        database.update_player_stats(loserPlayer,'draw')
        win_msg = 'Draw'
    else:
        database.end_game(game_id,winner_name)
        database.update_player_stats(winnerPlayer,'win')
        database.update_player_stats(loserPlayer,'lose')
        win_msg = f'{winner_name} wins!'
        
    database.write_records_to_disk()
    leaderboard = database.get_leaderboard().to_dict(orient='index')
    return render_template("stats.html",win_msg=win_msg,statistics=leaderboard)
