from src.session_manager import JumiaChatManager

def main():
    print("--- Jumia Oral Assistant (Sprint 12: Hygiène & Alignement) ---")
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

    print_response(user_id, "Salam, bghit chi laptop m3lem l-gaming")
    print_response(user_id, "Chi haja t-koun rkhisa l-estghlal l-3adi (bureautique)")

if __name__ == "__main__":
    main()
