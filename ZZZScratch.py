from app.main.beeWords import loadDictionary, setUpGame
import random

myDict  = loadDictionary().dictionaryWords
s = setUpGame(myDict)
# print(s.gameAnswers)
print(s.gameAlphabets)

# word = "CEDE"
# gameAlphabets = ["P", "I", "C", "K", "L", "E", "D"]  
# gameAnswers = []
# if len(word) > 3 and set(word) >= set(gameAlphabets[0]):
#     print("a")
#     if set(word) <= set(gameAlphabets):
#         print("b")
#         is_pangram = "PANGRAM" if set(word) == set(gameAlphabets) else ""
#         gameAnswers.append((word, is_pangram))  # Create a tuple

# print(word)
# print(gameAlphabets)
# print(gameAnswers)

# def has_suitable_letters(word):
#     """Checks if a word has exactly 7 unique letters, and no 's' or 'q."""
#     return len(set(word)) == 7 and 's' not in word.lower() and 'q' not in word.lower()

# def select_random_word(word_list):
#     """Selects a random word with 7 unique letters from the list."""
#     eligible_words = [word for word in word_list if has_suitable_letters(word)]

#     if eligible_words:
#         goodSetup = False
#         while True:
#             possibleWord = random.choice(eligible_words)
#             possibleBees = setUpGame.get_bees(list(possibleWord),myDict)

#             if len(possibleBees) > 25 and len(possibleBees) <= 75:
#                 print(possibleWord, len(possibleBees))
#                 print(possibleBees)
#                 return possibleWord
#                 break
#     else:
#         return None  # No words found with 7 unique letters

# # Example usage
# # my_word_list = ["apple", "banana", "straight", "computer", "keyboard"]
# random_word = select_random_word(myDict)

# if random_word:
#   print("Selected word:", random_word)
#   print("Letters:", set(random_word))
# else:
#   print("No suitable words found in the list.")


# goodSetUp = False
# while not goodSetUp:
#     myGame = setUpGame()
#     print(myGame.gameAlphabets)
#     bees = myGame.get_bees(myDict)
#     for word, status in bees:
#         goodSetUp = True if status == 'PANGRAM' else False
    
# print(bees)

# myGame.gameAlphabets = ["j", "o", "i", "n"]
# print(myGame.gameAlphabets)


# print(len(x.word_list))

# =======================
# decorator
# =======================

# def decorator1(func):
#     def dec1(*args, **kwargs):
#         print("in decorator1")
#         print(args)
#         print(kwargs)
#         print(func.__name__, func.__doc__)
#         result = func(*args, **kwargs)
#         return result
#     return dec1
# @decorator1
# def func1(*arg, **kwargs):
#     # Documentation
#     '''dasda'''
#     print("in func1")
#     x=2
#     print(x)
# func1(1, 2, 3, a="a")






# from app import myFlask, myDB
# from app.myModels import User, Post
# import sqlalchemy as sa

# myFlask.app_context().push()

# Passord hashing
# from werkzeug.security import check_password_hash, generate_password_hash
# x = generate_password_hash("test")
# print(x, check_password_hash(x, "test"))

# ==============================
# SQLAlchemy
# ==============================

# INSERT
# u = User(username = "u2", email = "u2@test.com")
# myDB.session.add(u)
# myDB.session.commit()

# SELECT no WHERE
# query = sa.select(User)
# users = myDB.session.scalars(query).all()
# for u in users:
#     print (u.id, u.username, u.email, u.posts)

# SELECT WHERE
# u = myDB.session.get(User, 1)
# print (u.id, u.username, u.email, u.posts)
# 
# query = sa.select(User).where(User.username.like('u%'))
# print(myDB.session.scalars(query).all())


# INSERT with foreign key refernced by object
# u = myDB.session.get(User, 1)
# p = Post(body="another post", author=u)
# myDB.session.add(p)
# myDB.session.commit()
# u = myDB.session.get(User, 1)
# print (u.id, u.username, u.email, u.posts)

# SELECT ORDER BY
# query = sa.select(User).order_by(User.username.desc())
# print(myDB.session.scalars(query).all())

# UPDATE
# myDB.session.query(User).filter(User.id==2).update({'username':'User 2'},synchronize_session=False)
# myDB.session.commit()

# All other SQLAlchemy
# query = sa.select(Post)
# posts = myDB.session.scalars(query)
# for p in posts:
#     print(p.id, p.author.username, p.body)
# 
# for x in range(1,4):
#     u = myDB.session.get(User, x)
#     query = u.posts.select()
#     posts = myDB.session.scalars(query).all()
#     print(u, posts)


# ==============================
# Load environment variables from .env file
# ==============================
# from dotenv import load_dotenv
# import os
# load_dotenv(".flaskenv")
# print(os.getenv("FLASK_APP"))

# ==============================
# # Flask mail
# # ==============================
# from flask_mail import Message
# from app import myMail, myFlask
# msg = Message('test subject', sender=myFlask.config['ADMINS'][0],
# recipients=['your-email@example.com'])
# msg.body = 'text body'
# msg.html = '<h1>HTML body</h1>'
# myMail.send(msg)