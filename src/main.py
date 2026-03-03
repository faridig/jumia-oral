from src.session_manager import JumiaChatManager

def main():
    print("--- Jumia Oral Assistant (Sprint 6) ---")
    chat = JumiaChatManager()
    
    user_id = "user_demo"
    print("\n[Assistant]: " + chat.handle_message(user_id, "Salam!"))
    print("\n[User]: Ana f Casablanca")
    print("\n[Assistant]: " + chat.handle_message(user_id, "Ana f Casablanca"))
    print("\n[User]: Bghit chi laptop mzyan")
    print("\n[Assistant]: " + chat.handle_message(user_id, "Bghit chi laptop mzyan"))

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
