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

        self.load_words(words_file)
        self.weigher = WordsWeigher(self.words)

    def load_words(self, words_file: str) -> None:
        with open(words_file) as words_fp:
            self.words = words_fp.read().splitlines()

    def choose_weighty_word(self, words: list[str], variation_multiplier: bool = False) -> (str, float):
        choosen_word = words[0]
        max_weight = self.weigher.get_word_weight(choosen_word, variation_multiplier)

        for word in words[1:]:
            new_weigth = self.weigher.get_word_weight(word, variation_multiplier)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_word_to_discover_letters(self) -> (str, float, str):
        word_filter = WordsFilter(self.words)
        word_filter.by_invalid_letters(self.invalid_letters)
        word_filter.by_discovered_letters(self.discovered_letters)
        filtered_words = word_filter.get_filtered()
        if not filtered_words:
            raise Exception("Word not found")

        new_invalid = self.invalid_letters + [letter for letter in self.correct_letters if letter]
        new_correct = [None, None, None, None, None]

        self.weigher = WordsWeigher(filtered_words)
        self.weigher.set_state(new_invalid, new_correct, self.discovered_letters, self.unpositioned_letters)
        self.weigher.set_multipliers(invalid=-100, correct=1, discovered=-100, unpositioned=-10)

        choosen_word, accuracy = self.choose_weighty_word(filtered_words, variation_multiplier=True)
        return choosen_word, accuracy, filtered_words

    def choose_word_to_guess(self) -> (str, float, str):
        word_filter = WordsFilter(self.words)
        word_filter.by_invalid_letters(self.invalid_letters)
        word_filter.by_correct_letters(self.correct_letters)
        word_filter.by_discovered_letters(self.discovered_letters)
        word_filter.by_unpositioned_letters(self.unpositioned_letters)
        filtered_words = word_filter.get_filtered()
        if not filtered_words:
            raise Exception("Word not found")

        self.weigher = WordsWeigher(filtered_words)
        self.weigher.set_state(
            self.invalid_letters, self.correct_letters, self.discovered_letters, self.unpositioned_letters)
        self.weigher.set_multipliers(invalid=1, correct=1, discovered=1, unpositioned=1)

        choosen_word, accuracy = self.choose_weighty_word(filtered_words)
        return choosen_word, accuracy, filtered_words

    def choose_round_word(self) -> (str, float, list[str]):
        guessed_word, guess_accuracy, valid_words = self.choose_word_to_guess()
        explore_word, explore_accuracy, _ = self.choose_word_to_discover_letters()

        new_letters = 0
        for letter in explore_word:
            if letter not in self.discovered_letters:
                new_letters += 1

        # @TODO Decision improvements
        # Verify if is last round
        # Save what letters in valid_words are not in self.discovered_letters

        if new_letters > 2 or guess_accuracy < 10:
            return explore_word, explore_accuracy, valid_words
        return guessed_word, guess_accuracy, valid_words

    def play_round(self) -> (str, float, list[str]):
        if not len(self.game_rounds):
            choosen_word, accuracy, _ = self.choose_word_to_discover_letters()
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
