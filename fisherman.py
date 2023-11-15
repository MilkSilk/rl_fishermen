import streamlit as st
import random

class Fisherman:
    def __init__(self, fisherman_id, policy=None, ponds=None, pond_id=0):
        self.fisherman_id = fisherman_id
        self.policy = policy
        self.ponds = ponds
        self.pond = ponds[pond_id]
        self.fish = 0
        self.caught_fish = 0

    def action(self):
        action = self.policy()
        if action == 4:
            return
        else:
            self.pond = self.ponds[action]
            fisherman_luck = random.random()
            self.caught_fish = self.pond.serve_fisherman(fisherman_luck)
            self.fish += self.caught_fish

    def render_fisherman(self, pond_to_render_at, container=st):
        if self.pond == pond_to_render_at:
            im_source = f'images/fishermen/{self.fisherman_id}.jpg'
        else:
            im_source = 'images/fishermen/empty.jpg'
        container.image(im_source)

    def __str__(self):
        return f'Fisherman{self.fisherman_id}. Fishing at pond {self.pond}, has {self.fish} fish'

