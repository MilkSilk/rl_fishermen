# General DS
import numpy as np
import pandas as pd
import plotly.express as px
import random

# RL
import ray
import gymnasium as gym
from gymnasium.spaces import MultiDiscrete
from ray.rllib.algorithms.ppo import PPO

# App modules
from fisherman import Fisherman
from pond import Pond

class FishingEnv(gym.Env):
    def __init__(self, config):
        self.action_space = MultiDiscrete([5]*12) # 4 ponds (5th option to skip fishing), 12 fishermen 
        self.observation_space = MultiDiscrete([6, 6, 6, 6]) # 6 fish indicator values for 4 ponds
        self.reset()

    def step(self, action):
        for fisherman in self.fishermen:
            fisherman.policy = lambda: action[fisherman.fisherman_id] 
            # fisherman.policy = lambda: random.randint(0, 4)
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

def run_episode(env_config):
    trainer = PPO(config=env_config, env=FishingEnv)

    env = FishingEnv(config=env_config)
    checkpoint_location = "models\checkpoint-1"
    trainer.load_checkpoint(checkpoint_location)
    done = False
    ponds_supply_info = []
    step_no = 0
    while not done:
        action = trainer.compute_single_action(observation=env.state)
        state, reward, done, truncated, info = env.step(action)
        for pond in env.ponds:
            pond_state = {
                'pond_id': pond.pond_id,
                'step_no': step_no,
                'fish_supply': pond.fish_supply
            }
            ponds_supply_info.append(pond_state)
        step_no += 1
    fishermen_data = []
    for fisherman in env.fishermen:
        fishermen_data.append({'fisherman_id': fisherman.fisherman_id, 'fish_caught':fisherman.fish})
    return env, fishermen_data, ponds_supply_info
        

def train(env_config):
    trainer = PPO(config=env_config, env=FishingEnv)
    checkpoint_location = "models\checkpoint-1"
    trainer.load_checkpoint(checkpoint_location)
    print('Starting training')
    try:
        for i in range(500):
            results = trainer.train()
            if i % 50 == 0:
                print(f"Iter: {i}; avg. reward={results['episode_reward_mean']}")
                save_result = trainer.save()
                path_to_checkpoint = save_result.checkpoint.path
                print(
                    "An Algorithm checkpoint has been created inside directory: "
                    f"'{path_to_checkpoint}'."
                )
                print()
                print()
    except KeyboardInterrupt:
        pass
    save_result = trainer.save()
    path_to_checkpoint = save_result.checkpoint.path
    print(
        "An Algorithm checkpoint has been created inside directory: "
        f"'{path_to_checkpoint}'."
    )


if __name__ == "__main__":
    ray.init(num_gpus=0)
    ray.rllib.utils.check_env(FishingEnv(config={}))
    env_config = {
        # Env class to use (here: gym.Env sub-class from above).
        "env": FishingEnv,
        "rollout_fragment_length": 128,
        "train_batch_size": 1024,
        "num_gpus": 0,
        "num_gpus_per_worker": 0,
        # "framework": "tf",
        "create_env_on_driver": True,
        # Parallelize environment rollouts.
        "num_workers": 1,
    }

    # train(env_config = env_config)

    env, fishermen_data, ponds_supply_info = run_episode(env_config = env_config)
    df_fishermen = pd.DataFrame(fishermen_data)
    df_ponds = pd.DataFrame(ponds_supply_info)
    hist_fig = px.histogram(df_fishermen, x='fish_caught')
    print('Average number of fish caught', df_fishermen['fish_caught'].mean().round(2))
    ponds_fig = px.line(df_ponds, x='step_no', y='fish_supply', color='pond_id')

    import plotly
    plotly.offline.plot(hist_fig, filename='histogram.html')
    plotly.offline.plot(ponds_fig, filename='ponds.html')

