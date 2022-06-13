"""
Weigher
=======

Class to give weight to words and letters
"""


class WordsWeigher:
    def __init__(self, words: list[str]):
        self.words = words
        self.letter_weight: dict[str, int] = {}

        self.invalid_letters: list[str] = []
        self.correct_letters: list = [None, None, None, None, None]
        self.discovered_letters: list[str] = []
        self.unpositioned_letters: list[list[str]] = [[], [], [], [], []]

        self.invalid_multiplier: int = 1
        self.correct_multiplier: int = 1
        self.discovered_multiplier: int = 1
        self.unpositioned_multiplier: int = 1

        self.generate_letter_weight()

    def generate_letter_weight(self) -> None:
        """Counts how many times each letter appears in the words then normalizes giving a weight to each one"""
        for word in self.words:
            for letter in list(word):
                if letter not in self.letter_weight:
                    self.letter_weight[letter] = 0
                self.letter_weight[letter] += 1
                
        sorted_letters = sorted(self.letter_weight.items(), key=lambda x: x[1])
        for idx, letter in enumerate(sorted_letters):
            self.letter_weight[letter[0]] = idx + 1

    def get_letter_weight(self, letter: str, idx: int = 0) -> int:
        """Returns the weight of a letter"""
        letter_weitgth = self.letter_weight[letter]
        if self.invalid_letters and letter in self.invalid_letters:
            letter_weitgth *= self.invalid_multiplier
        if self.correct_letters[idx] and letter in self.correct_letters[idx]:
            letter_weitgth *= self.correct_multiplier
        if self.discovered_letters and letter in self.discovered_letters:
            letter_weitgth *= self.discovered_multiplier
        if self.unpositioned_letters[idx] and letter in self.unpositioned_letters[idx]:
            letter_weitgth *= self.unpositioned_multiplier
        return letter_weitgth

    def set_state(self,
                  invalid_letters: list[str],
                  correct_letters: list,
                  discovered_letters: list[str],
                  unpositioned_letters: list[list[str]]) -> None:
        """Sets the state of the weigher"""
        self.invalid_letters = invalid_letters
        self.correct_letters = correct_letters
        self.discovered_letters = discovered_letters
        self.unpositioned_letters = unpositioned_letters

    def set_multipliers(self,
                        invalid_multiplier: int = 1,
                        correct_multiplier: int = 1,
                        discovered_multiplier: int = 1,
                        unpositioned_multiplier: int = 1) -> None:
        """Sets the multipliers of the weigher"""
        self.invalid_multiplier = invalid_multiplier
        self.correct_multiplier = correct_multiplier
        self.discovered_multiplier = discovered_multiplier
        self.unpositioned_multiplier = unpositioned_multiplier

    def get_word_weight(self,
                        word: str,
                        consider_duplicates: bool = True,
                        variation_multiplier: bool = False) -> int:
        """Returns the weight of a word"""
        weight = 0
        letters = []
        for idx, letter in enumerate(list(word)):
            if letter not in letters or consider_duplicates:
                weight += self.get_letter_weight(letter, idx)
            if letter not in letters:
                letters.append(letter)
        if variation_multiplier:
            weight *= len(letters)
        return weight
