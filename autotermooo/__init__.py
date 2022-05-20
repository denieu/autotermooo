from enum import Enum


class LetterStatusEnum(Enum):
    INVALID = 0
    WRONG_POSITION = 1
    CORRECT = 2


class AutoTermooo:
    def __init__(self, words_file: str):
        self.words_file: str = words_file
        self.words: list[str] = []
        self.letters_weight: dict[str, int] = {}

        self.rounds: list[list[tuple[str, LetterStatusEnum]]] = [
            [("m", LetterStatusEnum.WRONG_POSITION), ("e", LetterStatusEnum.WRONG_POSITION),
             ("i", LetterStatusEnum.WRONG_POSITION), ("a", LetterStatusEnum.INVALID), ("o", LetterStatusEnum.INVALID)],

            [("r", LetterStatusEnum.INVALID), ("i", LetterStatusEnum.CORRECT),
             ("m", LetterStatusEnum.CORRECT), ("e", LetterStatusEnum.CORRECT), ("i", LetterStatusEnum.WRONG_POSITION)],

            [("t", LetterStatusEnum.INVALID), ("i", LetterStatusEnum.CORRECT),
             ("m", LetterStatusEnum.CORRECT), ("e", LetterStatusEnum.CORRECT), ("s", LetterStatusEnum.INVALID)],

            [("l", LetterStatusEnum.INVALID), ("i", LetterStatusEnum.CORRECT),
             ("m", LetterStatusEnum.CORRECT), ("e", LetterStatusEnum.CORRECT), ("m", LetterStatusEnum.WRONG_POSITION)],

            # [("g", LetterStatusEnum.INVALID), ("r", LetterStatusEnum.CORRECT),
            #  ("e", LetterStatusEnum.CORRECT), ("v", LetterStatusEnum.CORRECT), ("e", LetterStatusEnum.CORRECT)],

            # [("s", LetterStatusEnum.WRONG_POSITION), ("a", LetterStatusEnum.CORRECT),
            #  ("c", LetterStatusEnum.CORRECT), ("a", LetterStatusEnum.CORRECT), ("s", LetterStatusEnum.CORRECT)]
        ]

        self.read_words()
        self.generate_letters_weight()
        print("words = ", self.words)
        print("letters weight = ", self.letters_weight)

    def read_words(self):
        with open(self.words_file) as words_fp:
            self.words = words_fp.read().splitlines()

    def generate_letters_weight(self):
        for word in self.words:
            for letter in list(word):
                if letter not in self.letters_weight:
                    self.letters_weight[letter] = 0
                self.letters_weight[letter] += 1

        sorted_letters = sorted(self.letters_weight.items(), key=lambda x: x[1])
        for idx, letter in enumerate(sorted_letters):
            self.letters_weight[letter[0]] = idx + 1

    def get_letter_weight(self, letter) -> int:
        return self.letters_weight[letter]

    def get_word_weight(self, word) -> int:
        weight = 0
        for letter in list(word):
            weight += self.get_letter_weight(letter)
        return weight

    def get_first_word_weight(self, word) -> int:
        weight = 0
        letters = []
        for letter in list(word):
            if letter in letters:
                return 0
            weight += self.get_letter_weight(letter)
            letters += letter
        return weight

    def choose_first_word(self) -> str:
        choosen_word = self.words[0]
        max_weight = self.get_first_word_weight(choosen_word)
        for word in self.words[1:]:
            new_weigth = self.get_first_word_weight(word)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word
        return choosen_word

    def choose_word_with_correct_letters(self, correct_letters):
        ok_words = []
        for word in self.words:
            word = list(word)
            skip_word = False
            for idx, letter in enumerate(correct_letters):
                if letter is not None:
                    if word[idx] != letter:
                        skip_word = True
                        break
            if skip_word:
                continue
            word = "".join(word)
            ok_words.append(word)
        return ok_words

    def choose_round_word(self, invalid_letters, wrong_position_letters, correct_letters):
        ok_words = self.choose_word_with_correct_letters(correct_letters)
        print("ok_words = ", ok_words)
        result_words = []
        for word in ok_words:
            word = list(word)
            skip_word = False

            # Filter word if have a invalid letter
            for invalid_letter in invalid_letters:
                if invalid_letter in word:
                    skip_word = True
                    break
            if skip_word:
                continue

            # Filter word if we have a letter in wrong position
            # Filter words that do not contain already discovered letters
            for idx, position in enumerate(wrong_position_letters):
                for letter in position:
                    if word[idx] == letter:
                        skip_word = True
                        break
                    elif letter not in word:
                        skip_word = True
                        break
            if skip_word:
                continue

            word = "".join(word)
            result_words.append(word)

        print("filteres words = ", result_words)
        if not result_words:
            raise Exception("Não restou nenhuma palavra")

        choosen_word = result_words[0]
        max_weight = self.get_first_word_weight(choosen_word)
        for word in result_words[1:]:
            new_weigth = self.get_word_weight(word)
            if new_weigth > max_weight:
                max_weight = new_weigth
                choosen_word = word
        return choosen_word

    def play_round(self):
        if not len(self.rounds):
            return self.choose_first_word()

        invalid_letters = []
        wrong_position_letters = [[], [], [], [], []]
        correct_letters = [None, None, None, None, None]
        for game_round in self.rounds:
            for idx, position in enumerate(game_round):
                letter, status = position
                if status == LetterStatusEnum.INVALID:
                    invalid_letters += letter
                elif status == LetterStatusEnum.WRONG_POSITION:
                    wrong_position_letters[idx] += letter
                elif status == LetterStatusEnum.CORRECT:
                    correct_letters[idx] = letter

        print("invalid_letters = ", invalid_letters)
        print("wrong_position_letters", wrong_position_letters)
        print("correct_letters", correct_letters)

        return self.choose_round_word(invalid_letters, wrong_position_letters, correct_letters)


if __name__ == '__main__':
    test = AutoTermooo('game_words/pt_br.txt')
    result = test.play_round()
    if result:
        print("word = ", result)
        print(f"'{result}' weigth = ", test.get_first_word_weight(result))
