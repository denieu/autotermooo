"""
Weigher
=======

Class to give weight to words and letters
"""


class WordsWeigher:
    def __init__(self, words: list[str]):
        self.words = words
        self.letter_weight: dict[str, int] = {}

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

    def get_letter_weight(self, letter: str) -> int:
        """Returns the weight of a letter"""
        return self.letter_weight[letter]

    def get_word_weight(self,
                        word: str,
                        invalid_letters: list[str],
                        correct_letters: list,
                        discovered_letters: list[str],
                        unpositioned_letters: list[list[str]],
                        invalid_multiplier: int = 1,
                        correct_multiplier: int = 1,
                        discovered_multiplier: int = 1,
                        unpositioned_multiplier: int = 1,
                        consider_duplicates: bool = True,
                        variation_multiplier: bool = False) -> int:
        """Returns the weight of a word"""
        weight = 0
        letters = []
        for idx, letter in enumerate(list(word)):
            if letter not in letters or consider_duplicates:
                letter_weitgth = self.get_letter_weight(letter)

                if invalid_letters and letter in invalid_letters:
                    letter_weitgth *= invalid_multiplier
                if correct_letters[idx] and letter in correct_letters[idx]:
                    letter_weitgth *= correct_multiplier
                if discovered_letters and letter in discovered_letters:
                    letter_weitgth *= discovered_multiplier
                if unpositioned_letters[idx] and letter in unpositioned_letters[idx]:
                    letter_weitgth *= unpositioned_multiplier

                weight += letter_weitgth
            if letter not in letters:
                letters.append(letter)
        if variation_multiplier:
            weight *= len(letters)
        return weight
