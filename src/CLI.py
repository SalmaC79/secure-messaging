import os
from El_gamal_module import generate_keypair, save_keys, load_keys



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(BASE_DIR, "keys")
os.makedirs(KEYS_DIR, exist_ok=True)

def choose_user():
    while True:
        print("Choose user:")
        print("1) User A")
        print("2) User B")
        choice = input("> ")
        if choice == "1":
            return "userA"
        elif choice == "2":
            return "userB"
        else:
            print("Invalid choice. Try again.")

def ensure_user_keys(username):
    pub_file = os.path.join(KEYS_DIR, f"{username}_public.json")
    priv_file = os.path.join(KEYS_DIR, f"{username}_private.json")

    if not os.path.exists(pub_file) or not os.path.exists(priv_file):
        print(f"[+] Generating ElGamal keys for {username}...")
        public, private = generate_keypair(bits=256)
        save_keys(os.path.join(KEYS_DIR, username), public, private)
    else:
        print(f"[✓] Keys already exist for {username}")

def main():
    user = choose_user()

    # Ensure keys exist
    ensure_user_keys("userA")
    ensure_user_keys("userB")

    # Load own keys
    public, private = load_keys(os.path.join(KEYS_DIR, user))
    


if __name__ == "__main__":
    main()
