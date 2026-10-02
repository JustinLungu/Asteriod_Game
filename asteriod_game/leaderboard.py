from asteriod_game.constants import (
    LEADERBOARD_FILE,
    LEADERBOARD_SIZE,
)
import json

class Leaderboard:
    def __init__(self, path=LEADERBOARD_FILE, size=LEADERBOARD_SIZE):
        self.path = path
        self.size = size
        self.scores = self._load()

    def _load(self):
        try:
            with open(self.path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        return sorted((s for s in data if isinstance(s, int)), reverse=True)[:self.size]

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.scores, f, indent=2)

    def submit(self, score):
        self.scores.append(score)
        self.scores.sort(reverse=True)
        self.scores = self.scores[:self.size]
        self._save()

    def is_high_score(self, score):
        return len(self.scores) < self.size or score > self.scores[-1]
