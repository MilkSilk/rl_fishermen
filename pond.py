import random

class Pond:
    def __init__(self, pond_id, initial_fish_supply=None):
        self.pond_id = pond_id
        self.fish_supply = 0
        self.change_fish_supply(initial_fish_supply) # 0-25
    
    def serve_fisherman(self, fisherman_luck):
        if fisherman_luck > self.fish_catch_difficulty and self.fish_supply > 0:
            self.change_fish_supply(-1)
            return 1
        else:
            return 0
        
    def change_fish_supply(self, change_number):
        self.fish_supply += change_number
        self.fish_indicator = int(self.fish_supply // 5)
        self.fish_catch_difficulty = 0.75 - self.fish_supply / 50

    def breed_fish(self):
        breeding_luck = random.random()
        new_fish = (self.fish_supply * breeding_luck) // 4
        self.change_fish_supply(new_fish)

    def __str__(self):
        return f'Pond{self.pond_id}. Fish supply: {self.fish_supply}. ' + \
          f'Indicator: {self.fish_indicator}. Difficulty: {self.fish_catch_difficulty}'
        

    


