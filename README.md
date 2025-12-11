# Adjusted ElGamal for Files  
### Cryptographic Implementation Analysis & Experimental Framework

This repository contains an enhanced implementation of the **ElGamal public-key cryptosystem**, specifically redesigned to support **efficient file encryption, decryption, and large prime generation**.  
It provides a modular framework for evaluating different primality-testing algorithms, optimized key generation, file chunking, and multithreading techniques.

---

## 🚀 Introduction

Classical ElGamal suffers from limitations such as:

- Slow key generation  
- Inefficient ciphertext expansion  
- Inability to encrypt large files directly  
- Slow encryption/decryption for large data  

This project implements **Adjusted ElGamal**, improving both **security** and **performance** through:

- Fast large-prime generation (Miller–Rabin, AKS, Solovay–Strassen)
- Extended Euclidean Algorithm for faster key generation  
- File block processing (chunk-based encryption)
- Multithreading to accelerate computation  
- Preprocessing optimizations using `ByteArrayIO` and `StringIO`

This framework allows researchers to compare performance across multiple configurations.

---

## 📦 Installation Requirements

Before running the program, ensure your Python environment includes the following packages (all are standard libraries except DebugTimer):

```
math
random
time
logging
sys
pickle
hashlib
functools
queue
io
threading
DebugTimer # custom / external helper (included in project if provided)
```

No additional third-party dependencies are required.

---

## ▶️ How to Run

Run the full experimental pipeline:

```
python3 testAll.py
```

This will:

- Generate large primes using three different algorithms

- Run Adjusted ElGamal encryption & decryption

- Compare single-thread vs multithread performance

- Show the processed-data optimization results

## 📁 Project Structure & File Explanation

---

### **🔢 Part 1 — Large Prime Generation**

| Algorithm              | File                         |
|------------------------|------------------------------|
| Miller–Rabin           | `Large_Prime_Generation.py`  |
| AKS primality test     | `AKS_algorithm.py`           |
| Solovay–Strassen test  | `solovay_strassen.py`        |

These modules allow consistent comparison of prime length, performance, and accuracy.

---

### **🔐 Part 2 — Adjusted ElGamal Encryption & Decryption**

| Component                        | Description                           | File                |
|----------------------------------|---------------------------------------|---------------------|
| Original ElGamal + Large Prime  | Baseline implementation               | `OurMethod.py`      |
| File Encryption (single thread) | Supports `.txt` and images            | `File_encryption.py` |
| File Encryption (multithreading)| Enhanced speed, `.txt` only           | `improved_plus.py`  |

Enhancements include:

- **Chunk-based processing**  
- **Fast modular inverse using Extended Euclid**  
- **Multithreaded block-level encryption**  
- **Data preprocessing (ByteArrayIO / StringIO) to minimize conversion cost**

---

### **🧪 Test Suite**

| File         | Description                                           |
|--------------|-------------------------------------------------------|
| `testAll.py` | Runs all examples, experiments, and comparisons       |

This is the recommended entry point.

---

## 📊 Experimental Summary

Based on our implementation:

---

### **🔢 Large Prime Generation Performance**

| Algorithm         | Performance                                   |
|------------------|------------------------------------------------|
| Miller–Rabin      | Fastest (≈309-digit prime in ~0.15s)          |
| AKS              | Deterministic but slower                       |
| Solovay–Strassen | Correct but extremely slow for large primes    |

---

### **⚡ Adjusted ElGamal Performance**

Multithreading + data preprocessing significantly accelerates both encryption and decryption:

| Method                        | Encryption Time | Decryption Time |
|-------------------------------|-----------------|-----------------|
| Single-threaded               | ~10.5s          | ~8.0s           |
| Multithreaded + Preprocessing | ~5.7s           | ~5.8s           |

---

## 🧩 Techniques Used

- Modular arithmetic & primality testing  
- Public-key cryptography  
- Multithreaded task queues  
- Python byte-stream optimization  
- Performance benchmarking


