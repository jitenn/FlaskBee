from flask import Flask, render_template, request
from markupsafe import Markup
from classLoadWordList import LoadWordList

def get_bees(input, word_list, answers):
    for word in word_list:
        if len(word) > 3 and set(word) >= set(input[0]):
            if set(word) <= set(input):
                if set(word) == set(input):
                    pangram = " : PANGRAM"
                else:
                    pangram = ""

                answers.append (word + pangram)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    print("here")

    word_list = LoadWordList("static").word_list  # Load the word list

    user_input = str(request.form.get('user_input', 1))

    answers = []
    get_bees(user_input.lower(), word_list, answers)
  
    result = ""

    for answer in answers:
        result += Markup(str(answer) + "<br>")
    
    return render_template('spellingbee.html', user_input=user_input, result=result)


if __name__ == '__main__':
    app.run(debug=True)
