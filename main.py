# Coded by Eddy Ahlqvist - 2020
# Modified in 2025 for learning purposes

import random
import time
import sys

random_number = random.randint(1, 100)
tries = 0

user_name = str(input("Enter your name or Bot if you want to enable Bot-mode: "))
if user_name == "Bot" or user_name == "bot" or user_name == "b":
    bot_mode = True
    tries += 1
else:
    bot_mode = False

used_numbers = []
win = False
bot_guess = random.randint(1, 100)

# Starting values for the bot guess range
high_num = 100
low_num = 1

# Below while loop is all about the bot
while bot_mode:
    print("--==<< Bot mode >>==-- \nBot is now guessing on a number between " + str(low_num) + " and " + str(high_num))
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
        print("Congratulations " + user_name + "! " + str(random_number) + " was the correct number :)")
        if tries > 1:
            print("You guessed " + str(tries) + " times on the following numbers: " + str(used_numbers))
        else:
            print("OMG FIRST TRY! Cheating bots everywhere...")
        bot_mode = False
        win = True
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

# Below while loop is all about the player
while not win:
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
        print("Congratulations " + user_name + "! " + str(random_number) + " was the correct number :)")
        if tries > 1:
            print("You guessed " + str(tries) + " times on the following numbers: " + str(used_numbers))
        else:
            print("OMG FIRST TRY! YOU ARE AMAZING!!!")
        win = True
    elif guess < random_number:
        print("To low, try again")
    else:
        print("To high, try again")

# Below is High Score stuff

# f = open("highscore.txt", "a")
# f.write(str(tries) + " tries. User: " + user_name + "\n")
# f.close()
#
# f = open("highscore.txt", "r")
# print(f.read())
# f.close()
