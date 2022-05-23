from autotermooo.solver import TermoooSolver


class AutoTermooo:
    def __init__(self):
        self.solver = TermoooSolver("game_words/pt_br.txt")

    def play_game(self):
        while True:
            choosen_word, accuracy, options = self.solver.play_round()
            print(f"The best word is '{choosen_word}' with {accuracy}% accuracy, all options = {options}")

            typed_word = input("Type the chosen word: ")
            status = input("Enter what is left on your screen, 0 for INVALID, 1 for WRONG_POSITION or 2 for CORRECT"
                           "(No space or enter between characters): ")

            status = [int(letter_status) for letter_status in list(status)]
            self.solver.game_rounds.append((typed_word, status))
            print("")
