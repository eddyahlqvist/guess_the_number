# bot.py

import requests
import random
import time
import sys

class Bot:
    def __init__(self, name: str | None, skill: str):
        self.name = name or self.generate_name()
        self.skill = skill


    @classmethod
    def create(cls):
        """Factory method to generate a bot with selected skill and random name."""
        skill = cls.select_skill()  # Ask user for bot skill
        if skill is None:
            return None  # User backed out
        return cls(None, skill)  # Create bot with random name


    @staticmethod
    def select_skill():
        while True:
            print("\nBot skill settings: ")
            print("1. Novice")
            print("2. Competent")
            print("3. Expert")
            print("4. Back to menu")
            inp = input("Choose a skill level: ")
            if inp == "1":
                return "novice"
            elif inp == "2":
                return "competent"
            elif inp == "3":
                return "expert"
            elif inp == "4":
                return None
            else:
                print("Invalid choice, try again.")


    @staticmethod
    def generate_name() -> str:
        try:
            response = requests.get("https://randomuser.me/api/?inc=name&noinfo", timeout=5)
            response.raise_for_status()
            data = response.json()
            user_data = data["results"][0]["name"]
            return f"{user_data['title'].capitalize()} {user_data['last'].capitalize()}"
        except (requests.RequestException, KeyError, IndexError, ValueError):
            fallback_names = ["HarryBotter", "Glitch", "404", "Mr. Logic", "Mr. Botastic"]
            return random.choice(fallback_names)


    def guess(self, low: int, high: int) -> int:
        """Return the next guess based on skill level."""
        if self.skill == "novice":
            return random.randint(low, high)
        elif self.skill == "competent":
            mid = (low + high) // 2
            range_size = high - low
            max_dev = max(1, range_size // 10)
            deviation = random.randint(-max_dev, max_dev)
            return max(low, min(high, mid + deviation))
        elif self.skill == "expert":
            return (low + high) // 2
        else:
            raise ValueError(f"Unknown bot skill: {self.skill}")


    def thinking_animation(self):
        for _ in range(3):
            time.sleep(0.5)
            print(". ", end="")
            sys.stdout.flush()
        time.sleep(1)