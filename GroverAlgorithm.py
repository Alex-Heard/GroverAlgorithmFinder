# !pip install qiskit
# !pip install qiskit_aer

# Imports
from math import sqrt, pi
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import MCXGate
from qiskit_aer import AerSimulator

# Set problem size
n_bits = 12
target = 1        # in [0, 4095]
n = 1 << n_bits      # # 2^12 = 4096 states
target_bits = [(target >> i) & 1 for i in range(n_bits)]  # convert into binary

# Multi-controlled phase(z) flip -> flips the target if all control qubits are 1.
def mcz_gate(qc, data_qubits):
    target_state = data_qubits[-1]
    qc.h(target_state)
    # We want to apply the MCX gate len(data_qubits) times
    qc.append(MCXGate(len(data_qubits) - 1), data_qubits) # Append an X gate controlled by all but one qubit to the circuit, using the last qubit as the target.
    qc.h(target_state)

# Oracle: mark the target by applying phase flip -> essentially negating the state we are trying to find
def oracle(qc, data_qubits, target_bits):
    # map |target> -> |111...1| by flipping qubits where the target bit is 0
    zero_bit_positions = [i for i, bit in enumerate(target_bits) if bit == 0] # stores a list of integers
    qc.x(zero_bit_positions) # flips the state of each data qubit

    # apply phase flip on |111...1|
    mcz_gate(qc, data_qubits)

    # unmap back to the original basis
    qc.x(zero_bit_positions)

# Diffusion: flip all states around the average -> marked state is more likely to be measured
def diffuser(qc, data_qubits):
    qc.h(data_qubits)
    qc.x(data_qubits)
    mcz_gate(qc, data_qubits)
    qc.x(data_qubits)
    qc.h(data_qubits)

# Build circuit
data = QuantumRegister(n_bits, 'data')
classical = ClassicalRegister(n_bits, 'c') # Stores measurement
qc = QuantumCircuit(data, classical)

# Uniform superposition
qc.h(data)

# Grover iterations (≈ pi/4 * sqrt(N))
num_iterations = int((pi/4) * sqrt(n))  # 50 for N=4096
for i in range(num_iterations):
    oracle(qc, data, target_bits)
    diffuser(qc, data)

# Measure
qc.measure(data, classical)

# Simulate
backend = AerSimulator()
tqc = transpile(qc, backend) # Match actual backend config
result = backend.run(tqc, shots=200000).result()
counts = result.get_counts()

# Decode top result (reverse bitstring -> MSB..LSB)
bitstring, freq = max(counts.items(), key=lambda kv: kv[1])
found = int(bitstring, 2)

print(f"Most frequent: {found} (bits {bitstring})(frequency {freq})")
print(f"Target: {target}")

