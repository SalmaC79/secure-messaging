---

# Secure Messenger 🛡️✉️

A **Python-based secure messaging application** featuring end-to-end encryption, file and audio sharing, and a modern PyQt6 GUI. Designed for educational and practical purposes in **cybersecurity and networking**, this project demonstrates cryptography integration with real-time messaging.

---

## Table of Contents

1. [Features](#features)
2. [Demo](#demo)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Technologies](#technologies)
7. [Security](#security)
8. [License](#license)

---

## Features

* 🔒 **End-to-end encryption:** Hybrid cryptography using AES for message encryption and RSA for key exchange.
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

![Messenger Screenshot](./screenshots/demo.png)
<img width="1600" height="838" alt="image" src="https://github.com/user-attachments/assets/50a1cf89-c151-4046-9582-46b5ec80faea" />


---

## Installation

### Requirements

Clone this repository:

```bash
git clone https://github.com/yourusername/secure-messaging.git
cd secure-messaging
```
Then run this command :

```bash
 pip install -r requirements.txt 
```
---

## Usage

Run the application in two split terminals, each command in a terminal:

--> User A terminal :

```bash
 python interface.py userA
```
--> User B terminal :

```bash
 python interface.py userB
```
---

## Project Structure

```
.
├── Readme files/ #for each module, we produced a readme file
├── Test/
├── Test_files/
├── src/
│   ├── GUI
│   └── CLI functions #the modules of our project and the cli
├── tests/ #our modules tests
├── venv/
├── .gitignore
└── requirements.txt
```

---

## Technologies

* **Python 3.11** – Core language
* **PyQt6** – Graphical user interface
* **AES & RSA (via PyCryptodome)** – Message encryption and key exchange
* **hashlib** – Hashing for message integrity and signatures
* **Wave & PyAudio** – Audio recording and playback
* **JSON** – Local message history storage

---

## Security

* Uses **hybrid cryptography**: AES for encrypting messages, RSA for exchanging keys.
* Messages are signed and verified (simulated) to ensure integrity.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---
