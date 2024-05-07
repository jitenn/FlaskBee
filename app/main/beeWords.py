import requests
from flask import current_app
from collections import Counter
import os
import random
import string

class loadDictionary:
    def __init__(self, config, listtype = "static") -> None:
        """
        Validate gameAlphabets.
        
        Args:
            listtype (str): "dynamic" or "static" (default) 

        Returns:
            
        """
        print("Loading Dictionary")

        if listtype is None:
            listtype = "dynamic"

        self.url = config['DICTIONARY_DYNAMIC']
        self.filename= os.path.join(os.path.dirname(__file__), config['DICTIONARY_STATIC'])
        # self.url = "https://ia803406.us.archive.org/31/items/csw21/CSW21.txt"
        # self.filename= os.path.join(os.path.dirname(__file__),"txtDictionary12Dicts.txt")
        
        if listtype.lower() == "static":
            self.dictionaryWords = self._loadFromDictionaryStatic()
        else:
            self.dictionaryWords = self._loadFromDictionaryDynamic()

        self.max_letter_occurrences = self._find_max_letter_occurrences()


    def _loadFromDictionaryDynamic(self):
        response = requests.get(self.url)
        response.raise_for_status() 
        return response.text.upper().splitlines()


    def _loadFromDictionaryStatic(self):
        """Loads a list of words from a text file"""
        with open(self.filename, "r") as f:
            return [word.upper().strip() for word in f.readlines()]


    def _find_max_letter_occurrences(self):
        """Finds the maximum occurrence of each letter in the alphabet among all the words."""
        all_letters = Counter()
        for word in self.dictionaryWords:
            word_counter = Counter(word.upper())  # Create a Counter for each word
            for letter, count in word_counter.items():  # Iterate through letter counts
                all_letters[letter] = max(all_letters[letter], count)  # Update with max
        return dict(all_letters)  # Return the combined counts


class setUpGame:
    def __init__(self, myDict) -> None:
        """
        Sets up the game
        
        Args:
            listtype (list of words): Universe list of dictionary words

        Returns:
            
        """
        self.myDict  = myDict
        possibleWord = self.select_random_word(myDict)
        print(possibleWord)
        self.gameRequiredLetter = possibleWord[-1]
        # self.gameAlphabets = list(set(possibleWord))
        self.gameAlphabets = list(set(possibleWord.replace(self.gameRequiredLetter,'')))
        self.gameAlphabets.append(self.gameRequiredLetter)
        self.gameAnswers = self.get_bees(gameAlphabets=self.gameAlphabets, 
                                         gameRequiredLetter=self.gameRequiredLetter,
                                         dictionaryWords=self.myDict)
        self.gameRanks = self.get_ranks()

        print(self.gameAlphabets)
        print(self.gameRequiredLetter)
        print(self.gameAnswers)
        print(self.get_ranks())


    def _has_suitable_letters(self, word):
        """Checks if a word has exactly 7 unique letters, and no 's' or 'q."""
        return len(set(word)) == 7 and all(letter not in word.upper() for letter in current_app.config['LETTERS_TO_AVOID']) 
        # return len(set(word)) == 7 and 'S' not in word.upper() and 'Q' not in word.upper()


    def select_random_word(self, word_list):
        """Selects a random word with 7 unique letters from the list."""
        print("Generating word")
        eligible_words = [word for word in word_list if self._has_suitable_letters(word)]

        if eligible_words:
            while True:
                possibleWord = random.choice(eligible_words)
                possibleBees = self.get_bees(list(possibleWord), possibleWord[-1], self.myDict)

                if len(possibleBees) > current_app.config['BEES_MINIMUM'] and len(possibleBees) <= current_app.config['BEES_MAXIMUM']:
                    print(len(possibleBees), possibleWord, possibleWord[-1])
                    self.gameAlphabets = list(set(possibleWord))
                    self.gameAnswers = possibleBees
                    self.gameRequiredLetter = possibleWord[-1]
                
                    return possibleWord
                    break
        else:
            return None  # No words found with 7 unique letters

    
    def get_bees(self, gameAlphabets, gameRequiredLetter, dictionaryWords):
        gameAnswers = []

        for word in dictionaryWords:
            if len(word) > 3 and set(word) >= set(gameRequiredLetter):
                if set(word) <= set(gameAlphabets):
                    is_pangram = "PANGRAM" if set(word) == set(gameAlphabets) else ""
                    score = len(word) + len(is_pangram) if len(word) > 4 else 1
                    gameAnswers.append((word, is_pangram, score))  # Create a tuple
                    
        # self.gameAnswers = gameAnswers
        return gameAnswers 
    
    def get_ranks(self):
        gameScore = 0

        for word, is_pangram, score in self.gameAnswers:
            gameScore += score

        gameRanks = [(0, "Beginner"),
                     (int(gameScore * 0.02), "Good Start"),
                     (int(gameScore * 0.05), "Moving Up"),
                     (int(gameScore * 0.08), "Good"),
                     (int(gameScore * 0.15), "Solid"),
                     (int(gameScore * 0.25), "Nice"),
                     (int(gameScore * 0.4), "Great"),
                     (int(gameScore * 0.5), "Amazing"),
                     (int(gameScore * 0.7), "Genius"),
                     (gameScore, "Queen Bee!")
                    ]
        
        return gameRanks
