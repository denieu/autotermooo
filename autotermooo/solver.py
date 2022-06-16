"""
Solver
======

Class to solve termoo game.
"""
from autotermooo.filter import WordsFilter
from autotermooo.weigher import WordsWeigher

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
        self.weigher = WordsWeigher(self.words)

    def read_words(self, words_file: str) -> None:
        with open(words_file) as words_fp:
            self.words = words_fp.read().splitlines()

    def choose_best_word(self, words: list[str], discover_new_letters: bool = False) -> (str, float):
        self.weigher.set_state(self.invalid_letters, self.correct_letters,
                               self.discovered_letters, self.unpositioned_letters)
        self.weigher.set_multipliers(invalid_multiplier=-10 if discover_new_letters else 1,
                                     correct_multiplier=1 if discover_new_letters else 1,
                                     discovered_multiplier=-1 if discover_new_letters else 1,
                                     unpositioned_multiplier=-100 if discover_new_letters else 1)

        choosen_word = words[0]
        max_weight = self.weigher.get_word_weight(choosen_word, discover_new_letters)

        for word in words[1:]:
            new_weigth = self.weigher.get_word_weight(word, discover_new_letters)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_round_word(self) -> (str, float, list[str]):
        word_filter = WordsFilter(self.words)
        word_filter.by_invalid_letters(self.invalid_letters)
        word_filter.by_correct_letters(self.correct_letters)
        word_filter.by_discovered_letters(self.discovered_letters)
        word_filter.by_unpositioned_letters(self.unpositioned_letters)
        filtered_words = word_filter.get_filtered()

        if not filtered_words:
            raise Exception("Word not found")

        choosen_word, accuracy = self.choose_best_word(filtered_words)
        # if accuracy <= 5:
        #     choosen_word, accuracy = self.choose_best_word(self.words,
        #                                                    discover_new_letters=True,
        #                                                    consider_duplicates=False, variation_multiplier=True)
        #     accuracy = 0
        return choosen_word, accuracy, filtered_words

    def play_round(self) -> (str, float, list[str]):
        if not len(self.game_rounds):
            choosen_word, accuracy = self.choose_best_word(self.words, discover_new_letters=True)
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
