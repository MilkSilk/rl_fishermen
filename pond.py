import random

class Pond:
    def __init__(self, initial_fish_supply=None):
        self.fish_supply = 0
        self.change_fish_supply(initial_fish_supply) # 0-25
        self.set_fish_indicator_and_catch_difficulty()
    
    def serve_fisherman(self):
        fisherman_luck = random.random()
        if fisherman_luck > self.fish_catch_difficulty:
            self.change_fish_supply(-1)
            return 1
        else:
            return 0
        
    def change_fish_supply(self, change_number):
        self.fish_supply += change_number
        self.fish_indicator = self.fish_supply // 5
        self.fish_catch_difficulty = 0.75 - self.fish_supply / 50

    def breed_fish(self):
        breeding_luck = random.random()
        new_fish = (self.fish_supply * breeding_luck) // 3
        self.change_fish_supply(new_fish)
        

    


