import os
import time
import requests
import csv
from datetime import datetime
from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit import qasm2, transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import ALAPScheduleAnalysis, PadDynamicalDecoupling
from qiskit.circuit.library import XGate

# --- CONFIGURATION ---
load_dotenv()
IBM_KEY = os.getenv("IBM_QUANTUM_TOKEN")
TARGET = "ibm_marrakesh"
DMZ_URL = "http://YOUR_SERVER_IP:8000"
API_KEY = "YOUR_CUSTOM_API_KEY"
ROUNDS = 30  # Increased to N=30 for statistical significance

RAW_QASM = """OPENQASM 2.0;
include "qelib1.inc";
qreg q[5]; creg c[5];

// Nontrivial initial state
x q[1]; x q[3];

// Layer 1: Entanglement + phase structure
h q[0]; cu1(pi/2) q[0], q[1]; cu1(pi/4) q[0], q[2];
h q[2]; cu1(pi/2) q[2], q[3]; cu1(pi/4) q[2], q[4];

// Layer 2: Cross-coupled interference
cx q[1], q[4]; cx q[3], q[0];
u3(pi/3, pi/5, pi/7) q[1]; u3(pi/4, pi/6, pi/8) q[3];

// Layer 3: Routing stress
cx q[0], q[4]; cx q[4], q[2]; cx q[2], q[1]; cx q[1], q[3];

// Reverse pressure
cx q[3], q[0]; cx q[4], q[1];

// Partial QFT-like closure
h q[4]; cu1(pi/2) q[3], q[4]; cu1(pi/4) q[2], q[4];
h q[3]; cu1(pi/2) q[2], q[3];

// Measurements
measure q[0] -> c[0]; measure q[1] -> c[1]; measure q[2] -> c[2]; measure q[3] -> c[3]; measure q[4] -> c[4];
"""

def align_telemetry(counts, mapping_ledger):
    aligned_counts = {}
    for state, freq in counts.items():
        state_list = list(state)
        aligned_state = ['0'] * len(state)
        state_list.reverse()
        for logical, physical in mapping_ledger.items():
            if physical < len(state_list):
                aligned_state[logical] = state_list[physical]
        aligned_state.reverse()
        aligned_str = "".join(aligned_state)
        aligned_counts[aligned_str] = aligned_counts.get(aligned_str, 0) + freq
    return aligned_counts

def get_top_states(counts, num=3):
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:num]

def run_automated_suite():
    print("\n[*] Authenticating with IBM Quantum Platform...")
    service = QiskitRuntimeService(channel="ibm_quantum_platform", token=IBM_KEY)
    backend = service.backend(TARGET)
    sampler = Sampler(mode=backend)
    
    benchmark_data = []
    dmz_layout_ledger = {0: 4, 1: 2, 2: 0, 3: 3, 4: 1} # DMZ Logic mapping

    print(f"\n[!] =========================================")
    print(f"[!] INITIATING MASSIVE HARVEST (N=30)")
    print(f"[!] WARNING: This will queue 60 jobs. Grab a coffee.")
    print(f"[!] =========================================")

    for i in range(ROUNDS):
        print(f"\n[*] --- ROUND {i+1}/{ROUNDS} ---")
        
        # 1. DMZ ROUTING
        res = requests.post(f"{DMZ_URL}/submit", json={"qasm": RAW_QASM, "target_hardware": TARGET}, headers={"x-api-key": API_KEY})
        job_id = res.json()["job_id"]
        
        opt_qasm = ""
        while True:
            time.sleep(3)
            status = requests.get(f"{DMZ_URL}/status/{job_id}", headers={"x-api-key": API_KEY}).json()
            if status["status"] == "COMPLETED":
                opt_qasm = status["result"][status["result"].find("OPENQASM 2.0;"):]
                break

        prom_circ = qasm2.loads(opt_qasm, custom_instructions=qasm2.LEGACY_CUSTOM_INSTRUCTIONS)
        pm = PassManager([ALAPScheduleAnalysis(backend.target.durations()), PadDynamicalDecoupling(backend.target.durations(), [XGate(), XGate()])])
        shielded_circ = pm.run(prom_circ)

        # 2. NATIVE ROUTING
        raw_native_circ = qasm2.loads(RAW_QASM)
        native_circ = transpile(raw_native_circ, backend=backend, optimization_level=3)

        # 3. EXECUTION
        print("    -> Firing payloads...")
        job_prom = sampler.run([shielded_circ])
        job_native = sampler.run([native_circ])
        
        print(f"    -> Awaiting Execution...")
        
        raw_prom_counts = job_prom.result()[0].data.c.get_counts()
        res_native = job_native.result()[0].data.c.get_counts()
        
        res_prom = align_telemetry(raw_prom_counts, dmz_layout_ledger)
        
        prom_top = get_top_states(res_prom)
        native_top = get_top_states(res_native)
        
        native_sharpness = sum(shots for _, shots in native_top)
        prom_sharpness = sum(shots for _, shots in prom_top)
        
        delta = ((prom_sharpness - native_sharpness) / native_sharpness) * 100 if native_sharpness > 0 else 0
        
        print(f"    [+] Round {i+1} Result: Prometheus ({prom_sharpness}) | Native ({native_sharpness}) | Delta: {delta:.2f}%")
        
        benchmark_data.append({
            "Round": i+1,
            "Prometheus_Top_3_Shots": prom_sharpness,
            "Native_Top_3_Shots": native_sharpness,
            "Advantage_Percentage": round(delta, 2),
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    # 4. EXPORT TO CSV
    filename = "prometheus_benchmarks_N30.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Round", "Prometheus_Top_3_Shots", "Native_Top_3_Shots", "Advantage_Percentage", "Timestamp"])
        writer.writeheader()
        writer.writerows(benchmark_data)
        
    print(f"\n[+] MASSIVE HARVEST COMPLETE. Data exported to {filename}.")

if __name__ == "__main__":
    run_automated_suite()