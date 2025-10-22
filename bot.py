# bot.py

import requests, random, time, sys
from enum import Enum


class Skill(Enum):
    NOVICE = "novice"
    COMPETENT = "competent"
    EXPERT = "expert"


class Bot:
    def __init__(self, name: str | None):
        self.name = name or self.generate_name()
        self.skill = random.choice(list(Skill))


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
        if self.skill is Skill.NOVICE:
            return random.randint(low, high)
        elif self.skill is Skill.COMPETENT:
            mid = (low + high) // 2
            range_size = high - low
            max_dev = max(1, range_size // 10)
            deviation = random.randint(-max_dev, max_dev)
            return max(low, min(high, mid + deviation))
        elif self.skill is Skill.EXPERT:
            return (low + high) // 2
        else:
            raise ValueError(f"Unknown bot skill: {self.skill}")


    def react_normal(self, low: int, high: int) -> str:
        lines = [
            f"{self.name} is now guessing on a number between {low} and {high}.",
            f"{self.name} scans the range from {low} to {high} with curiosity.",
            f"{self.name} examines the numbers between {low} and {high} carefully.",
            f"{self.name} is thinking out loud: 'Somewhere between {low} and {high}…'",
            f"{self.name} narrows their eyes, focusing on the range {low}–{high}.",
            f"{self.name} mutters: 'Hmm… {low} to {high}, let's see…'"
        ]
        return random.choice(lines)


    def react_narrow(self, low: int, high: int) -> str:
        lines = [
            f"{self.name} has narrowed it down to either {low} or {high}!",
            f"{self.name} gasps — only {low} or {high} are left!",
            f"{self.name} knows it’s either {low} or {high} now. The tension rises!",
            f"{self.name} is sweating — just {low} and {high} remain!",
            f"{self.name} whispers: 'It's either {low} or {high}… I can feel it.'",
            f"{self.name} leans in closer — two numbers left: {low} and {high}.",
            f"{self.name} clenches their fist: 'Just {low} and {high}… this is it.'"
        ]
        return random.choice(lines)


    def react_final(self) -> str:
        lines = [
            f"{self.name} smiles from ear to ear — the final number is within reach!",
            f"{self.name} raises a triumphant eyebrow — there is only one number left!",
            f"{self.name} laughs confidently — the last number stands alone!",
            f"{self.name} smirks: 'I can’t lose now. This final guess is mine.'",
            f"{self.name} grins: 'Only one remains… time to claim victory!'",
            f"{self.name} bangs the virtual table — 'I’ve solved it. The end is near!'"
        ]
        return random.choice(lines)


    # noinspection PyMethodMayBeStatic
    def thinking_animation(self):
        for _ in range(3):
            time.sleep(0.5)
            print(". ", end="")
            sys.stdout.flush()
        time.sleep(1)