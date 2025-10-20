# Coded by Eddy Ahlqvist - 2020
# Modified in 2025 for learning purposes
# main.py

import random
import math

from bot import Bot

class GuessTheNumberGame:
    RANGE_SETTINGS = {'easy': 50, 'medium': 100, 'hard': 1000}

    def __init__(self):
        self.user_name: str | None = None
        self.score: int = 0


    def menu(self):
        while True:
            options = {'1': 'Play game', '2': 'Bot play'}
            if self.user_name is not None:
                options['3'] = 'Change name'

            print("\nMenu")
            for key, label in options.items():
                print(f"{key}. {label}")
            print("q. Quit")

            # Build list of valid choices dynamically
            valid_choices = list(options.keys())
            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice == "quit":
                print("Goodbye!")
                break
            if choice == "back":
                continue

            actions = {
                '1': self.start_player_game,
                '2': self.bot_soloplay,
                '3': self.change_name
            }

            action = actions.get(choice)
            result = action()

            if result == "quit":
                print("Goodbye!")
                break
            if result == "back":    # For main menu, 'back' = do nothing or re-loop
                continue


    def set_range(self):
        while True:
            options = {
                '1': 'Easy',
                '2': 'Medium',
                '3': 'Hard'
           }
            print("\nRange Options: ")
            for key, label in options.items():
                max_range = self.RANGE_SETTINGS[label.lower()]
                print(f"{key}. {label} (1–{max_range})")
            print("b. Back")
            print("q. Quit")
            valid_choices = list(options.keys())

            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice == "back":
                return None
            if choice == "quit":
                return "quit"

            if choice == "1":
                return {'name': 'easy', 'range': self.RANGE_SETTINGS['easy']}
            elif choice == "2":
                return {'name': 'medium', 'range': self.RANGE_SETTINGS['medium']}
            elif choice == "3":
                return {'name': 'hard', 'range': self.RANGE_SETTINGS['hard']}


    def play_game(self, difficulty_range: dict[str, int | str]) -> None:
        random_number = random.randint(1, difficulty_range['range'])
        used_numbers = []
        tries = 0
        self.ensure_user_name()
        print(f"Game is on! {self.user_name} is playing on {difficulty_range['name']} difficulty.")
        while True:
            try:
                guess = int(input(f"Guess on a number between 1 and {difficulty_range['range']}: "))
                tries += 1
                used_numbers.append(guess)
                if guess > difficulty_range['range'] or guess < 1:
                    tries -= 1
                    used_numbers.pop()
                    raise ValueError
            except ValueError:
                print("Incorrect input. Please try again.")
                continue
            if guess == random_number:
                score, ideal = self.calculate_score(tries, difficulty_range['range'])
                self.score = score
                print(f"Congratulations {self.user_name}! {random_number} was the correct number.")
                print(f"Ideal guesses: {ideal}")
                print(f"Your guesses: {tries}")
                print(f"Your score: {score}/{ideal * 2}")
                if tries > 1:
                    print(f"You guessed on the following numbers: "
                          f"\n{used_numbers} on {difficulty_range['name']} difficulty.")
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
            if menu_choice == "quit":
                return "quit"
            if not menu_choice:
                return None  # back to main menu

            difficulty_range = self.set_range()
            if difficulty_range == "quit":
                return "quit"
            if not difficulty_range:
                continue  # back to bot menu

            break

        bot = Bot.create()
        if bot is None:
            return None

        print("Inviting a random bot ", end='')
        bot.thinking_animation()

        random_number = random.randint(1, difficulty_range['range'])
        used_numbers = []
        tries = 0
        high_num = difficulty_range['range']
        low_num = 1
        bot_guess = bot.guess(low_num, high_num)

        print(f"\n{bot.name} ({bot.skill.capitalize()} bot) has joined the session.")
        print(f"--==<< Bot mode >>==-- \n{bot.name} is now guessing on a number between {low_num} and {high_num}")

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
                print(f"--==<< Bot mode >>==-- \n{bot.name} is smiling from ear to ear when placing the final guess!")
                bot_guess = high_num
                continue
            elif high_num - low_num == 1:
                print(f"--==<< Bot mode >>==-- \n{bot.name} has narrowed it down to either {low_num} or {high_num}!")
            else:
                self.print_feedback(direction)
                print(f"--==<< Bot mode >>==-- \n{bot.name} is now guessing on a number between {low_num} and {high_num}")


    def show_bot_menu(self):
        while True:
            options = {
                '1': ('Random bots', 'random'),
                '2': ('Special bots', 'special') # placeholder, creates a standard random bot atm
            }

            print("\nBot menu")
            for key, (label, _) in options.items():
                print(f"{key}. {label}")
            print("b. Back")
            print("q. Quit")

            valid_choices = list(options.keys())
            choice = self.get_choice("Choose an option: ", valid_choices)

            if choice == "quit":
                return "quit"
            if choice == "back":
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
        if difficulty_range == "quit":
            return "quit"
        if not difficulty_range:
            return "back"
        return self.play_game(difficulty_range)


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
    def get_choice(prompt: str, valid_options: list[str]) -> str:
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
                return "quit"
            if choice in ("b", "back"):
                return "back"
            if choice in valid_options:
                return choice

            print("Invalid choice, try again.")

    @staticmethod
    def calculate_score(tries: int, range_size: int) -> tuple[int, int]:
        ideal = math.ceil(math.log2(range_size))
        score = max(0, (ideal * 2) - tries)
        return score, ideal


if __name__ == "__main__":
    game = GuessTheNumberGame()
    game.menu()