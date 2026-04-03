from src.session_manager import JumiaChatManager

def main():
    print("--- 🛒 Jumia Oral : Session Interactive (Mode Client) ---")
    print("Tapez 'exit' pour quitter.\n")
    chat = JumiaChatManager()
    user_id = "user_demo"
    
    while True:
        user_input = input("\n[Vous] (Darija/Fr) : ")
        if user_input.lower() in ["exit", "quit", "quitter"]:
            print("Besseha! A bientot.")
            break
            
        res = chat.handle_message(user_id, user_input)
        
        # Affichage propre
        if isinstance(res, dict):
            print(f"\n[Jumia Bot] 🤖 : {res.get('text')}")
            if res.get('text_tts'):
                print(f"\n📢 (Audio Phoenix) : {res.get('text_tts')}")
        else:
            print(f"\n[Jumia Bot] 🤖 : {res}")

if __name__ == "__main__":
    main()
