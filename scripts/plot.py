import pandas as pd
import matplotlib.pyplot as plt

# -------- LOAD DATA --------
baseline = pd.read_csv("../data/baseline.csv")
rule = pd.read_csv("../data/rule.csv")
ai = pd.read_csv("../data/ai.csv")

# -------- GROUP AI BY ITERATION --------
ai_avg = ai.groupby("iteration").mean()

# -------- PLOT POWER --------
plt.figure()

plt.plot(baseline["iteration"], baseline["power"], label="Baseline", linewidth=2)
plt.plot(rule["iteration"], rule["power"], label="Rule-Based", linewidth=2)
plt.plot(ai_avg.index, ai_avg["power"], label="AI (Average)", linewidth=3)

plt.xlabel("Iteration")
plt.ylabel("Power (W)")
plt.title("Power Consumption Comparison")
plt.legend()
plt.grid()

plt.savefig("../results/power_comparison.png")
plt.show()

# -------- PLOT THROUGHPUT --------
plt.figure()

plt.plot(baseline["iteration"], baseline["throughput"], label="Baseline", linewidth=2)
plt.plot(rule["iteration"], rule["throughput"], label="Rule-Based", linewidth=2)
plt.plot(ai_avg.index, ai_avg["throughput"], label="AI (Average)", linewidth=3)

plt.xlabel("Iteration")
plt.ylabel("Throughput")
plt.title("Throughput Comparison")
plt.legend()
plt.grid()

plt.savefig("../results/throughput_comparison.png")
plt.show()

# -------- PLOT PACKET LOSS --------
plt.figure()

plt.plot(baseline["iteration"], baseline["packetLoss"], label="Baseline", linewidth=2)
plt.plot(rule["iteration"], rule["packetLoss"], label="Rule-Based", linewidth=2)
plt.plot(ai_avg.index, ai_avg["packetLoss"], label="AI (Average)", linewidth=3)

plt.xlabel("Iteration")
plt.ylabel("Packet Loss")
plt.title("Packet Loss Comparison")
plt.legend()
plt.grid()

plt.savefig("../results/loss_comparison.png")
plt.show()

# -------- BAR CHART (AVERAGES) --------
baseline_avg = baseline.mean()
rule_avg = rule.mean()
ai_avg_total = ai.mean()

labels = ["Baseline", "Rule-Based", "AI"]

power_vals = [baseline_avg["power"], rule_avg["power"], ai_avg_total["power"]]
throughput_vals = [baseline_avg["throughput"], rule_avg["throughput"], ai_avg_total["throughput"]]

plt.figure()
plt.bar(labels, power_vals)
plt.title("Average Power Consumption")
plt.ylabel("Power (W)")
plt.savefig("../results/avg_power.png")
plt.show()

plt.figure()
plt.bar(labels, throughput_vals)
plt.title("Average Throughput")
plt.ylabel("Throughput")
plt.savefig("../results/avg_throughput.png")
plt.show()

print("Plots generated successfully!")