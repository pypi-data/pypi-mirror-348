import os
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import circuit_drawer
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Generate turn-to-qubit mapping
def generate_turn2qubit(protein_sequence):
    N = len(protein_sequence)
    if N < 2:
        raise ValueError("Protein sequence must have at least 2 beads.")
    num_turns = 2 * (N - 1)
    fixed_bits = '0100q1'
    variable_bits = 'q' * (num_turns - len(fixed_bits))
    return fixed_bits + variable_bits, fixed_bits, variable_bits

# Build MJ interaction matrix
def build_mj_interactions(protein):
    N = len(protein)
    mat = np.zeros((N, N))
    np.random.seed(29507)
    MJ = np.random.rand(20, 20) * -6
    MJ = np.triu(MJ) + np.triu(MJ, 1).T
    acids = ["C", "M", "F", "I", "L", "V", "W", "Y", "A", "G", 
             "T", "S", "N", "Q", "D", "E", "H", "R", "K", "P"]
    acid2idx = {acid: idx for idx, acid in enumerate(acids)}
    for i in range(N):
        for j in range(N):
            mat[i, j] = MJ[acid2idx[protein[i]], acid2idx[protein[j]]]
    return mat

# Compute energy from bitstrings
def exact_hamiltonian(bitstrings, hyperParams):
    lambda_dis = 720
    lambda_loc = 20
    lambda_back = 50
    energies = np.zeros(len(bitstrings))
    num_beads = len(hyperParams["protein"])

    for idx, bitstring in enumerate(bitstrings):
        config = list(hyperParams["turn2qubit"])
        q_indices = [i for i, x in enumerate(config) if x == 'q']
        for i, q_idx in enumerate(q_indices):
            config[q_idx] = bitstring[i]
        config = ''.join(config)
        turns = [int(config[i:i+2], 2) for i in range(0, len(config), 2)]
        energies[idx] = lambda_back * sum(turns[i] == turns[i+1] for i in range(len(turns) - 1))
        curr_interaction_qubit = hyperParams["numQubitsConfig"]
        for i in range(num_beads - 4):
            for j in range(i + 5, num_beads, 2):
                if curr_interaction_qubit >= len(bitstring):
                    break
                if bitstring[curr_interaction_qubit] == '0':
                    curr_interaction_qubit += 1
                    continue
                energies[idx] += hyperParams["interactionEnergy"][i, j]
                # … [rest of distance-based terms unchanged] …
                curr_interaction_qubit += 1
    return energies

# Ansatz circuit
def protein_config_ansatz(parameters):
    num_qubits = len(parameters) // 3
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        qc.h(i)
        qc.ry(parameters[i], i)
        qc.rx(parameters[i + num_qubits], i)
        qc.rz(parameters[i + 2 * num_qubits], i)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    for i in range(num_qubits):
        qc.t(i)
    for i in range(num_qubits):
        qc.ry(parameters[i], i)
        qc.rx(parameters[i + num_qubits], i)
        qc.rz(parameters[i + 2 * num_qubits], i)
    qc.measure_all()
    return qc

# CVaR objective function
def protein_vqe_objective(parameters, hyperParams):
    ansatz = protein_config_ansatz(parameters)
    simulator = AerSimulator()
    compiled_circuit = transpile(ansatz, simulator)
    job = simulator.run(compiled_circuit, shots=hyperParams["numShots"])
    result = job.result()
    counts = result.get_counts()
    bitstrings = [format(int(k.replace(" ", ""), 2), f'0{len(parameters) // 3}b') for k in counts]
    probs = np.array(list(counts.values())) / hyperParams["numShots"]
    energies = exact_hamiltonian(bitstrings, hyperParams)
    sort_idx = np.argsort(energies)
    sorted_probs = probs[sort_idx]
    sorted_energies = energies[sort_idx]
    alpha = 0.025
    cut_idx = np.searchsorted(np.cumsum(sorted_probs), alpha)
    cvar_probs = sorted_probs[:cut_idx + 1]
    cvar_probs[-1] += alpha - np.sum(cvar_probs)
    return np.dot(cvar_probs, sorted_energies[:cut_idx + 1]) / alpha

# --- MAIN EXECUTION ---
# 1. Sequence length check (max 10)
protein_sequence = input("Enter the protein sequence (max 10 amino acids, e.g., APRLRFY): ").strip().upper()
if len(protein_sequence) < 2 or len(protein_sequence) > 10:
    raise ValueError("Protein sequence must have between 2 and 10 amino acids.")

# 2. Max iterations
max_iterations = input("Enter maximum iterations [default 50]: ").strip()
max_iterations = int(max_iterations) if max_iterations.isdigit() and int(max_iterations) > 0 else 50

# 3. Output directory
output_dir = input("Enter output directory [default './results']: ").strip() or "./results"
os.makedirs(output_dir, exist_ok=True)

# Prepare quantum-folding hyperparameters
turn2qubit, fixed_bits, variable_bits = generate_turn2qubit(protein_sequence)
num_qubits_config = turn2qubit.count('q')
interaction_energy = build_mj_interactions(protein_sequence)
hyperParams = {
    "protein": protein_sequence,
    "turn2qubit": turn2qubit,
    "numQubitsConfig": num_qubits_config,
    "interactionEnergy": interaction_energy,
    "numShots": 1024
}

# 4. Iterate CVaR VQE with progress indicator
cvar_results = []
optimal_params = None
min_energy = np.inf

for i in range(max_iterations):
    initial_parameters = np.random.uniform(-np.pi, np.pi, size=3 * (num_qubits_config + 2))
    result = minimize(lambda θ: protein_vqe_objective(θ, hyperParams),
                      initial_parameters, method='COBYLA')
    cvar_results.append(result.fun)
    if result.fun < min_energy:
        min_energy = result.fun
        optimal_params = result.x
    # progress indicator
    pct = (i + 1) / max_iterations * 100
    print(f"Iteration {i+1}/{max_iterations} completed — {pct:.1f}%")

# Summary text
summary = f"""
--- Quantum Protein Folding Summary ---

Protein Sequence: {protein_sequence}
Fixed Bits:       {fixed_bits}
Variable Bits:    {variable_bits}
Minimum CVaR Energy: {min_energy:.5f}
"""

# Save summary
summary_path = os.path.join(output_dir, "output_summary.txt")
with open(summary_path, "w") as f:
    f.write(summary)
print(f"Saved summary → {summary_path}")

# Save optimal circuit image
optimal_circuit = protein_config_ansatz(optimal_params)
circuit_path = os.path.join(output_dir, "optimal_circuit.png")
circuit_drawer(optimal_circuit.remove_final_measurements(inplace=False),
               output='mpl', filename=circuit_path)
print(f"Saved circuit diagram → {circuit_path}")

# Scatter plot of CVaR energies
scatter_path = os.path.join(output_dir, "cvar_scatter.png")
plt.figure()
plt.scatter(range(1, max_iterations + 1), cvar_results, marker='o')
plt.title("CVaR Energies Across Iterations")
plt.xlabel("Iteration")
plt.ylabel("CVaR Energy")
plt.grid(True)
plt.savefig(scatter_path)
plt.close()
print(f"Saved CVaR scatter → {scatter_path}")

# Bitstring histogram
simulator = AerSimulator()
compiled_optimal = transpile(optimal_circuit, simulator)
job = simulator.run(compiled_optimal, shots=hyperParams["numShots"])
result = job.result()
counts = result.get_counts()
total_shots = sum(counts.values())
filtered = {k: v/total_shots for k, v in counts.items() if v/total_shots >= 0.02}
hist_path = os.path.join(output_dir, "bitstring_histogram.png")
plt.figure(figsize=(10, 5))
plt.bar(filtered.keys(), filtered.values(), edgecolor='black')
plt.xticks(rotation=45, ha='right')
plt.ylabel("Probability")
plt.xlabel("Bitstring")
plt.title("High-Probability Bitstrings (≥2%)")
plt.tight_layout()
plt.savefig(hist_path)
plt.close()
print(f"Saved bitstring histogram → {hist_path}")
