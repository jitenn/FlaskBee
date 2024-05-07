from datetime import datetime, timezone
from flask import render_template, flash, redirect, url_for, request, g, current_app, session
from langdetect import detect, LangDetectException
from app.main.forms import EmptyForm, GuessForm
from app.main import bp
from app.main.beeWords import loadDictionary, setUpGame
# from app import myDictionary

# print("routes")

@bp.before_app_request
def before_request():
    ''' Placeholder for before_app_request '''
    pass

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
def index():

    # session.pop('correct_guesses', None) 
    # session.pop('game_answers', None) 

    form = EmptyForm()
    if form.validate_on_submit():
        return redirect(url_for('main.spellingbee'))

    return render_template('index.html', title='Home', form=form)

@bp.route('/newgame', methods=['GET', 'POST'])
def newgame():

    session.pop('correct_guesses', None) 
    session.pop('game_answers', None) 

    current_app.myGame.select_random_word(current_app.myDictionary.dictionaryWords) 
    myGame = current_app.myGame
    print(myGame.gameAnswers)

    return redirect(url_for('main.spellingbee'))


@bp.route('/spellingbee', methods=['GET', 'POST'])
def spellingbee():
    
    myGame = current_app.myGame
    
    form = GuessForm(game_alphabets=myGame.gameAlphabets, game_answers=myGame.gameAnswers)
    # print(myGame.gameAlphabets)
    session['game_answers'] = sorted(myGame.gameAnswers)

    if form.validate_on_submit():
        # try:
        #     language = detect(form.guess.data)
        # except LangDetectException:
        #     language = ''

        # flash(f'You guessed {form.guess.data}')
        session['correct_guesses'] = sorted(session.get('correct_guesses', []) + [form.guess.data.upper()])
        print("here")
        print(session['game_answers'])
        print("here")

        print(session.get('correct_guesses'))
        return redirect(url_for('main.spellingbee'))
        # return render_template('spellingbee.html', title='Home', form=form, game_alphabets = myGame.gameAlphabets, correct_guesses=form.guess.data)

    page = request.args.get('page', 1, type=int)

    return render_template('spellingbee.html', title='Home', form=form, game_alphabets = myGame.gameAlphabets)
