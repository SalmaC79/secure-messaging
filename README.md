
---

# Secure Messenger - *VaultTalk* 🛡️✉️

A **Python-based secure messaging application** featuring end-to-end encryption, file and audio sharing, and a modern PyQt6 GUI. Designed for educational and practical purposes in **cybersecurity and networking**, this project demonstrates cryptography integration with real-time messaging.

---

## Table of Contents

1. [Features](#features)
2. [Demo](#demo)
3. [Installation](#installation)
4. [Usage](#usage)
5. [CLI Mode](#cli-mode)
6. [Project Structure](#project-structure)
7. [Technologies](#technologies)
8. [Security](#security)
9. [License](#license)

---

## Features

* 🔒 **End-to-end encryption:** Hybrid cryptography using AES for message encryption and RSA/ElGamal for key exchange.
* 🎧 **Audio messaging:** Record and send audio clips directly through the interface.
* 📁 **File sharing:** Send files of any type with intuitive file bubbles and previews for images, PDFs, and audio.
* 💬 **Message reactions:** React to messages with emojis, similar to modern chat apps.
* 🖥️ **PyQt6 GUI:** Smooth and responsive user interface with dark mode and animated elements.
* ⏱️ **Timestamping:** Automatically timestamped messages.
* ✅ **Message verification:** Simulated signature verification to ensure message integrity.
* 🗂️ **Message history:** Persistent chat history saved locally in JSON format.
* 🎨 **Customizable backgrounds:** Support for background images in the chat window.

---

## Demo

<img width="1600" height="838" alt="VaultTalk GUI Demo" src="https://github.com/user-attachments/assets/50a1cf89-c151-4046-9582-46b5ec80faea" />

---

## Installation

### Requirements

Clone this repository:

```bash
git clone https://github.com/yourusername/secure-messaging.git
cd secure-messaging
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

---

## Usage

Run the application in **two split terminals**, each command in a terminal:

**User A terminal:**

```bash
python interface.py userA
```

**User B terminal:**

```bash
python interface.py userB
```

---

## CLI Mode

VaultTalk provides a **Command-Line Interface (CLI)** to explore how secure messaging works behind the scenes.
It demonstrates AES session key generation, message/file encryption and decryption, and signature verification.

**To run the CLI:**

```bash
python interface.py
```

The CLI allows you to:

1. Choose your user (`userA` / `userB`).
2. Send or receive AES session keys using ElGamal.
3. Send messages or files with encryption and signature.
4. Read received messages or files and verify signatures.
5. Clear all keys, messages, and files after use.

This mode is ideal for **testing, debugging, and understanding the cryptography flow** without the GUI.

---

## Project Structure

```
.
├── Readme files/           # Individual README files for modules
├── Test/
├── Test_files/
├── src/
│   ├── GUI                # GUI modules
│   └── CLI functions      # Core project and CLI modules
├── tests/                 # Unit tests for modules
├── venv/
├── .gitignore
└── requirements.txt
```

---

## Technologies

* **Python 3.11** – Core language
* **PyQt6** – Graphical user interface
* **AES & RSA/ElGamal (via PyCryptodome)** – Message encryption and key exchange
* **hashlib** – Hashing for message integrity and signatures
* **Wave & PyAudio** – Audio recording and playback
* **JSON** – Local message history storage

---

## Security

* Uses **hybrid cryptography**: AES for encrypting messages and RSA/ElGamal for exchanging keys.
* Messages and files are signed and verified (simulated) to ensure integrity.
* AES session keys are generated dynamically for each session and exchanged securely.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

