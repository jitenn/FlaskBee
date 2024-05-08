from flask import request, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, validators
from wtforms.validators import ValidationError, DataRequired, Length

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username


class GuessForm(FlaskForm):
    guess = StringField('Guess', 
                        [validators.DataRequired()], 
                        render_kw={'style': ' \
                                   text-transform: uppercase; \
                                   font-weight: bold; \
                                   letter-spacing: 1px; \
                                   font-size: 20px \
                                   '}
                        )
        
    submit = SubmitField('Try (Press Enter)')

    # Overloaded constructor accepts the game alphabets as an argument and saves in the object
    def __init__(self, game_alphabets, game_answers, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.game_alphabets = game_alphabets
        self.game_answers = game_answers

    # WTForms implements validate_<field name> as default validator for <field name>
    def validate_guess(self, guess):
        
        allowed_words = [word_pangram_score[0].upper() for word_pangram_score in self.game_answers]

        if len(guess.data.upper()) < 4:      
            raise ValidationError("Too short")
        elif self.game_alphabets[-1] not in guess.data.upper():       # rightmost letter is center letter
            raise ValidationError("Your guess must include the center letter")
        elif not (set(self.game_alphabets) >= set(guess.data.upper())):
            raise ValidationError("You must use the letters in the hive, and only the letters in the hive")
        elif guess.data.upper() not in allowed_words:
            raise ValidationError("Not a word")
        elif guess.data.upper() in session.get('correct_guesses', []):
            raise ValidationError("Already found")
            
            


class EmptyForm(FlaskForm):
    submit = SubmitField('Play Jiten\'s Spelling Bee')


class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *arg, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'meta' not in kwargs:
            kwargs['meta'] = {'csrf': False}
        super(SearchForm, self).__init__(*arg, **kwargs)


class MessageForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')
