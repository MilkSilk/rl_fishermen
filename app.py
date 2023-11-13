import streamlit as st

st.title('Reinforcement learning agents showcase')
st.markdown('</br></br></br>', unsafe_allow_html=True)

def render_pond(pond_id, fisherman_col1, pond_col, fisherman_col2):

    with fisherman_col1:
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/7.jpg')
        st.image('images/fishermen/8.jpg')
        st.image('images/fishermen/9.jpg')
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

    with pond_col:
        col1, col2, col3 = st.columns(3)
        col1.image('images/fishermen/1.jpg')
        col2.image('images/fishermen/2.jpg')
        col3.image('images/fishermen/3.jpg')
        st.image('images/pond/5.jpg')
        col1, col2, col3 = st.columns(3)
        col1.image('images/fishermen/10.jpg')
        col1.image('images/fishermen/empty.jpg')
        col2.image('images/fishermen/11.jpg')
        col2.image('images/fishermen/empty.jpg')
        col3.image('images/fishermen/12.jpg')
        col3.image('images/fishermen/empty.jpg')

    with fisherman_col2:
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/4.jpg')
        st.image('images/fishermen/5.jpg')
        st.image('images/fishermen/6.jpg')
        st.image('images/fishermen/empty.jpg')
        st.image('images/fishermen/empty.jpg')

col1, col2 = st.columns(2)
fisherman_col1, pond_col1, fisherman_col2, _, \
    fisherman_col3, pond_col2, fisherman_col4 = st.columns([1, 3, 1, 1, 1, 3, 1])
render_pond(pond_id, fisherman_col1, pond_col1, fisherman_col2)
render_pond(pond_id, fisherman_col3, pond_col2, fisherman_col4)

render_pond(pond_id, fisherman_col1, pond_col1, fisherman_col2)
render_pond(pond_id, fisherman_col3, pond_col2, fisherman_col4)
