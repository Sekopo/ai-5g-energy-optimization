AI-Driven Energy Optimization for 5G Networks

Overview

This project presents an AI-based approach to reduce energy consumption in 5G base stations while maintaining acceptable Quality of Service (QoS).
Using NS-3 simulation and Q-learning, the system dynamically adjusts transmission power based on network load.

The project compares three scenarios:

1. Baseline: Fixed maximum power (no optimization)
2. Rule-Based: Static threshold-based control
3. AI-Based: Reinforcement Learning (adaptive control)


Objectives

(a) Reduce energy consumption in 5G networks
(b) Maintain acceptable throughput, latency, and packet loss
(c) Demonstrate advantages of AI over static approaches


System Architecture

NS-3 Simulation (sim.cc) -> state.txt (network load) -> ai_infer.py (selects power level) -> NS-3 applies action (computes reward) -> reward.txt + next_state.txt -> ai_train.py (updates Q-table)


Technologies Used

1. NS-3 (C++): Network simulation
2. Python: AI logic (Q-learning)
3. Pandas & Matplotlib: Data analysis and visualization


Project Structure

AI-5G-PROJECT/
> config/                # Configuration files
> data/                  # AI scripts and runtime files
    - ai_infer.py
    - ai_train.py
    - ai_agent_legacy.py
> scripts/
    - plot.py            # Graph generation
> ns3-sim/
    - sim.cc             # NS-3 simulation file
> results/               # Output graphs/scripts
> README.md
> requirements.txt


Installation & Setup

1. Install Python dependencies

bash
    pip install -r requirements.txt


2. Install NS-3

Download and install NS-3 from:
[https://www.nsnam.org/](https://www.nsnam.org/)


3. Add simulation file

Copy the simulation file into NS-3:

bash
    cp ns3-sim/sim.cc <ns-3-dev>/scratch/


4. Build NS-3

bash
    cd ns-3-dev
    ./ns3 build


Running the Simulation

Baseline (no optimization)

bash
    ./ns3 run scratch/sim -- --scenario=0


Rule-based control

bash
    ./ns3 run scratch/sim -- --scenario=1


AI-based control (learning enabled)

bash
    ./ns3 run scratch/sim -- --scenario=2


Run the AI scenario multiple times to allow learning:

bash
    ./ns3 run scratch/sim -- --scenario=2


Generating Graphs

bash
    cd scripts
    python plot.py


This will generate:

- Power consumption graphs
- Throughput comparison
- Packet loss comparison
- Average performance charts


Results Summary

1. AI dynamically adjusts transmission power
2. Reduces energy consumption compared to baseline
3. Maintains acceptable QoS
4. Outperforms rule-based control in adaptability


Reinforcement Learning Details

(a) Algorithm: Q-Learning
(b) State: Network load
(c) Actions: Transmission power levels (80W – 200W)
(d) Reward Function:

    Reward = Throughput − (0.7 × Power) − (30 × PacketLoss)


Key Parameters:

  1. α (alpha): Learning rate
  2. γ (gamma): Discount factor
  3. ε (epsilon): Exploration rate


Key Insights

(a) Static systems waste energy under low load
(b) Rule-based systems lack flexibility
(c) AI adapts dynamically to network conditions
(d) Trade-off between energy saving and QoS is effectively balanced


Future Improvements

1. Use Deep Reinforcement Learning (DQN)
2. Integrate real network datasets
3. Multi-cell and multi-user simulation
4. Real-time deployment


Author

Masheane Sekopo and Renang Lenkoe
(Final Year B.Eng Project – Computer Systems & Networks Engineering)


License

This project is for academic and research purposes.

