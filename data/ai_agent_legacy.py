import random
import os
import pickle

# -------- PARAMETERS --------
actions = list(range(80, 201, 20))
alpha = 0.1
gamma = 0.9
epsilon = 0.3

Q_FILE = "../data/q_table.pkl"

# -------- LOAD STATE --------
with open("../data/state.txt", "r") as f:
    load = float(f.read().strip())

state = int(load * 10)

# -------- LOAD Q-TABLE (ROBUST) --------
Q = {}

if os.path.exists(Q_FILE):
    try:
        with open(Q_FILE, "rb") as f:
            Q = pickle.load(f)
    except:
        print("Resetting corrupted Q-table...")
        Q = {}

# Initialize state if new
if state not in Q:
    Q[state] = [0] * len(actions)

# -------- ACTION SELECTION --------
if random.random() < epsilon:
    action_index = random.randint(0, 2)
else:
    action_index = Q[state].index(max(Q[state]))

power = actions[action_index]

# -------- WRITE ACTION --------
with open("../data/action.txt", "w") as f:
    f.write(str(power))

# -------- READ REWARD --------
reward = 0
if os.path.exists("../data/reward.txt"):
    with open("../data/reward.txt", "r") as f:
        reward = float(f.read().strip())

# -------- READ NEXT STATE --------
next_state = state
if os.path.exists("../data/next_state.txt"):
    with open("../data/next_state.txt", "r") as f:
        next_load = float(f.read().strip())
        next_state = int(next_load * 10)

if next_state not in Q:
    Q[next_state] = [0] * len(actions)

# -------- Q-LEARNING UPDATE --------
old_value = Q[state][action_index]
next_max = max(Q[next_state])

new_value = old_value + alpha * (reward + gamma * next_max - old_value)
Q[state][action_index] = new_value

# -------- SAVE Q-TABLE (THIS WAS THE KEY) --------
with open(Q_FILE, "wb") as f:
    pickle.dump(Q, f)

# -------- DEBUG PRINT --------
print(f"State: {state}, Action: {power}, Reward: {reward}")