# Grover's Quantum Search Algorithm (12-Qubit / 4096 States)

A scalable, pure gate-level implementation of **Grover's Search Algorithm** built in Python with **Qiskit** and simulated using `AerSimulator`. The circuit demonstrates quadratic quantum speedup by isolating a target element out of $N = 4096$ states ($n = 12$ qubits) using automated oracle mapping and amplitude amplification diffusion operators.

---

## Technical Overview

Grover's algorithm searches an unstructured database of size $N = 2^n$ in $\mathcal{O}(\sqrt{N})$ queries compared to the classical complexity $\mathcal{O}(N)$.

Key components of this implementation:
- **Uniform Superposition:** Initializes the 12-qubit register into equal superposition across all 4,096 basis states via parallel Hadamard transformations.
- **Bitwise Phase Oracle:** Dynamically synthesizes the marking operator for any arbitrary integer target by applying bit-flip ($X$) masks to map $\vert{}x_{\text{target}}\rangle \to \vert{}11\dots1\rangle$, executing a multi-controlled phase flip, and uncomputing the basis transformations.
- **Multi-Controlled Phase Flip ($MCZ$):** Conjugates a multi-controlled Toffoli gate (`MCXGate`) across $n-1$ controls with target Hadamard gates to implement an $n$-qubit reflection operator.
- **Grover Diffuser (Inversion About the Mean):** Implements $2\vert{}\psi\rangle\langle\psi\vert{}$ - I$ using $H^{\otimes n} X^{\otimes n} (MCZ) X^{\otimes n} H^{\otimes n}$ to amplify the probability amplitude of the marked state while suppressing non-target amplitudes.
- **Optimal Step Scheduling:** Automatically computes the theoretical optimal iteration count $R \approx \left\lfloor \frac{\pi}{4}\sqrt{N} \right\rfloor$ ($R = 50$ iterations for $N = 4096$) to avoid over-rotation.

---

## Circuit Specifications

- **Register Width:** 12 Quantum bits (`QuantumRegister`), 12 Classical bits (`ClassicalRegister`)
- **State Space:** $2^{12} = 4096$ orthogonal states
- **Grover Iterations:** 50 amplification cycles
- **Simulation Shots:** 200,000

---

## Prerequisites

```bash
pip install qiskit qiskit-aer
