# Coded by Eddy Ahlqvist - 2020

# Import the random library to be able to create a random number
import random

# Import time library for calming down the bot a bit
import time

# Need sys to flush in the bot stream
import sys

# Create a random number between 1 and 100 and assign it to the variable 'random_number'
random_number = random.randint(1, 100)

# Keeps track on how many guesses the user will input before finding the correct number
tries = 0

# Stores the user name from an input or turn on bot mode
user_name = str(input("Enter your name or Bot if you want to enable Bot-mode: "))
if user_name == "Bot" or user_name == "bot" or user_name == "b":
    bot_mode = True
    tries += 1
else:
    bot_mode = False

# Stores all the guessed numbers for display when the game is finished
used_numbers = []

# Sets the 'win condition'. Used in the while loop below
win = False

# Variable for random bot guess
bot_guess = random.randint(1, 100)

high_num = 100
low_num = 0

while bot_mode:
    print("--==<< Bot mode >>==-- \nBot is now guessing on a number between 1 and 100: ")
    used_numbers.append(bot_guess)
    print("Guessing", end='')
    sys.stdout.flush()
    time.sleep(0.8)
    print(".", end='')
    sys.stdout.flush()
    time.sleep(0.8)
    print(".", end='')
    sys.stdout.flush()
    time.sleep(0.8)
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
        tries += 1
    else:
        high_num = bot_guess - 1
        time.sleep(1.5)
        bot_guess = random.randint(low_num, bot_guess - 1)
        tries += 1

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

# f = open("highscore.txt", "a")
# f.write(str(tries) + " tries. User: " + user_name + "\n")
# f.close()
#
# f = open("highscore.txt", "r")
# print(f.read())
# f.close()
