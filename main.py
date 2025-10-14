# Coded by Eddy Ahlqvist - 2020
# Modified in 2025 for learning purposes

import random
import time
import sys

def menu():
    while True:
        print("Menu")
        print("1. Play game")
        print("2. Bot play")
        print("3. Quit")
        choice = input("Choose an option: ")
        if choice == "1":
            play_game()
        elif choice == "2":
            bot_soloplay()
        else:
            print("Goodbye!")
            break

def play_game():
    random_number = random.randint(1, 100)
    used_numbers = []
    tries = 0
    user_name = input("Enter your name: ")

    while True:
        try:
            guess = int(input("Guess on a number between 1 and 100: "))
            tries += 1
            used_numbers.append(guess)
            if guess > 100 or guess < 1:
                tries -= 1
                used_numbers.pop()
                raise ValueError
        except ValueError:
            print("Incorrect input. Please try again.")
            continue
        if guess == random_number:
            print(f"Congratulations {user_name}! {random_number} was the correct number.")
            if tries > 1:
                print(f"You guessed {tries} times on the following numbers: {used_numbers}")
            else:
                print("Very impressive! You beat the game on the first try! ")
            break

        elif guess < random_number:
            print("To low, try again")
        else:
            print("To high, try again")

def bot_soloplay():
    random_number = random.randint(1, 100)
    used_numbers = []
    tries = 0
    user_name = "Bot"
    tries += 1
    bot_guess = random.randint(1, 100)

    # Starting values for the bot guess range
    high_num = 100
    low_num = 1

    while True:
        if low_num + 1 == high_num - 1: # to avoid message like guessing between 49 and 49
            print(f"--==<< Bot mode >>==-- \nBot is smiling from ear to ear when placing its final guess!")
        else:
            print(f"--==<< Bot mode >>==-- \nBot is now guessing on a number between {low_num} and {high_num}")
        used_numbers.append(bot_guess)
        print("Guessing", end='')
        sys.stdout.flush()
        for i in range(3):
            time.sleep(0.5)
            print(". ", end='')
            sys.stdout.flush()
        time.sleep(1)
        print(str(bot_guess))

        if bot_guess == random_number:
            print(f"Congratulations {user_name}! {random_number} was the correct number.")
            if tries > 1:
                print(f"The bot guessed {tries} times on the following numbers: {used_numbers}")
            else:
                print("Unbelievable! The bot beat the game on its first try! ")
            break
        elif bot_guess < random_number:
            low_num = bot_guess + 1
            time.sleep(1.5)
            bot_guess = random.randint(bot_guess + 1, high_num)
            print("To low, try again")
            tries += 1
        else:
            high_num = bot_guess - 1
            time.sleep(1.5)
            bot_guess = random.randint(low_num, bot_guess - 1)
            print("To high, try again")
            tries += 1


# Below is High Score stuff

# f = open("highscore.txt", "a")
# f.write(str(tries) + " tries. User: " + user_name + "\n")
# f.close()
#
# f = open("highscore.txt", "r")
# print(f.read())
# f.close()

if __name__ == "__main__":
    menu()