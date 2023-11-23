# Fishing commons dillema simulator with a reinforcement learning solution

App showcasing reinforcement learning capabilities

It compares a naive strategy on an environment vs policy learnt by a RL agent with the PPO algorithm

## How to run
pip install -r requirements.txt

streamlit run app.py --server.port 8501 --server.runOnSave True

On the bottom of app.py comment/uncomment relevant function to either run naive or RL policy.
F5 on the web browser to reset after commenting/uncommenting