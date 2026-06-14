# Prometheus Dynamics: IBM Quantum Execution Telemetry

This repository contains the raw hardware telemetry, IBM Primitive Unified Blocs (PUBS), and verification metrics associated with the **Prometheus Engine** empirical benchmarks. 

Prometheus is an active-avoidance dynamic routing compiler designed to preserve computational structure at transpilation depths beyond conventional hardware expectations. This repository serves as the public data room for independent verification of observed hardware measurements.

##  Methodology

All benchmark results were generated using identical logical circuits, identical shot counts, identical IBM Quantum calibration windows, and side-by-side compilation.

* **Hardware:** IBM Quantum Systems `ibm_kingston` and `ibm_fez` (both utilizing the 156-qubit Heron r2 processor architecture).
* **Baseline Transpilation:** Native Qiskit SABRE (`optimization_level=3`).
* **Test Payloads:** Structured logic networks including QFT, QAOA, Bernstein-Vazirani (BV), and GHZ states.
* **Execution Parameters:** 4,096 shots (`ibm_fez`) and 100,000 shots (`ibm_kingston`) to force extreme thermal and decoherence thresholds.

##  Repository Structure

The raw data is segmented into two primary archives corresponding to the benchmarks detailed on the Prometheus Dynamics website:

### 1. `heron_entropy_telemetry.zip`
Contains the execution logs and cryptographic hardware proofs for the Shannon Entropy noise mitigation benchmarks.
* `session-3296b2d4-f65f-4f10-8e3f-eaf52c0c5cb9-jobs.csv`: The master ledger of 34 contiguous jobs executed on `ibm_fez`, recording the paired SABRE vs. Prometheus executions.
* `session-3296b2d4-f65f-4f10-8e3f-eaf52c0c5cb9-info.json`: The raw IBM metadata confirming the hardware environment, batch mode execution, and calibration window timestamps.

### 2. `ibm_kingston_pubs.zip`
Contains the raw JSON result files and PUBS metadata for the extreme depth stress tests executed on `ibm_kingston`.
* Includes the 100,000-shot execution bitstrings that yielded the verifiable 6,099 executed gate depth and anomalous XEB preservation.

##  Proprietary Intellectual Property Notice

To protect the core intellectual property of the Prometheus active-avoidance routing topology, **we are intentionally withholding the post-transpilation Prometheus OpenQASM payloads.**

We provide the Logical QASM (input architecture), the native SABRE QASM (baseline reference), and the raw IBM PUBS Bitstrings (output execution data). Executed gate depths, shot densities, and runtime parameters are natively timestamped and verifiable via the raw IBM output arrays. Evaluation should be based exclusively on reproducible, hardware-observed performance rather than internal algorithmic disclosure.

##  Verification

Reviewers are encouraged to parse the IBM PUBS JSON files and run standard linear cross-entropy (XEB) and Shannon Entropy calculations against the raw bitstrings to independently verify the expectation values.
