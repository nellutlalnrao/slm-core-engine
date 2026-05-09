from core.session.session_manager import SessionManager

sm = SessionManager()

session = sm.get_or_create()
print("Session ID:", session.session_id)

while True:
    q = input(">>> ")
    if q.lower() == "exit":
        break

    sm.add_message(session, "user", q)
    print("Saved to session.")