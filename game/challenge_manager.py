"""
Module for managing challenges
"""
from path_manager import *
from glob import glob
import importlib


class ChallengeManager:
    def __init__(self):
        self.challenges = {}
        self.current_challenge = None
        self.load_challenges()
    
    def load_challenges(self):
        """Load every challenges"""
        for challenge in glob("*.py", root_dir=resource_path("challenges")):
            module = importlib.import_module(f"challenges.{challenge[:-3]}")

            if not hasattr(module, "HEADERS"):
                print(f"Missing HEADERS dict for {challenge}")
                continue

            if not hasattr(module, "run"):
                print(f"Missing run() function for {challenge}")
                continue

            headers = getattr(module, "HEADERS")
            headers['run_func'] = getattr(module, "run")
            headers['id'] = challenge[:-3]

            self.challenges[headers['id']] = headers
    
    def get_challenge(self, challenge_id):
        """Get a challenge by his ID"""
        return self.challenges.get(challenge_id)
    
    def get_all_challenges(self):
        """Get all challenges"""
        return self.challenges
    
    def set_current_challenge(self, challenge_id):
        """Set current challenge"""
        if challenge_id is None:
            self.current_challenge = None
        else:
            self.current_challenge = self.challenges.get(challenge_id)
        return self.current_challenge
    
    def get_current_challenge(self):
        """Get current challenge"""
        return self.current_challenge

challenge_manager = ChallengeManager()
