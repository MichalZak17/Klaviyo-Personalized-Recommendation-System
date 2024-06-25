import json
import random

class MenuSelector:
    @staticmethod
    def select_list(lists):
        print("Select a list:")

        for index, lst in enumerate(lists['data']):
            print(f"{index + 1}. {lst['attributes']['name']}")
            
        selection = int(input("Enter your choice (number): "))
        return lists['data'][selection - 1]['id']
    
    @staticmethod
    def select_random_profile(profiles) -> dict:
        profiles = profiles.get("data", [])

        if not profiles: return None

        return random.choice(profiles)