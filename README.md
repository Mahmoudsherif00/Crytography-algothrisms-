# Security Cryptography Algorithms

A modern platform for understanding and implementing cryptographic algorithms with real-world applications. Explore classical ciphers, modern symmetric/asymmetric encryption, and secure hashing functions seamlessly through a beautiful, responsive web interface.

## 🌟 Overview

This project provides a professional, educational, and fully functional suite of cryptographic algorithms implemented purely in Python. The backend logic relies entirely on Python's standard libraries, ensuring maximum transparency, audibility, and zero external cryptographic dependencies (no `pycryptodome` or `cryptography` packages required). The frontend is powered by Streamlit, wrapped in a custom dark-themed UI with glassmorphism aesthetics.

## ✨ Features

- **Symmetric Algorithms:**
  - **AES (Advanced Encryption Standard):** Block cipher encryption and decryption.
  - **DES (Data Encryption Standard):** Classic block cipher.
  - **RC4:** Stream cipher implementation.
  - **Playfair Cipher:** Digraph substitution cipher.
  - **Vernam Cipher (One-Time Pad):** XOR-based perfect secrecy cipher.
  - **Vigenère Cipher:** Polyalphabetic substitution cipher.
- **Asymmetric Algorithms:**
  - **RSA:** Public-key cryptosystem with integrated prime generation, key-pair creation, and encryption/decryption handling.
- **Hashing Algorithms:**
  - **MD5, SHA-1, SHA-256:** Cryptographic hash functions generating fixed-size digests.
- **Interactive UI:**
  - Responsive, modern dashboard with animated components.
  - Real-time execution and error handling.

## 🛠️ Project Structure

```text
Security/
├── app.py                # Main Streamlit Dashboard Application
├── requirements.txt      # Project dependencies
├── README.md             # Project documentation
├── aes_cipher.py         # AES implementation
├── des_cipher.py         # DES implementation
├── hashing.py            # MD5, SHA-1, SHA-256 implementations
├── playfair.py           # Playfair implementation
├── rc4_cipher.py         # RC4 implementation
├── rsa_cipher.py         # RSA implementation
├── vernam.py             # Vernam implementation
└── vigenere.py           # Vigenere implementation
```

## 🚀 Installation & Setup

### For Windows

1. **Clone the repository** (or download the source):
   ```bash
   git clone https://github.com/yourusername/Security-Cryptography-Algorithms.git
   cd Security-Cryptography-Algorithms
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv env
   ```

3. **Activate the environment:**
   ```bash
   env\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### For Mac / Linux

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/Security-Cryptography-Algorithms.git
   cd Security-Cryptography-Algorithms
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv env
   ```

3. **Activate the environment:**
   ```bash
   source env/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 🤝 Contribution Guide

Contributions are always welcome! If you'd like to improve the algorithms, add new ones, or enhance the UI, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

**GitHub Repository:** [https://github.com/yourusername/Security-Cryptography-Algorithms](https://github.com/yourusername/Security-Cryptography-Algorithms)
"# Security-Project-" 
