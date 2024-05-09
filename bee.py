from app import create_app  #, myDictionary, myGame
import os
# from app.main.beeWords import loadDictionary, setUpGame
# from app.models import User, Post, Message, Notification, Task

bee = create_app() 


@bee.shell_context_processor
def make_shell_context():
    return {'app': bee, 'os': os}

# Run flask app when invoked from interactive shell
# Commment this out to invoke from shell and debug
if __name__ == '__main__':
    bee.run(port = 5555, debug = True)

