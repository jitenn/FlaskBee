import requests
from collections import Counter
import os
import random
import string

class loadDictionary:
    def __init__(self, listtype = "static") -> None:
        """
        Validate gameAlphabets.
        
        Args:
            listtype (str): "dynamic" or "static" (default) 

        Returns:
            
        """
        print("Loading Dictionary")
        if listtype is None:
            listtype = "dynamic"

        self.url = "https://ia803406.us.archive.org/31/items/csw21/CSW21.txt"
        # self.filename="txtCollinsScrabbleWords2019.txt"
        self.filename= os.path.join(os.path.dirname(__file__),"txtDictionary12Dicts.txt")
        
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
        self.gameAlphabets = list(set(possibleWord))
        self.gameRequiredLetter = self.gameAlphabets[-1]
        self.gameAnswers = self.get_bees(gameAlphabets=self.gameAlphabets, 
                                         gameRequiredLetter=self.gameRequiredLetter,
                                         dictionaryWords=self.myDict)
        print(self.gameAlphabets)
        print(self.gameRequiredLetter)
        print(self.gameAnswers)


    def _has_suitable_letters(self, word):
        """Checks if a word has exactly 7 unique letters, and no 's' or 'q."""
        return len(set(word)) == 7 and 'S' not in word.upper() and 'Q' not in word.upper()


    def select_random_word(self, word_list):
        """Selects a random word with 7 unique letters from the list."""
        print("Generating word")
        eligible_words = [word for word in word_list if self._has_suitable_letters(word)]

        if eligible_words:
            while True:
                possibleWord = random.choice(eligible_words)
                possibleBees = self.get_bees(list(possibleWord), possibleWord[-1], self.myDict)

                if len(possibleBees) > 25 and len(possibleBees) <= 60:
                    self.gameAlphabets = list(set(possibleWord))
                    self.gameAnswers = possibleBees
                
                    return possibleWord
                    break
        else:
            return None  # No words found with 7 unique letters

    
    def get_bees(self, gameAlphabets, gameRequiredLetter, dictionaryWords):
        gameAnswers = []
        # print(gameAlphabets)
        # print(gameAlphabets[0])
        for word in dictionaryWords:
            if len(word) > 3 and set(word) >= set(gameRequiredLetter):
                if set(word) <= set(gameAlphabets):
                    is_pangram = "PANGRAM" if set(word) == set(gameAlphabets) else ""
                    gameAnswers.append((word, is_pangram))  # Create a tuple
                    
        # self.gameAnswers = gameAnswers
        return gameAnswers 