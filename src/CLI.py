import os
import json

from exchange_flow import (
    setupkeysElgamal,
    sender_send_session_key,
    receiver_receive_session_key
)

from secure_messaging_full import (
    secure_encrypt,
    secure_decrypt
)

from El_gamal_module import load_keys


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_DIR = os.path.join(BASE_DIR, "messages")
os.makedirs(MESSAGES_DIR, exist_ok=True)


# ---------------------------------------------------------
# Messaging
# ---------------------------------------------------------

def send_message(sender, receiver, aes_key):
    message = input("\nType your message: ")
    _, my_private = setupkeysElgamal(sender)

    package = secure_encrypt(
        message,
        aes_key,
        my_private
    )

    filename = f"{receiver}_from_{sender}_{len(os.listdir(MESSAGES_DIR)) + 1}.json"
    filepath = os.path.join(MESSAGES_DIR, filename)

    with open(filepath, "w") as f:
        json.dump(package, f, indent=4)

    print(f"✔ Message encrypted and saved: {filename}")

def read_messages(user, aes_key):
    print(f"\n📬 Messages for {user}:")

    msgs = [
        f for f in os.listdir(MESSAGES_DIR)
        if f.startswith(f"{user}_from_")
    ]

    if not msgs:
        print("No messages found.")
        return

    for filename in sorted(msgs):
        filepath = os.path.join(MESSAGES_DIR, filename)

        sender = filename.split("_")[2]  # userA / userB
        sender_public_key, _ = load_keys(sender)

        with open(filepath, "r") as f:
            package = json.load(f)

        try:
            plaintext, valid = secure_decrypt(
                package,
                aes_key,
                sender_public_key
            )

            print(f"\nFrom {sender}:\n{plaintext}")
            print("✔ Valid signature" if valid else "❌ Invalid signature")

            # 🔥 DELETE AFTER SUCCESSFUL READ
            os.remove(filepath)

        except Exception as e:
            print(f"❌ Failed to decrypt {filename}: {e}")

# ---------------------------------------------------------
# User selection
# ---------------------------------------------------------

def choose_user():
    while True:
        print("Choose user for this terminal:")
        print("1) User A")
        print("2) User B")
        choice = input("> ")

        if choice == "1":
            return "userA"
        elif choice == "2":
            return "userB"
        else:
            print("Invalid choice.\n")


# ---------------------------------------------------------
# AES key flow
# ---------------------------------------------------------

def choose_aes_key_source(me, peer):
    while True:
        print("AES key option:")
        print("1) Generate and send AES key")
        print("2) Receive AES key")

        choice = input("> ")

        if choice == "1":
            aes_key = sender_send_session_key(peer)
            print(f"✔ AES key sent to {peer}")
            return aes_key

        elif choice == "2":
            aes_key = receiver_receive_session_key(me)
            if aes_key is None:
                print("↩ No AES key yet. Try again.\n")
                continue
            print("✔ AES key received.")
            return aes_key

        else:
            print("Invalid choice.\n")


# ---------------------------------------------------------
# Messaging CLI
# ---------------------------------------------------------
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
KEYS_DIR = os.path.join(PROJECT_ROOT, "keys")

def clear_directory(dir_path):
    if not os.path.exists(dir_path):
        return

    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"⚠ Could not delete {file_path}: {e}")



def messaging_cli(me, peer, aes_key):
    while True:
        print("\nChoose an option:")
        print("1) Send a message")
        print("2) Read received messages")
        print("3) Exit")

        choice = input("> ")

        if choice == "1":
            send_message(me, peer, aes_key)

        elif choice == "2":
            read_messages(me, aes_key)

        elif choice == "3":
            print("🧹 Clearing keys and messages...")

            clear_directory(KEYS_DIR)
            clear_directory(MESSAGES_DIR)

            print("✔ keys/ and messages/ cleared.")
            print("Exiting.")
            break

        else:
            print("Invalid choice.")


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

def main():
    me = choose_user()
    peer = "userB" if me == "userA" else "userA"

    print(f"\n🧍 This terminal is: {me}")
    print(f"🧍 Other terminal: {peer}\n")
    my_public, my_private = setupkeysElgamal(me)


    # AES session key setup
    aes_key = choose_aes_key_source(me, peer)

    # Messaging loop
    messaging_cli(me, peer, aes_key)


if __name__ == "__main__":
    main()
