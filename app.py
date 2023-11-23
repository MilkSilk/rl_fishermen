import streamlit as st 
import random
import time
import pandas as pd
import plotly.express as px
from ray.rllib.algorithms.ppo import PPO

from fisherman import Fisherman
from pond import Pond
from environment import FishingEnv

debug = False
n_steps = 50
n_extra_renders_per_episode = 2
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

if 'ponds' not in st.session_state:
    st.session_state['ponds'] = []
    for i in range(4):
        initial_fish_supply = random.randint(9, 21)
        new_pond = Pond(pond_id=i, initial_fish_supply=initial_fish_supply)
        st.session_state['ponds'].append(new_pond)
        if debug:
            st.text(new_pond)

if 'fishermen' not in st.session_state:
    dummy_policy = lambda: random.randint(0, 3)
    st.session_state['fishermen'] = []
    for i in range(12):
        new_fisherman = Fisherman(fisherman_id=i, policy=dummy_policy, ponds=st.session_state['ponds'], pond_id=dummy_policy())
        st.session_state['fishermen'].append(new_fisherman)
        if debug:
            st.text(new_fisherman)

if 'step_no' not in st.session_state:
    st.session_state['step_no'] = 0
if 'ponds_supply' not in st.session_state:
    st.session_state['ponds_supply'] = []

if 'trainer' not in st.session_state:
    st.session_state['trainer'] = PPO(config=env_config, env=FishingEnv)
    checkpoint_location = "models\checkpoint-1"
    st.session_state['trainer'].load_checkpoint(checkpoint_location)
if 'env' not in st.session_state:
    st.session_state['env'] = FishingEnv(config=env_config)

st.title('Reinforcement learning agents showcase')
st.markdown('</br></br></br>', unsafe_allow_html=True)

def render_pond(pond_id, fisherman_col1, pond_col, fisherman_col2):

    with fisherman_col1:
        st.image('images/fishermen/empty.jpg')
        st.session_state['fishermen'][0].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.session_state['fishermen'][1].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.session_state['fishermen'][2].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

    with pond_col:
        col1, col2, col3 = st.columns(3)
        st.session_state['fishermen'][3].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col1)
        st.session_state['fishermen'][4].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col2)
        st.session_state['fishermen'][5].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col3)
        st.image(f"images/pond/{st.session_state['ponds'][pond_id].fish_indicator}.jpg")
        col1, col2, col3 = st.columns(3)
        st.session_state['fishermen'][6].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col1)
        col1.image('images/fishermen/empty.jpg')
        st.session_state['fishermen'][7].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col2)
        col2.image('images/fishermen/empty.jpg')
        st.session_state['fishermen'][8].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id], container=col3)
        col3.image('images/fishermen/empty.jpg')

    with fisherman_col2:
        st.image('images/fishermen/empty.jpg')
        st.session_state['fishermen'][9].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.session_state['fishermen'][10].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.session_state['fishermen'][11].render_fisherman(pond_to_render_at=st.session_state['ponds'][pond_id])
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

fisherman_col1, pond_col1, fisherman_col2, _, \
    fisherman_col3, pond_col2, fisherman_col4 = st.columns([1, 3, 1, 1, 1, 3, 1])

if (st.session_state['step_no'] != 0) and ((st.session_state['step_no'] == 1) or \
   (st.session_state['step_no'] % (n_steps // n_extra_renders_per_episode) == 0) or \
   (st.session_state['step_no'] > n_steps)):
    st.markdown(f"### Environment state on step {st.session_state['step_no']}")
    fisherman_col1, pond_col1, fisherman_col2, _, \
        fisherman_col3, pond_col2, fisherman_col4 = st.columns([1, 3, 1, 1, 1, 3, 1])
    render_pond(0, fisherman_col1, pond_col1, fisherman_col2)
    render_pond(1, fisherman_col3, pond_col2, fisherman_col4)

    render_pond(2, fisherman_col1, pond_col1, fisherman_col2)
    render_pond(3, fisherman_col3, pond_col2, fisherman_col4)
    st.markdown("""---""")
    time.sleep(5)

def run_rl_fishermen():
    st.session_state['ponds'] = st.session_state['env'].ponds
    st.session_state['fishermen'] = st.session_state['env'].fishermen
    action = st.session_state['trainer'].compute_single_action(observation=st.session_state['env'].state)
    state, reward, done, truncated, info = st.session_state['env'].step(action)
    for pond in st.session_state['env'].ponds:
        pond_state = {
            'pond_id': pond.pond_id,
            'step_no': st.session_state['step_no'],
            'fish_supply': pond.fish_supply
        }
        st.session_state['ponds_supply'].append(pond_state)

    fishermen_data = []
    for fisherman in st.session_state['env'].fishermen:
        fishermen_data.append({'fisherman_id': fisherman.fisherman_id, 'fish_caught':fisherman.fish})
    st.session_state['step_no'] += 1
    if st.session_state['step_no'] <= n_steps:
        st.rerun()
    return fishermen_data

def run_naive_fishermen():
    for fisherman in st.session_state['fishermen']:
        fisherman.action()

    for pond in st.session_state['ponds']:
        pond_state = {'pond_id': pond.pond_id, 
            'step_no': st.session_state['step_no'], 
            'fish_supply': pond.fish_supply
        }
        st.session_state['ponds_supply'].append(pond_state)
        pond.breed_fish()

    st.session_state['step_no'] += 1
    if st.session_state['step_no'] <= n_steps:
        st.rerun()
    fishermen_data = []
    for fisherman in st.session_state['fishermen']:
        fishermen_data.append({'fisherman_id': fisherman.fisherman_id, 'fish_caught':fisherman.fish})
    return fishermen_data

fishermen_data = run_rl_fishermen()
# fishermen_data = run_naive_fishermen()

df_fishermen = pd.DataFrame(fishermen_data)
df_ponds = pd.DataFrame(st.session_state['ponds_supply'])
st.plotly_chart(px.histogram(df_fishermen, x='fish_caught'))
st.metric('Average number of fish caught', df_fishermen['fish_caught'].mean().round(2))
st.plotly_chart(px.line(df_ponds, x='step_no', y='fish_supply', color='pond_id'))
