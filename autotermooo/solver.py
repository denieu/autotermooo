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

    def read_words(self, words_file: str):
        with open(words_file) as words_fp:
            self.words = words_fp.read().splitlines()

    def generate_letter_weight(self):
        for word in self.words:
            for letter in list(word):
                if letter not in self.letter_weight:
                    self.letter_weight[letter] = 0
                self.letter_weight[letter] += 1

        sorted_letters = sorted(self.letter_weight.items(), key=lambda x: x[1])
        for idx, letter in enumerate(sorted_letters):
            self.letter_weight[letter[0]] = idx + 1

    def get_letter_weight(self, letter) -> int:
        return self.letter_weight[letter]

    def get_word_weight(self, word, consider_duplicates=True, variation_multiplier=False) -> int:
        weight = 0
        letters = []
        for letter in list(word):
            if letter not in letters or consider_duplicates:
                weight += self.get_letter_weight(letter)
            if letter not in letters:
                letters += letter
        if variation_multiplier:
            weight *= len(letters)
        return weight

    def filter_by_correct_letters(self, word):
        for idx, letter in enumerate(self.correct_letters):
            if letter is not None:
                if word[idx] != letter:
                    return False
        return True

    def filter_by_invalid_letters(self, word):
        for invalid_letter in self.invalid_letters:
            if invalid_letter in word:
                return False
        return True

    def filter_by_discovered_letters(self, word):
        for discovered_letter in self.discovered_letters:
            if discovered_letter not in word:
                return False
        return True

    def filter_by_unpositioned(self, word):
        for idx, position in enumerate(self.unpositioned_letters):
            for letter in position:
                if word[idx] == letter:
                    return False
        return True

    def choose_best_word(self, words, consider_duplicates=True, variation_multiplier=False):
        choosen_word = words[0]
        max_weight = self.get_word_weight(choosen_word, consider_duplicates, variation_multiplier)
        for word in words[1:]:
            new_weigth = self.get_word_weight(word, consider_duplicates, variation_multiplier)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_round_word(self):
        filtered_words = filter(self.filter_by_invalid_letters, self.words)
        filtered_words = filter(self.filter_by_correct_letters, filtered_words)
        filtered_words = filter(self.filter_by_discovered_letters, filtered_words)
        filtered_words = filter(self.filter_by_unpositioned, filtered_words)
        filtered_words = list(filtered_words)

        if not filtered_words:
            raise Exception("Word not found")

        choosen_word, accuracy = self.choose_best_word(filtered_words)
        if accuracy <= 5:
            choosen_word, accuracy = self.choose_best_word(filtered_words,
                                                           consider_duplicates=False, variation_multiplier=True)
        return choosen_word, accuracy, filtered_words

    def play_round(self):
        if not len(self.game_rounds):
            choosen_word, accuracy = self.choose_best_word(self.words,
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
