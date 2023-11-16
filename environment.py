import numpy as np
import pandas as pd
import ray
import random
# import tensorflow as tf
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete
from ray.rllib.algorithms.ppo import PPO

from fisherman import Fisherman
from pond import Pond

class FishingEnv(gym.Env):
    def __init__(self, config):
        self.action_space = MultiDiscrete([5]*12) # 4 ponds (5th option to skip fishing), 12 fishermen 
        self.observation_space = MultiDiscrete([6, 6, 6, 6]) # 6 fish indicator values for 4 ponds
        self.reset()

    def step(self, action):
        for fisherman in self.fishermen:
            # fisherman.policy = lambda: action[fisherman.fisherman_id] 
            fisherman.policy = lambda: random.randint(0, 4)
            fisherman.action()
        for pond in self.ponds:
            pond.breed_fish()
        self.state = np.array([pond.fish_indicator for pond in self.ponds])
        reward = sum([fisherman.caught_fish for fisherman in self.fishermen])
        done = False
        n_fish_in_ponds = sum([pond.fish_supply for pond in self.ponds])
        end_condition = n_fish_in_ponds == 0 or self.step_no == 50 # No fish in ponds or 50th episode
        if end_condition:
            done = True
        truncated = False
        info = {}
        self.step_no += 1
        return self.state, reward, done, truncated, info

    def reset(self, seed=None, options=None):
        self.step_no = 0
        self.ponds = []
        for i in range(4):
            initial_fish_supply = random.randint(9, 21)
            new_pond = Pond(pond_id=i, initial_fish_supply=initial_fish_supply)
            self.ponds.append(new_pond)

        dummy_policy = lambda: random.randint(0, 3)
        self.fishermen = []
        for i in range(12):
            new_fisherman = Fisherman(fisherman_id=i, 
                                      policy=dummy_policy, 
                                      ponds=self.ponds,
                                      pond_id=dummy_policy()
                                     )
            self.fishermen.append(new_fisherman)
        self.state = np.array([pond.fish_indicator for pond in self.ponds])
        info = {}
        return self.state, info

    def render():
        pass

def run_step(env_config):
    trainer = PPO(config=env_config, env=FishingEnv)

    trainer.load_checkpoint("C:\Users\jacek.jankowiak\ray_results\PPO_FishingEnv_2023-11-16_08-12-01thvfkqm2")
    try:
        print(trainer.state)
        action = trainer.compute_single_action(observation=trainer.state)
        print(action)
        state, reward, done, truncated, info = trainer.step(action)
        print(state)
        print(reward)
    except Exception as e:
        print(e)

def train(env_config):
    trainer = PPO(config=env_config, env=FishingEnv)
    
    print('Starting training')
    try:
        for i in range(100):
            results = trainer.train()
            print(f"Iter: {i}; avg. reward={results['episode_reward_mean']}")
    except KeyboardInterrupt:
        pass
    trainer.save()


if __name__ == "__main__":
    ray.init(num_gpus=0)
    ray.rllib.utils.check_env(FishingEnv(config={}))
    env_config = {
        # Env class to use (here: gym.Env sub-class from above).
        "env": FishingEnv,
        "rollout_fragment_length": 128,
        "train_batch_size": 128,
        "num_gpus": 0,
        "num_gpus_per_worker": 0,
        # "framework": "tf",
        "create_env_on_driver": True,
        # Parallelize environment rollouts.
        "num_workers": 1,
    }
    train(env_config = env_config)
    run_step(env_config = env_config)
