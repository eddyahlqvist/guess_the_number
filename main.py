# Coded by Eddy Ahlqvist - 2020
# Modified in 2025 for learning purposes
# main.py

import random


from bot import Bot

class GuessTheNumberGame:
    RANGE_SETTINGS = {'easy': 50, 'medium': 100, 'hard': 1000}

    def __init__(self):
        self.user_name: str | None = None
        self.score: int = 0 # score not yet implemented

    def menu(self):
        while True:
            options = {'1': 'Play game', '2': 'Bot play'}
            if self.user_name is not None:
                options['3'] = 'Change name'
            options['q'] = 'Quit'

            print("\nMenu")
            for key, label in options.items():
                print(f"{key}. {label}")

            choice = input("Choose an option: ").strip().lower()

            if choice == "1":
                difficulty_range = self.set_range()
                if difficulty_range:
                    self.play_game(difficulty_range)
                else:
                    continue
            elif choice == "2":
                self.bot_soloplay()
            elif self.user_name and choice == "3":
                self.change_name()
            elif choice in ("q", "quit", "exit"):
                print("Goodbye!")
                break
            else:
                visible_nums = ", ".join(key for key in options if key.isdigit())
                print(f"Please enter {visible_nums}, or 'q' to quit.")

    def set_range(self):
        while True:
            print("\nRange difficulty settings: ")
            print(f"1. Easy (1–{self.RANGE_SETTINGS['easy']})")
            print(f"2. Medium (1–{self.RANGE_SETTINGS['medium']})")
            print(f"3. Hard (1–{self.RANGE_SETTINGS['hard']})")
            print("4. Back to menu")
            inp = input("Choose range difficulty: ")
            if inp == "1":
                return {'name': 'easy', 'range': self.RANGE_SETTINGS['easy']}
            elif inp == "2":
                return {'name': 'medium', 'range': self.RANGE_SETTINGS['medium']}
            elif inp == "3":
                return {'name': 'hard', 'range': self.RANGE_SETTINGS['hard']}
            elif inp == "4":
                return None
            else:
                print("Invalid choice, try again.")

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
                print(f"Congratulations {self.user_name}! {random_number} was the correct number.")
                if tries > 1:
                    print(f"You guessed {tries} times on the following numbers: "
                          f"\n{used_numbers} on {difficulty_range['name']} difficulty.")
                else:
                    print("Very impressive! You beat the game on the first try! ")
                break
            elif guess < random_number:
                self.print_feedback("low")
            else:
                self.print_feedback("high")

    def bot_soloplay(self):
        menu_choice = self.show_bot_menu()
        if menu_choice is None:
            return  # user went back to main menu

        difficulty_range = self.set_range()
        if not difficulty_range:
            return  # user backed out

        bot = Bot.create()
        if bot is None:
            return

        print("Inviting a random bot ", end='')
        bot.thinking_animation()

        random_number = random.randint(1, difficulty_range['range'])
        used_numbers = []
        tries = 0
        high_num = difficulty_range['range']
        low_num = 1
        bot_guess = bot.guess(low_num, high_num)

        print(f"\n{bot.name} has joined the session.")
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


    @staticmethod
    def show_bot_menu():
        while True:
            bot_menu_options = {'1': 'Random bots', '2': 'Special bots', '3': 'Back to main menu'}
            print("\nBot menu")
            for key, label in bot_menu_options.items():
                print(f"{key}. {label}")
            choice = input("Choose an option: ").strip().lower()
            if choice == "1":
                return "random"
            elif choice == "2":
                print("Not yet implemented")
            elif choice == "3":
                return None
            else:
                print("Invalid choice, try again.")


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


    @staticmethod
    def print_feedback(direction: str):
        """Prints a feedback message based on guess direction."""
        if direction == "low":
            print("Too low, try again.")
        elif direction == "high":
            print("Too high, try again.")
        else:
            print(direction)  # fallback for unexpected usage


if __name__ == "__main__":
    game = GuessTheNumberGame()
    game.menu()