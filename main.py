# Coded by Eddy Ahlqvist - 2020
# Modified in 2025 for learning purposes
# main.py

import random
import math
import os
import json

from bot import Bot
from enum import Enum

class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class SystemCommand(Enum):
    QUIT = "quit"
    BACK = "back"

base_dir = os.path.dirname(os.path.abspath(__file__))
numbergame_path = os.path.join(base_dir, "highscore.json")

class GuessTheNumberGame:
    RANGE_SETTINGS = {
        Difficulty.EASY: 50,
        Difficulty.MEDIUM: 100,
        Difficulty.HARD: 1000
    }

    def __init__(self):
        self.user_name: str | None = None
        self.score: int = 0
        self.difficulty = Difficulty.EASY
        self.highscore: list[dict] = []


    def menu(self):
        try:
            with open(numbergame_path, "r") as f:
                self.highscore = json.load(f)
        except FileNotFoundError:
            self.highscore: list[dict] = []

        while True:
            options = {'1': 'Play game', '2': 'Bot play', '3': 'High Scores'}
            if self.user_name is not None:
                options['4'] = 'Change name'

            print("\nMenu")
            for key, label in options.items():
                print(f"{key}. {label}")
            print(f"q. {SystemCommand.QUIT.value.capitalize()}")

            # Build list of valid choices dynamically
            valid_choices = list(options.keys())
            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice is SystemCommand.QUIT:
                print("Goodbye!")
                break
            if choice is SystemCommand.BACK:
                continue

            actions = {
                '1': self.start_player_game,
                '2': self.bot_soloplay,
                '3': self.show_highscores,
                '4': self.change_name
            }

            action = actions.get(choice)
            result = action()

            if result is SystemCommand.QUIT:
                print("Goodbye!")
                break
            if result is SystemCommand.BACK:    # For main menu, 'back' = do nothing or re-loop
                continue


    def set_range(self):
        while True:
            options = {
                '1': Difficulty.EASY,
                '2': Difficulty.MEDIUM,
                '3': Difficulty.HARD
           }
            print("\nRange Options: ")
            for key, label in options.items():
                max_range = self.RANGE_SETTINGS[label]
                print(f"{key}. {label.value.capitalize()} (1–{max_range})")
            print(f"b. {SystemCommand.BACK.value.capitalize()}")
            print(f"q. {SystemCommand.QUIT.value.capitalize()}")
            valid_choices = list(options.keys())

            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice is SystemCommand.QUIT:
                return SystemCommand.QUIT
            if choice is SystemCommand.BACK:
                return None

            if choice == "1":
                return Difficulty.EASY
            elif choice == "2":
                return Difficulty.MEDIUM
            elif choice == "3":
                return Difficulty.HARD


    def play_game(self) -> None:
        max_range = self.RANGE_SETTINGS[self.difficulty]
        random_number = random.randint(1, max_range)
        used_numbers = []
        tries = 0
        self.ensure_user_name()
        print(f"Game is on! {self.user_name} is playing on {self.difficulty.value} difficulty.")
        while True:
            try:
                guess = int(input(f"Guess on a number between 1 and {max_range}: "))
                tries += 1
                used_numbers.append(guess)
                if guess > max_range or guess < 1:
                    tries -= 1
                    used_numbers.pop()
                    raise ValueError
            except ValueError:
                print("Incorrect input. Please try again.")
                continue
            if guess == random_number:
                score, ideal = self.calculate_score(tries, max_range)
                self.score = score
                print(f"Congratulations {self.user_name}! {random_number} was the correct number.")
                print(f"Ideal guesses: {ideal}")
                print(f"Your guesses: {tries}")
                print(f"Your score: {score}/{ideal * 2}")
                self.highscore.append({
                    "name": self.user_name,
                    "score": score
                })
                self.highscore.sort(key=lambda x: x["score"], reverse=True)
                self.highscore = self.highscore[:10]  # keep only top 10
                self.save_highscore(self.highscore)
                if tries > 1:
                    print(f"You guessed on the following numbers: "
                          f"\n{used_numbers} on {self.difficulty.value} difficulty.")
                else:
                    print("Very impressive! You beat the game on the first try! ")
                break
            elif guess < random_number:
                self.print_feedback("low")
            else:
                self.print_feedback("high")

    def bot_soloplay(self):
        while True:
            menu_choice = self.show_bot_menu()
            if menu_choice is SystemCommand.QUIT:
                return SystemCommand.QUIT
            if not menu_choice:
                return None  # back to main menu

            difficulty_range = self.set_range()
            if difficulty_range is SystemCommand.QUIT:
                return SystemCommand.QUIT
            if not difficulty_range:
                continue  # back to bot menu
            self.difficulty = difficulty_range
            break

        bot = Bot.create()
        if bot is None:
            return None

        print("Inviting a random bot ", end='')
        bot.thinking_animation()

        max_range = self.RANGE_SETTINGS[self.difficulty]
        random_number = random.randint(1, max_range)
        used_numbers = []
        tries = 0
        high_num = max_range
        low_num = 1
        bot_guess = bot.guess(low_num, high_num)

        print(f"\n{bot.name} ({bot.skill.value.capitalize()} bot) has joined the session.")
        print(f"--==<< Bot mode >>==-- \n{bot.react_normal(low_num, high_num)}")

        while True:
            tries += 1
            used_numbers.append(bot_guess)
            print("Guessing ", end='')
            bot.thinking_animation()
            print(str(bot_guess))

            if bot_guess < random_number:
                direction = "low"
                low_num = bot_guess + 1
            elif bot_guess > random_number:
                direction = "high"
                high_num = bot_guess - 1
            else:
                print(f"Congratulations {bot.name}! {random_number} was the correct number.")
                if tries > 1:
                    print(f"{bot.name} guessed {tries} times on the following numbers: {used_numbers}")
                else:
                    print(f"Unbelievable! {bot.name} beat the game on the first try!")
                break


            bot_guess = bot.guess(low_num, high_num)

            # Shared feedback logic
            if low_num >= high_num:
                print(f"--==<< Bot mode >>==-- \n{bot.react_final()}")
                bot_guess = high_num
                continue
            elif high_num - low_num == 1:
                print(f"--==<< Bot mode >>==-- \n{bot.react_narrow(low_num, high_num)}")
            else:
                self.print_feedback(direction)
                print(f"--==<< Bot mode >>==-- \n{bot.react_normal(low_num, high_num)}")


    def show_bot_menu(self):
        while True:
            options = {
                '1': ('Random bots', 'random'),
                '2': ('Special bots', 'special') # placeholder, creates a standard random bot atm
            }

            print("\nBot menu")
            for key, (label, _) in options.items():
                print(f"{key}. {label}")
            print(f"b. {SystemCommand.BACK.value.capitalize()}")
            print(f"q. {SystemCommand.QUIT.value.capitalize()}")

            valid_choices = list(options.keys())
            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice is SystemCommand.QUIT:
                return SystemCommand.QUIT
            if choice is SystemCommand.BACK:
                return None

            return options[choice][1]


    def change_name(self):
        old_name = self.user_name
        new_name = input("Enter your new name: ").strip()
        if not new_name:
            print("Name can't be empty. Keeping current name.")
        elif new_name == old_name:
            print("That's already your name.")
        else:
            self.user_name = new_name
            print(f"{old_name} has left the building! You are now known as {new_name}.")


    def ensure_user_name(self):
        if self.user_name is None:
            self.user_name = input("Enter your name: ").strip()
            print(f"Welcome, {self.user_name}!")
        else:
            print(f"Welcome back, {self.user_name}!")
        return self.user_name


    def start_player_game(self):
        difficulty_range = self.set_range()
        if difficulty_range is SystemCommand.QUIT:
            return SystemCommand.QUIT
        if not difficulty_range:
            return SystemCommand.BACK
        self.difficulty = difficulty_range
        return self.play_game()

    @staticmethod
    def print_feedback(direction: str):
        """Prints a feedback message based on guess direction."""
        if direction == "low":
            print("Too low, try again.")
        elif direction == "high":
            print("Too high, try again.")
        else:
            print(direction)  # fallback for unexpected usage

    @staticmethod
    def get_choice(prompt: str, valid_options: list[str]) -> SystemCommand | str:
        """
        Ask the user for a choice, normalize input, and handle standard commands.
        Returns:
            - the chosen option (e.g. "1", "2", "medium")
            - "quit" if user wants to quit the program
            - "back" if user wants to go back to previous menu
        """
        while True:
            choice = input(prompt).strip().lower()

            if choice in ("q", "quit", "exit"):
                return SystemCommand.QUIT
            if choice in ("b", "back"):
                return SystemCommand.BACK
            if choice in valid_options:
                return choice

            print("Invalid choice, try again.")

    @staticmethod
    def calculate_score(tries: int, range_size: int) -> tuple[int, int]:
        ideal = math.ceil(math.log2(range_size))
        score = max(0, (ideal * 2) - tries)
        return score, ideal


    def show_highscores(self):
        if not self.highscore:
            print("\nNo highscores yet!")
            return

        print("\n--==<< High Scores >>==--")
        for i, entry in enumerate(self.highscore, start=1):
            print(f"{i}. {entry['name']}: {entry['score']}")


    @staticmethod
    def save_highscore(highscore: list[dict]):
        try:
            with open(numbergame_path, "w") as f:
                json.dump(highscore, f, indent=4)
        except Exception as e:
            print(f"Error saving highscore: {e}")


if __name__ == "__main__":
    game = GuessTheNumberGame()
    game.menu()