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

* Python 3.11+
* PyQt6
* `pyaudio`
* `wave`

```bash
pip install PyQt6 pyaudio
```

Clone this repository:

```bash
git clone https://github.com/yourusername/secure-messaging.git
cd secure-messaging
```

---

## Usage

Run the application:

```bash
 python interface.py userA
 python interface.py userB
```

**Features in action:**

1. **Start a new conversation**: Enter your username and your peer's username.
2. **Send text messages**: Type in the input box and press "Send".
3. **Send files**: Click the "Attach" button and select a file.
4. **Record audio**: Press the microphone icon to record and send.
5. **React to messages**: Click on a message and add an emoji reaction.

---

## Project Structure

```
secure-messenger/
│
├─ interface.py        # Main GUI application
├─ backgrounds/        # Customizable background images
├─ icons/              # Icons used in GUI
├─ models/             # Optional ML/audio models
├─ README.md           # This file
└─ history/            # Chat histories saved as JSON
```

---

## Technologies

* **Python 3.11** – Core language
* **PyQt6** – Graphical user interface
* **AES & RSA (simulated)** – Message encryption and key exchange
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
