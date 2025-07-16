"""
Module for managing challenges
"""
from path_manager import *
from glob import glob
import importlib.util
import importlib


class ChallengeManager:
    def __init__(self):
        self.challenges = {}
        self.userchallenges = {}
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
        
        userchallenge_dir = get_userchallenges_directory()
        for challenge in glob("**/*.py", root_dir=userchallenge_dir, recursive=True):
            filename = os.path.basename(challenge)
            spec = importlib.util.spec_from_file_location(filename, os.path.join(userchallenge_dir, challenge))
            module = importlib.util.module_from_spec(spec)

            sys.modules[filename] = module
            spec.loader.exec_module(module)

            headers = getattr(module, "HEADERS")
            headers['run_func'] = getattr(module, "run")
            headers['id'] = filename[:-3]

            self.userchallenges[headers['id']] = headers

    def get_challenge(self, challenge_id):
        """Get a challenge by his ID"""
        return self.challenges.get(challenge_id)
    
    def get_all_userchallenges(self):
        """Get all users challenges"""
        return self.userchallenges
    
    def get_all_challenges(self):
        """Get all challenges"""
        return self.challenges
    
    def set_current_challenge(self, challenge_id):
        """Set current challenge"""
        if challenge_id is None:
            self.current_challenge = None
        else:
            if challenge_id.startswith("user."):
                self.current_challenge = self.userchallenges.get(challenge_id[5:])
            else:
                self.current_challenge = self.challenges.get(challenge_id)

        return self.current_challenge
    
    def get_current_challenge(self):
        """Get current challenge"""
        return self.current_challenge

challenge_manager = ChallengeManager()
