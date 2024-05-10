from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, current_app, session
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

    print(f'Home Page Traffic From : {request.remote_addr}')
    print(request.headers.getlist("X-Forwarded-For"))
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
    session.pop('max_score', None)

    # Set up new game
    myGame = setUpGame(current_app.myDictionary.dictionaryWords) 

    print(f'New Game Traffic From : {request.remote_addr}')
    print(myGame.gameAnswers)

    session['in_a_game'] = True
    session['game_requiredletter'] = myGame.gameRequiredLetter
    session['game_alphabets'] = myGame.gameAlphabets
    session['game_answers'] = sorted(myGame.gameAnswers)
    session['game_ranks'] = myGame.gameRanks
    session['current_score'] = 0
    session['current_rank'] = myGame.gameRanks[0][1]
    session['max_score'] = myGame.gameRanks[-1][0]
    # print(session['current_rank'])
    
    flash('New game generated - all the best!')
    
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
        
        tempDictScore = {word: value for word, _, value in session['game_answers']}
        tempDictPangram = {word: isPangram for word, isPangram, _ in session['game_answers']}
        
        flash(f'{tempDictPangram.get(form.guess.data.upper())}  Points: {tempDictScore.get(form.guess.data.upper()) }')
        
        session['current_score'] += tempDictScore.get(form.guess.data.upper())
        
        if session['current_score'] == session['max_score']:
            flash(f"C O N G R A T U L A T I O N S - You are Queen Bee!!")
            session['current_rank'] = session['game_ranks'][-1][1]
        else:
            tempLastRank = session['game_ranks'][0][1]
            for cutoff, rank in session['game_ranks']:
                if session['current_score'] < cutoff:
                    session['current_rank'] = tempLastRank
                    break
                tempLastRank = rank
        
        # print(session['current_score'])
        # print(session['current_rank'])

        # print(session.get('correct_guesses'))

        return redirect(url_for('main.spellingbee'))
    else:
        if len(form.guess.errors) > 0:
            flash(f'Try again. {form.guess.errors[0]}', 'error')
        # print(len(form.guess.errors))
        # print(form.guess.errors)


    page = request.args.get('page', 1, type=int)

    return render_template('spellingbee.html', title='Home', form=form, game_alphabets = session['game_alphabets'])
