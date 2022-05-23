INVALID = 0
WRONG_POSITION = 1
CORRECT = 2


class AutoTermooo:
    def __init__(self, words_file: str):
        self.words: list[str] = []
        self.letter_weight: dict[str, int] = {}

        self.game_rounds: list[tuple[str, list[int]]] = []

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

    def get_word_weight_with_fewer_repeated_letters(self, word) -> int:
        weight = 0
        letters = []
        for letter in list(word):
            if letter in letters:
                return 0
            weight += self.get_letter_weight(letter)
            letters += letter
        return weight

    def get_word_weight(self, word) -> int:
        weight = 0
        for letter in list(word):
            weight += self.get_letter_weight(letter)
        return weight

    @staticmethod
    def filter_words_with_correct_letters(words, correct_letters):
        filtered_words = []
        for word in words:
            word = list(word)
            skip_word = False
            for idx, letter in enumerate(correct_letters):
                if letter is not None:
                    if word[idx] != letter:
                        skip_word = True
            if skip_word:
                continue
            word = "".join(word)
            filtered_words.append(word)
        return filtered_words

    @staticmethod
    def filter_words_without_invalid_letters(words, invalid_letters):
        filtered_words = []
        for word in words:
            word = list(word)
            skip_word = False
            for invalid_letter in invalid_letters:
                if invalid_letter in word:
                    skip_word = True
            if skip_word:
                continue
            word = "".join(word)
            filtered_words.append(word)
        return filtered_words

    @staticmethod
    def filter_words_without_discovered_letters(words, discovered_letters):
        filtered_words = []
        for word in words:
            word = list(word)
            skip_word = False
            for discovered_letter in discovered_letters:
                if discovered_letter not in word:
                    skip_word = True
            if skip_word:
                continue
            word = "".join(word)
            filtered_words.append(word)
        return filtered_words

    @staticmethod
    def filter_words_with_letters_in_wrong_position(words, wrong_position_letters):
        filtered_words = []
        for word in words:
            word = list(word)
            skip_word = False
            for idx, position in enumerate(wrong_position_letters):
                for letter in position:
                    if word[idx] == letter:
                        skip_word = True
            if skip_word:
                continue
            word = "".join(word)
            filtered_words.append(word)
        return filtered_words

    def choose_best_word_with_fewer_repeated_letters(self, words):
        choosen_word = words[0]
        max_weight = self.get_word_weight_with_fewer_repeated_letters(choosen_word)
        for word in words[1:]:
            new_weigth = self.get_word_weight_with_fewer_repeated_letters(word)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_best_word(self, words):
        choosen_word = words[0]
        max_weight = self.get_word_weight(choosen_word)
        for word in words[1:]:
            new_weigth = self.get_word_weight(word)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word

        accuracy = round(1 / len(words) * 100, 2)
        return choosen_word, accuracy

    def choose_round_word(self, invalid_letters, correct_letters, discovered_letters, wrong_position_letters):
        filtered_words = self.filter_words_without_invalid_letters(self.words, invalid_letters)
        filtered_words = self.filter_words_with_correct_letters(filtered_words, correct_letters)
        filtered_words = self.filter_words_without_discovered_letters(filtered_words, discovered_letters)
        filtered_words = self.filter_words_with_letters_in_wrong_position(filtered_words, wrong_position_letters)

        if not filtered_words:
            raise Exception("Word not found")

        choosen_word, accuracy = self.choose_best_word(filtered_words)
        if accuracy <= 5:
            choosen_word, accuracy = self.choose_best_word_with_fewer_repeated_letters(filtered_words)
        return choosen_word, accuracy, filtered_words

    def play_round(self):
        if not len(self.game_rounds):
            choosen_word, accuracy = self.choose_best_word_with_fewer_repeated_letters(self.words)
            return choosen_word, accuracy, self.words

        invalid_letters = []
        correct_letters = [None, None, None, None, None]
        discovered_letters = []
        wrong_position_letters = [[], [], [], [], []]

        for letters, letters_status in self.game_rounds:
            letters = list(letters)

            for idx, letter_status in enumerate(letters_status):
                letter = letters[idx]

                if letter_status == INVALID:
                    if letter not in invalid_letters:
                        invalid_letters.append(letter)
                elif letter_status == WRONG_POSITION:
                    if letter in invalid_letters:
                        raise Exception(f"The letter {letter},"
                                        f" was defined as WRONG POSITION but it had already been defined as INVALID")
                    wrong_position_letters[idx] += letter
                    if letter not in discovered_letters:
                        discovered_letters.append(letter)
                elif letter_status == CORRECT:
                    correct_letters[idx] = letter
                    if letter not in discovered_letters:
                        discovered_letters.append(letter)
                else:
                    raise Exception(f"Invalid letter {letter} status, round {''.join(letters)}")

        choice, accuracy, options = self.choose_round_word(invalid_letters, correct_letters,
                                                           discovered_letters, wrong_position_letters)
        return choice, accuracy, options

    def play_game(self):
        while True:
            choosen_word, accuracy, options = self.play_round()
            print(f"The best word is '{choosen_word}' with {accuracy}% accuracy, all options = {options}")

            typed_word = input("Type the chosen word: ")
            status = input("Enter what is left on your screen, 0 for INVALID, 1 for WRONG_POSITION or 2 for CORRECT"
                           "(No space or enter between characters): ")

            status = [int(letter_status) for letter_status in list(status)]
            self.game_rounds.append((typed_word, status))
            print("")


if __name__ == '__main__':
    autotermooo = AutoTermooo('game_words/pt_br.txt')
    autotermooo.play_game()
