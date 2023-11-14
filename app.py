import streamlit as st # streamlit run app.py --server.port 8501 --server.runOnSave True
import random

from fisherman import Fisherman
from pond import Pond

debug = False

ponds = []
for i in range(4):
    initial_fish_supply = random.randint(9, 21)
    new_pond = Pond(pond_id=i, initial_fish_supply=initial_fish_supply)
    ponds.append(new_pond)
    if debug:
        st.text(new_pond)

dummy_policy = lambda: random.randint(0, 3)
fishermen = []
for i in range(12):
    new_fisherman = Fisherman(fisherman_id=i, policy=dummy_policy, ponds=ponds, pond_id=dummy_policy())
    fishermen.append(new_fisherman)
    if debug:
        st.text(new_fisherman)


st.title('Reinforcement learning agents showcase')
st.markdown('</br></br></br>', unsafe_allow_html=True)

def render_pond(pond_id, fisherman_col1, pond_col, fisherman_col2):

    with fisherman_col1:
        st.image('images/fishermen/empty.jpg')
        fishermen[0].render_fisherman(pond_to_render_at=ponds[pond_id])
        fishermen[1].render_fisherman(pond_to_render_at=ponds[pond_id])
        fishermen[2].render_fisherman(pond_to_render_at=ponds[pond_id])
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

    with pond_col:
        col1, col2, col3 = st.columns(3)
        fishermen[3].render_fisherman(pond_to_render_at=ponds[pond_id], container=col1)
        fishermen[4].render_fisherman(pond_to_render_at=ponds[pond_id], container=col2)
        fishermen[5].render_fisherman(pond_to_render_at=ponds[pond_id], container=col3)
        st.image(f'images/pond/{ponds[pond_id].fish_indicator}.jpg')
        col1, col2, col3 = st.columns(3)
        fishermen[6].render_fisherman(pond_to_render_at=ponds[pond_id], container=col1)
        col1.image('images/fishermen/empty.jpg')
        fishermen[7].render_fisherman(pond_to_render_at=ponds[pond_id], container=col2)
        col2.image('images/fishermen/empty.jpg')
        fishermen[8].render_fisherman(pond_to_render_at=ponds[pond_id], container=col3)
        col3.image('images/fishermen/empty.jpg')

    with fisherman_col2:
        st.image('images/fishermen/empty.jpg')
        fishermen[9].render_fisherman(pond_to_render_at=ponds[pond_id])
        fishermen[10].render_fisherman(pond_to_render_at=ponds[pond_id])
        fishermen[11].render_fisherman(pond_to_render_at=ponds[pond_id])
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

fisherman_col1, pond_col1, fisherman_col2, _, \
    fisherman_col3, pond_col2, fisherman_col4 = st.columns([1, 3, 1, 1, 1, 3, 1])

for i in range(50):
    if i % 5 == 0:
        st.text(i)
        fisherman_col1, pond_col1, fisherman_col2, _, \
            fisherman_col3, pond_col2, fisherman_col4 = st.columns([1, 3, 1, 1, 1, 3, 1])
        render_pond(0, fisherman_col1, pond_col1, fisherman_col2)
        render_pond(1, fisherman_col3, pond_col2, fisherman_col4)

        render_pond(2, fisherman_col1, pond_col1, fisherman_col2)
        render_pond(3, fisherman_col3, pond_col2, fisherman_col4)
        st.markdown("""---""")
    for fisherman in fishermen:
        fisherman.action()

render_pond(0, fisherman_col1, pond_col1, fisherman_col2)
render_pond(1, fisherman_col3, pond_col2, fisherman_col4)

render_pond(2, fisherman_col1, pond_col1, fisherman_col2)
render_pond(3, fisherman_col3, pond_col2, fisherman_col4)
