# bot.py

import requests
import random
import time
import sys

class Bot:
    def __init__(self, name: str | None):
        self.name = name or self.generate_name()
        self.skill = random.choice(["novice", "competent", "expert"])


    @classmethod
    def create(cls):
        """Factory method to generate a bot with random name."""
        return cls(None)  # Create bot with random name


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

    # noinspection PyMethodMayBeStatic
    def thinking_animation(self):
        for _ in range(3):
            time.sleep(0.5)
            print(". ", end="")
            sys.stdout.flush()
        time.sleep(1)