"""
Solver
======

Class to solve termoo game.
"""
from autotermooo.filter import WordFilter
INVALID = 0
UNPOSITIONED = 1
CORRECT = 2


class TermoooSolver:
    def __init__(self, words_file: str):
        self.words: list[str] = []
        self.letter_weight: dict[str, int] = {}

        self.game_rounds: list[tuple[str, list[int]]] = []

        self.invalid_letters: list[str] = []
        self.correct_letters: list = [None, None, None, None, None]
        self.discovered_letters: list[str] = []
        self.unpositioned_letters: list[list[str]] = [[], [], [], [], []]

        self.read_words(words_file)
        self.generate_letter_weight()

    def read_words(self, words_file: str) -> None:
        with open(words_file) as words_fp:
            self.words = words_fp.read().splitlines()

    def generate_letter_weight(self) -> None:
        for word in self.words:
            for letter in list(word):
                if letter not in self.letter_weight:
                    self.letter_weight[letter] = 0
                self.letter_weight[letter] += 1

        sorted_letters = sorted(self.letter_weight.items(), key=lambda x: x[1])
        for idx, letter in enumerate(sorted_letters):
            self.letter_weight[letter[0]] = idx + 1

    def get_letter_weight(self, letter: str) -> int:
        return self.letter_weight[letter]

    def get_word_weight(self, word: str, discover_new_letters: bool = False, consider_duplicates: bool = True, variation_multiplier: bool = False) -> int:
        weight = 0
        letters = []
        for idx, letter in enumerate(list(word)):
            if letter not in letters or consider_duplicates:
                letter_weitgth = self.get_letter_weight(letter)
                if discover_new_letters:
                    if letter in self.discovered_letters:
                        letter_weitgth *= -1
                    elif letter in self.invalid_letters:
                        letter_weitgth *= -10
                    elif letter in self.unpositioned_letters[idx]:
                        letter_weitgth *= -100
                weight += letter_weitgth
            if letter not in letters:
                letters += letter
        if variation_multiplier:
            weight *= len(letters)
        return weight

    def choose_best_word(self, words: list[str],
                         discover_new_letters: bool = False,
                         consider_duplicates: bool = True, variation_multiplier: bool = False) -> (str, float):
        choosen_word = words[0]
        max_weight = self.get_word_weight(choosen_word, discover_new_letters, consider_duplicates, variation_multiplier)
        for word in words[1:]:
            new_weigth = self.get_word_weight(word, discover_new_letters, consider_duplicates, variation_multiplier)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_round_word(self) -> (str, float, list[str]):
        word_filter = WordFilter(self.words)
        word_filter.by_invalid_letters(self.invalid_letters)
        word_filter.by_correct_letters(self.correct_letters)
        word_filter.by_discovered_letters(self.discovered_letters)
        word_filter.by_unpositioned_letters(self.unpositioned_letters)
        filtered_words = word_filter.get_filtered()

        if not filtered_words:
            raise Exception("Word not found")

        choosen_word, accuracy = self.choose_best_word(filtered_words)
        if accuracy <= 5:
            choosen_word, accuracy = self.choose_best_word(self.words,
                                                           discover_new_letters=True,
                                                           consider_duplicates=False, variation_multiplier=True)
            accuracy = 0
        return choosen_word, accuracy, filtered_words

    def play_round(self) -> (str, float, list[str]):
        if not len(self.game_rounds):
            choosen_word, accuracy = self.choose_best_word(self.words,
                                                           discover_new_letters=True,
                                                           consider_duplicates=False, variation_multiplier=True)
            return choosen_word, accuracy, self.words

        for letters, letters_status in self.game_rounds:
            letters = list(letters)

            for idx, letter_status in enumerate(letters_status):
                letter = letters[idx]

                if letter_status == INVALID:
                    if letter not in self.invalid_letters:
                        self.invalid_letters.append(letter)
                elif letter_status == UNPOSITIONED:
                    if letter in self.invalid_letters:
                        raise Exception(f"The letter {letter},"
                                        f" was defined as UNPOSITIONED but it had already been defined as INVALID")
                    self.unpositioned_letters[idx] += letter
                    if letter not in self.discovered_letters:
                        self.discovered_letters.append(letter)
                elif letter_status == CORRECT:
                    self.correct_letters[idx] = letter
                    if letter not in self.discovered_letters:
                        self.discovered_letters.append(letter)
                else:
                    raise Exception(f"Invalid letter {letter} status, round {''.join(letters)}")

        return self.choose_round_word()
