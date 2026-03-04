from src.session_manager import JumiaChatManager

def main():
    print("--- Jumia Oral Assistant (Sprint 8) ---")
    chat = JumiaChatManager()
    
    user_id = "user_demo"
    
    def print_response(user, msg):
        res = chat.handle_message(user, msg)
        if isinstance(res, dict):
            print(f"\n[{user}]: {msg}")
            print(f"\n[Assistant]: {res.get('text')}")
            if res.get('media_url'):
                print(f" (Media: {res.get('media_url')})")
        else:
            print(f"\n[{user}]: {msg}")
            print(f"\n[Assistant]: {res}")

    print_response(user_id, "Salam!")
    print_response(user_id, "Ana f Casablanca")
    print_response(user_id, "Bghit chi laptop mzyan")

if __name__ == "__main__":
    main()
