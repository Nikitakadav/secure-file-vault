# 🔐 Secure File Vault

## Project Title

**Secure File Vault – AES-256 File Encryption and Decryption System Using Python**

## Problem Statement

Files stored on a computer may contain sensitive or private information. If unauthorized users access these files, the information can be misused. This project provides a secure way to encrypt files and protect them using a password.

## Objectives

* To encrypt files using AES-256.
* To decrypt files using the correct password.
* To protect files from unauthorized access.
* To detect incorrect passwords and modified files.
* To provide a simple and user-friendly GUI.

## Technologies Used

* Python
* Tkinter
* PyCryptodome
* VS Code

## Python Libraries Used

* `tkinter` – Graphical User Interface
* `Crypto.Cipher` – AES encryption/decryption
* `Crypto.Protocol.KDF` – PBKDF2 key generation
* `Crypto.Hash` – SHA-256
* `Crypto.Random` – Random salt generation
* `os` – File and path handling

## Cryptography / Network Security Concepts Used

* AES-256 Symmetric Encryption
* PBKDF2
* SHA-256
* Random Salt
* AES-EAX Authentication
* Password Strength Checking
* Data Integrity Verification

## Key Features

* AES-256 file encryption
* Password-based key generation
* File decryption
* Password strength checker
* Wrong password detection
* Tampered-file detection
* Safe output filename generation
* Simple Tkinter GUI

## System Requirements

**Hardware:**

* Computer/Laptop
* Minimum 4 GB RAM

**Software:**

* Windows/Linux/macOS
* Python 3.x
* VS Code or any Python IDE

## How to Install and Run

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_LINK
```

### 2. Open the Project Folder

```bash
cd secure-file-vault
```

### 3. Install Required Library

```bash
pip install pycryptodome
```

### 4. Run the Application

```bash
python app.py
```

## Screenshots

### Main GUI

![Main GUI](screenshots/main_gui.jpg)

### File Encryption

![Encryption](screenshots/encryption.jpg)

### File Decryption

![Decryption](screenshots/decryption.jpg)

### Wrong Password Detection

![Wrong Password](screenshots/wrong_password.jpg)

## Project Demonstration

The user selects a file and enters a password. The application generates an AES-256 key using PBKDF2, SHA-256 and a random salt. The file is then encrypted using AES-EAX and saved with the `.enc` extension.

For decryption, the encrypted file and password are provided. The application verifies the authentication tag and decrypts the file only when the password and encrypted data are valid.

## GitHub Repository Link

**Repository:** 

