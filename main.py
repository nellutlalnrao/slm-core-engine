from core.session.session_manager import SessionManager

def main():
    sm = SessionManager()

    # In real apps: user_id comes from auth / token / API key
    # Enables: 
    #   a) Multi-user isolation
    #   b) Secure session retrieval
    #   c) Future auth integration
    user_id = input("Enter user_id: ").strip()

    # get_or_create(...) Prevents:
    #   a) Session hijacking
    #   b) Cross-user memory leaks
    session = sm.get_or_create(user_id=user_id)
    print(f"Session ID: {session.session_id}")

    while True:
        q = input(">>> ").strip()

        if q.lower() in ("exit", "quit"):
            break

        if not q:
            continue

        sm.add_message(session, "user", q)
        print("✔ Message saved to session")

if __name__ == "__main__":
    main()