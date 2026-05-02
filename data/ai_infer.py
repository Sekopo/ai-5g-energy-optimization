import random
import pickle
import os

actions = list(range(80, 201, 20))
epsilon = 0.3
Q_FILE = "../data/q_table.pkl"

# -------- LOAD STATE --------
with open("../data/state.txt", "r") as f:
    load = float(f.read().strip())

state = int(load * 10)

# -------- LOAD Q-TABLE --------
Q = {}
if os.path.exists(Q_FILE):
    try:
        with open(Q_FILE, "rb") as f:
            Q = pickle.load(f)
    except:
        Q = {}

if state not in Q:
    Q[state] = [0] * len(actions)

# -------- ACTION SELECTION --------
if random.random() < epsilon:
    action_index = random.randint(0, len(actions)-1)
else:
    action_index = Q[state].index(max(Q[state]))

power = actions[action_index]

# -------- SAVE ACTION --------
with open("../data/action.txt", "w") as f:
    f.write(str(power))

# Save chosen action index for training
with open("../data/last_action.txt", "w") as f:
    f.write(str(action_index))

print(f"[INFER] State: {state}, Action: {power}")