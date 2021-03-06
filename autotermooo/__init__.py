from autotermooo.solver import TermoooSolver, INVALID, UNPOSITIONED, CORRECT


class AutoTermooo:
    def __init__(self):
        self.solver = TermoooSolver("game_words/pt_br.txt")

    @staticmethod
    def yes_or_not_input() -> bool:
        while True:
            user_input = input("").lower()
            if user_input == "y":
                return True
            elif user_input == "n":
                return False
            else:
                print("Invalid response")

    @staticmethod
    def solve_status(word: str, status: list[int]) -> list[int]:
        word = list(word)
        for idx, letter_status in enumerate(status):
            if letter_status not in [UNPOSITIONED, CORRECT]:
                continue

            for recursive_idx, recursive_letter_status in enumerate(status):
                if idx != recursive_idx and word[idx] == word[recursive_idx]:
                    if recursive_letter_status == INVALID:
                        status[recursive_idx] = UNPOSITIONED
                        print(f"Solving letter {word[idx]} status, from INVALID to UNPOSITIONED")
        return status

    def play_game(self) -> None:
        while True:
            suggested_word, accuracy, good_options = self.solver.play_round()
            print(f"All options: {good_options}")
            print(f"Accuracy: {accuracy}%")
            print(f"Suggested word: {suggested_word}")

            print(f"Do you accept the suggestion '{suggested_word}'? Yes(Y) or No(N)")
            sugestion_accepted = self.yes_or_not_input()
            choosen_word = suggested_word if sugestion_accepted else input("Type the chosen word: ").lower()

            status = input("Enter the result, 0 for INVALID, 1 for UNPOSITIONED or 2 for CORRECT: ")
            if status == "22222":
                break

            status = [int(letter_status) for letter_status in list(status)]
            status = self.solve_status(choosen_word, status)
            self.solver.game_rounds.append((choosen_word, status))
