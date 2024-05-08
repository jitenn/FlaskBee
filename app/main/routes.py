from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, current_app, session
from langdetect import detect, LangDetectException
from app.main.forms import EmptyForm, GuessForm
from app.main import bp
from app.main.beeWords import loadDictionary, setUpGame


@bp.before_app_request
def before_request():
    ''' Placeholder for before_app_request '''
    pass

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    form = EmptyForm()

    if form.validate_on_submit():
        if session.get('in_a_game', None) is None:
            return redirect(url_for('main.newgame'))
        else:
            return redirect(url_for('main.spellingbee'))

    return render_template('index.html', title='Home', form=form)


@bp.route('/newgame', methods=['GET', 'POST'])
def newgame():

    # Kill the session variables
    session.pop('in_a_game', None) 
    session.pop('game_requiredletter', None)
    session.pop('game_alphabets', None) 
    session.pop('game_answers', None) 
    session.pop('game_ranks', None) 
    session.pop('current_rank', None)
    session.pop('current_score', None)
    session.pop('correct_guesses', None) 

    # Set up new game
    myGame = setUpGame(current_app.myDictionary.dictionaryWords) 

    print(myGame.gameAnswers)

    session['in_a_game'] = True
    session['game_requiredletter'] = myGame.gameRequiredLetter
    session['game_alphabets'] = myGame.gameAlphabets
    session['game_answers'] = sorted(myGame.gameAnswers)
    session['game_ranks'] = myGame.gameRanks
    session['current_score'] = 0
    session['current_rank'] = myGame.gameRanks[0][1]
    print(session['current_rank'])
    
    flash('Generated new game - All the best!')
    
    return redirect(url_for('main.spellingbee'))


@bp.route('/spellingbee', methods=['GET', 'POST'])
def spellingbee():
    
    # Check if myGame has already been created. If not, create new game first
    # if not hasattr(current_app, 'myGame'):
    if session.get('in_a_game', None) is None:
        return redirect(url_for('main.newgame'))

    # myGame = current_app.myGame
    
    form = GuessForm(game_alphabets=session['game_alphabets'], game_answers=session['game_answers'])

    if form.validate_on_submit():

        # flash(f'You guessed {form.guess.data}')
        session['correct_guesses'] = sorted(session.get('correct_guesses', []) + [form.guess.data.upper()])

        print(session.get('correct_guesses'))

        return redirect(url_for('main.spellingbee'))
    else:
        print("Errors:", form.guess.errors) 

    page = request.args.get('page', 1, type=int)

    return render_template('spellingbee.html', title='Home', form=form, game_alphabets = session['game_alphabets'])
