from autotermooo.solver import TermoooSolver


class AutoTermooo:
    def __init__(self):
        self.solver = TermoooSolver("game_words/pt_br.txt")

    @staticmethod
    def yes_or_not_input():
        while True:
            user_input = input("").lower()
            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            else:
                print("Invalid response")

    def play_game(self):
        while True:
            suggested_word, accuracy, good_options = self.solver.play_round()
            print(f"The suggested word is '{suggested_word}' with {accuracy}% accuracy")

            print(f"Do you accept the suggestion '{suggested_word}'? Yes(Y) or No(N)")
            sugestion_accepted = self.yes_or_not_input()
            if sugestion_accepted:
                choosen_word = suggested_word
            else:
                print("Want to see other good options? Yes(Y) or No(N)")
                show_options = self.yes_or_not_input()
                if show_options:
                    print(f"All options: {good_options}")

                choosen_word = input("Type the chosen word: ").lower()

            status = input("Enter what is left on your screen, 0 for INVALID, 1 for UNPOSITIONED or 2 for CORRECT"
                           "(No space or enter between characters): ")
            if status == "22222":
                break

            status = [int(letter_status) for letter_status in list(status)]
            self.solver.game_rounds.append((choosen_word, status))
