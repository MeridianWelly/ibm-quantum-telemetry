# Prometheus Quantum Compiler: Empirical Telemetry & Hardware Benchmarks

## The Topological Routing Anomaly

This repository contains the empirical hardware telemetry evaluating a novel quantum routing architecture (Prometheus). The data documents a sustained physical anomaly that challenges the current Noisy Intermediate-Scale Quantum (NISQ) consensus. 

Standard heuristic compilers (e.g., SABRE) optimize strictly for minimum physical depth, operating on the premise that 2-qubit operations (SWAP gates) introduce local depolarizing noise, and thus, physical gate depth correlates negatively with quantum state fidelity. 

**The Observed Anomaly:** Our telemetry suggests that physical gate depth alone is not a sufficient predictor of computational degradation. Prometheus intentionally incurs massive physical depth penalties (inserting hundreds of additional SWAP gates to preserve global entanglement topologies), yet consistently yields lower output entropy and extracts stronger dominant signal peaks than shallow comparator circuits.

**The Working Hypothesis:** Preserving global entanglement structure and mathematically routing through specific hardware topologies may outweigh the local fidelity costs introduced by additional routing operations. 

---

## Zero-Trust Methodology & Air-Gapped IP

The proprietary routing heuristics and tensor matrices of the Prometheus compiler are strictly air-gapped pending patent protection. **We do not provide API access, black-box modules, or compiler binaries.** Instead, institutional review is conducted exclusively via zero-trust auditing. We have provided the raw hardware telemetry, unmodified IBM `job-result.json` payloads, transpiled OpenQASM circuits, and mathematical extraction tools for independent verification of the physical phenomena. Reviewers are invited to parse the payloads using their own extraction logic.

---

## Key Empirical Evidence

All executions were performed on the 156-qubit superconducting Heron architecture (`ibm_fez` and `ibm_kingston`). Control pipelines were strictly limited to IBM native compilation at Optimization Level 3 without readout error mitigation, exposing pure hardware behavior.

### 1. Deep-Scaling Matrix (200 Continuous Executions)
To definitively rule out statistical anomalies or localized hardware cooling cycles, we mapped 200 continuous, perfectly interleaved executions to observe the correlation between extreme gate depth and state preservation.

![Depth vs Entropy Scatter Plot](https://raw.githubusercontent.com/MeridianWelly/ibm-quantum-telemetry/main/assets/depth_vs_entropy_scatter.png)
*(Note: Visual representation of `prometheus_telemetry.csv`. Notice the clustering anomaly: Prometheus incurs ~1,000 extra physical routing gates yet consistently yields lower output entropy than the shallow SABRE benchmark.)*

### 2. Algorithm-Agnostic Peak Extraction
*Reference Job IDs: `d83f31ugbeec73amsoig` vs. `d83c1pg0bvlc73d38p2g`*

Rather than focusing solely on theoretical noise bounds, this baseline 5-qubit asymmetrical EfficientSU2 execution isolates the compiler's ability to extract the **intended dominant signal** (the `00000` ground state) from the background noise floor.

| Compiler Pipeline | Target Signal State | Target Extraction (Shots) | Top-5 State Retention |
| :--- | :---: | :---: | :---: |
| SABRE (Level 3) | `00000` | Failure to isolate | 688 / 2000 shots |
| **Prometheus Engine** | `00000` | **915 / 2000 shots** | **1861 / 2000 shots** |

### 3. The Live QFT-8 Blind Test
*Reference Job IDs: `d8o0o1jqv2lc7389ev00` vs. `d8o0o23qv2lc7389ev1g`*

Executed on a randomized, LLM-generated QFT-8 circuit. Prometheus absorbed a 4.4x SWAP penalty while successfully isolating the dominant signal peak.

| Metric | SABRE (Level 3) | Prometheus Engine | Delta / Impact |
| :--- | :--- | :--- | :--- |
| **Physical Depth** | 200 gates | **893 gates** | + 4.4x Penalty |
| **Shannon Entropy** | 7.7090 bits | 7.7317 bits | + 0.02 bits *(No meaningful separation observed)* |
| **Top State Peak** | 46 shots | **68 shots** | **+ 47% True Signal Extraction** |

### 4. Extreme Volumetric Testing (100,000 Shots)
To ensure the signal retention was not a localized anomaly, the engine was subjected to extreme physical depths and continuous execution loads. 

| Algorithm | Qubits | Compiler | Physical Depth | Shannon Entropy | KL Divergence | XEB |
| :--- | :---: | :--- | :--- | :--- | :--- | :--- |
| **QFT** | 8 | SABRE (Native) | 183 gates | 7.95 bits | 0.045 | 0.000 |
| **QFT** | **8** | **Prometheus** | **1,282 gates** | **6.60 bits** | **1.636** | **1.094\*** |
| **QAOA** | 12 | SABRE (Native) | 110 gates | 11.90 bits | 0.071 | 0.747 |
| **QAOA** | **12** | **Prometheus** | **227 gates** | **11.87 bits** | **0.121** | **0.669** |
| **QAOA** | 16 | SABRE (Native) | 139 gates | 15.41 bits | 5.079 | 0.581 |
| **QAOA** | **16** | **Prometheus** | **291 gates** | **15.36 bits** | **5.483** | **0.610** |

*\*Note on XEB Boundary: Under highly concentrated experimental output distributions where counts skew exponentially higher than chaotic Porter-Thomas models, the linear XEB estimator structurally shifts above unity under finite sampling ($N=100,000$).*

---

## Falsification Criteria

To facilitate rigorous scientific review, we establish the following experimental conditions under which the Prometheus routing hypothesis would be falsified:

1. **Statistical Convergence:** Replication showing Prometheus entropy metrics converging to, or exceeding, native SABRE performance as sample sizes (shots/runs) approach infinity.
2. **Hardware Dependency:** Complete failure to reproduce the topological insulation effect on independent superconducting processors.
3. **Randomized Benchmarks:** Randomized input-state executions consistently eliminating the depth-performance separation observed in structured algorithms.
4. **Routing Parity:** Alternative heuristic routing passes (e.g., `t|ket⟩` or randomized SWAP networks) generating matching signal extraction at equivalent physical depths.

---

## Data Room Verification

All data required to audit these claims is provided directly within this repository. To accommodate different security postures and hardware access levels, there are two paths for independent verification:

### Option A: Live Cloud Verification (Requires IBM Premium Access)
Reviewers with active premium IBM Quantum API tokens can tunnel directly into the Qiskit Runtime API to verify the historical job executions on the premium (Heron) mainframes.

1. Open `/scripts/cloud_telemetry_extractor.py` in any text editor.
2. Replace `"YOUR_IBM_TOKEN_HERE"` on line 53 with your active premium IBM API Token and save the file. *(Note: Free-tier tokens routing through the open-instance will return a "Job not found" error, as they lack clearance to view ledgers on premium hardware).*
3. Open your terminal, navigate to the repository folder, and run the script by passing any Job ID from the provided CSV ledgers.

**Example Execution:**
```bash
python scripts/cloud_telemetry_extractor.py --job d83c1pg0bvlc73d38p2g
