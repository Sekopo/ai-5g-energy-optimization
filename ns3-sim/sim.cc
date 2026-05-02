#include "ns3/core-module.h"
#include <fstream>
#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace ns3;

// -------- Rule-based function --------
double GetRuleBasedPower(double load) {
    if (load < 0.3) return 100;
    else if (load < 0.7) return 160;
    else return 200;
}

int main(int argc, char *argv[]) {

    int scenario = 0;
    CommandLine cmd;
    cmd.AddValue("scenario", "0=Baseline,1=Rule,2=AI", scenario);
    cmd.Parse(argc, argv);

    srand(time(0));

    std::string filename;
    if (scenario == 0) filename = "../data/baseline.csv";
    else if (scenario == 1) filename = "../data/rule.csv";
    else filename = "../data/ai.csv";

    // -------- Check if file is empty --------
    std::ifstream checkFile(filename);
    bool isEmpty = checkFile.peek() == std::ifstream::traits_type::eof();
    checkFile.close();

    std::ofstream log(filename, std::ios::app);

    if (!log.is_open()) {
        std::cout << "ERROR: Cannot open file!" << std::endl;
        return 1;
    }

    // -------- Write header if empty --------
    if (isEmpty) {
        log << "iteration,load,throughput,latency,packetLoss,power,energy\n";
    }

    // -------- Simulation loop --------
    for (int i = 0; i < 20; i++) {

        // -------- Time-based load --------
        double load;
        if (i < 3) load = 0.2;
        else if (i < 7) load = 1.0;
        else load = 0.5;

        // -------- Base network conditions --------
        double throughput = 20.0 * load;
        double delay = 50.0 * (1 - load);
        int rxPackets = 100;

        int power = 200;

        // -------- Scenario logic --------
        if (scenario == 0) {
            power = 200;
        }
        else if (scenario == 1) {
            power = GetRuleBasedPower(load);
        }
        else if (scenario == 2) {

            // -------- STEP 1: Write state --------
            std::ofstream stateFile("../data/state.txt");
            stateFile << load;
            stateFile.close();

            // -------- STEP 2: Run inference --------
            int inferResult = system("python3 ../data/ai_infer.py");

            if (inferResult != 0) {
                std::cout << "AI inference failed!" << std::endl;
            }

            // -------- STEP 3: Read action --------
            std::ifstream actionFile("../data/action.txt");
            if (actionFile.is_open()) {
                actionFile >> power;
                actionFile.close();
            } else {
                std::cout << "WARNING: Could not read action.txt, using default power." << std::endl;
            }
        }

        // -------- LOSS MODEL --------
        double snr = power / 200.0;
        double congestion = load;

        double lossProb = congestion * (1.0 - snr);

        // Noise
        lossProb += ((double) rand() / RAND_MAX) * 0.02;

        if (lossProb > 1.0) lossProb = 1.0;
        if (lossProb < 0.0) lossProb = 0.0;

        int lostPackets = (int)(lossProb * 100);

        // -------- Metrics --------
        double avgThroughput = throughput * (power / 200.0);

        double avgLatency = (rxPackets > 0)
            ? delay / rxPackets
            : 0;

        double packetLoss = (rxPackets + lostPackets > 0)
            ? (double) lostPackets / (rxPackets + lostPackets)
            : 0;

        // -------- Reward --------
        double reward = avgThroughput
                        - 0.7 * power
                        - 30 * packetLoss;

        // -------- STEP 4: Write reward + next state --------
        if (scenario == 2) {

            std::ofstream rewardFile("../data/reward.txt");
            rewardFile << reward;
            rewardFile.close();

            std::ofstream nextStateFile("../data/next_state.txt");
            nextStateFile << load;
            nextStateFile.close();

            // -------- STEP 5: Train --------
            int trainResult = system("python3 ../data/ai_train.py");

            if (trainResult != 0) {
                std::cout << "AI training failed!" << std::endl;
            }
        }

        // -------- Energy --------
        double timeStep = 1.0;
        double energy = power * timeStep;

        // -------- Logging --------
        log << i << ","
            << load << ","
            << avgThroughput << ","
            << avgLatency << ","
            << packetLoss << ","
            << power << ","
            << energy << "\n";

        std::cout << "Iter " << i
                  << " | Load: " << load
                  << " | Power: " << power
                  << " | Loss: " << packetLoss
                  << std::endl;
    }

    log.close();
    return 0;
}