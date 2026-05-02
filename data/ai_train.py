import pickle
import os

actions = list(range(80, 201, 20))
alpha = 0.1
gamma = 0.9

Q_FILE = "../data/q_table.pkl"

# -------- LOAD STATE --------
with open("../data/state.txt", "r") as f:
    load = float(f.read().strip())
state = int(load * 10)

# -------- LOAD NEXT STATE --------
with open("../data/next_state.txt", "r") as f:
    next_load = float(f.read().strip())
next_state = int(next_load * 10)

# -------- LOAD REWARD --------
with open("../data/reward.txt", "r") as f:
    reward = float(f.read().strip())

# -------- LOAD ACTION INDEX --------
with open("../data/last_action.txt", "r") as f:
    action_index = int(f.read().strip())

# -------- LOAD Q-TABLE --------
Q = {}
if os.path.exists(Q_FILE):
    try:
        with open(Q_FILE, "rb") as f:
            Q = pickle.load(f)
    except:
        Q = {}

# Initialize states
if state not in Q:
    Q[state] = [0] * len(actions)

if next_state not in Q:
    Q[next_state] = [0] * len(actions)

# -------- Q-UPDATE --------
old_value = Q[state][action_index]
next_max = max(Q[next_state])

new_value = old_value + alpha * (reward + gamma * next_max - old_value)
Q[state][action_index] = new_value

# -------- SAVE Q --------
with open(Q_FILE, "wb") as f:
    pickle.dump(Q, f)

print(f"[TRAIN] State: {state}, Reward: {reward}, Updated Q")