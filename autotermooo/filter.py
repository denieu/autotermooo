"""
Filter
======

Class to filter words.
"""


class WordsFilter:
    def __init__(self, words: list[str]):
        self.words = words

    def by_correct_letters(self, correct_letters: list[str]) -> None:
        """Remove words that don't have the correct letters in the correct positions"""
        new_words = []
        for word in self.words:
            if all(letter is None or word[idx] == letter for idx, letter in enumerate(correct_letters)):
                new_words.append(word)
        self.words = new_words

    def by_invalid_letters(self, invalid_letters: list[str]) -> None:
        """Remove words that have invalid letters"""
        self.words = [word for word in self.words if all(letter not in word for letter in invalid_letters)]

    def by_discovered_letters(self, discovered_letters: list[str]) -> None:
        """Remove words that not have discovered letters"""
        self.words = [word for word in self.words if all(letter in word for letter in discovered_letters)]

    def by_unpositioned_letters(self, unpositioned_letters: list[list[str]]) -> None:
        """Remove words that have unpositioned letters"""
        new_words = []
        for word in self.words:
            if all(all(word[idx] != letter for letter in letters)
                   for idx, letters in enumerate(unpositioned_letters) if letters):
                new_words.append(word)
        self.words = new_words

    def get_filtered(self) -> list[str]:
        """Get the filtered words"""
        return self.words
