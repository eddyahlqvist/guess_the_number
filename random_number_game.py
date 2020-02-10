# Coded by Eddy Ahlqvist - 2020

# Import the random library to be able to create a random number
import random

# Create a random number between 1 and 100 and assign it to the variable 'random_number'
random_number = random.randint(1, 100)

# Gives a starting value to the 'guess' variable to avoid errors in the first input stage using characters or decimals
guess = 0

# Keeps track on how many guesses the user will input before finding the correct number
tries = 0

# Stores the user name from an input
user_name = str(input("Enter your name: "))

# Sets the 'win condition'. Used in the while loop below
win = False

while not win:  # Same as while win == False
    try:
        guess = int(input("Guess on a number between 1 and 100: "))
        tries += 1
        if guess > 100 or guess < 1:
            tries -= 1
            raise ValueError
    except ValueError:
        print("Incorrect input. Please try again.")
        continue
    if guess == random_number:
        print("Congratulations " + user_name + "! " + str(random_number) + " was the correct number :)")
        if tries > 1:
            print("You guessed " + str(tries) + " times")
        else:
            print("OMG FIRST TRY! YOU ARE AMAZING!!!")
        win = True
    elif guess < random_number:
        print("To low, try again")
    else:
        print("To high, try again")

f = open("highscore.txt", "a")
f.write(str(tries) + " tries. User: " + user_name + "\n")
f.close()

f = open("highscore.txt", "r")
scores = []
for line in f.readlines():
    scores.append([line])
scores.sort()
f.close()

# with open("highscore.txt", "w") as f:
#     f.write(str(scores) + "\n")
# f.close()

print(scores)

# f = open("highscore.txt", "r")
# print(f.read())
# f.close()
