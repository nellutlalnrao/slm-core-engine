from core.session.session_manager import SessionManager
from core.context.context_builder import ContextBuilder
from core.token.token_limiter import decide_max_tokens
from llama_cpp import Llama

def main():
    # -----------------------------
    # Load Model
    # -----------------------------
    MODEL_PATH = "models/Phi-3-mini-4k-instruct-q4.gguf"

    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=4096,
        n_threads=4,
        n_batch=32,
        temperature=0.6,
        top_p=0.9,
        verbose=False
    )

    print("✅ Model loaded")

    # -----------------------------
    # Init Session + Context Builder
    # -----------------------------
    sm = SessionManager()
    context_builder = ContextBuilder(session_manager=sm, max_messages=10)

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

    # -----------------------------
    # Main Chat Loop
    # -----------------------------
    while True:
        q = input(">>> ").strip()

        if q.lower() in ("exit", "quit"):
            print("Session ended")
            break

        if not q:
            continue

        # Save user message
        sm.add_message(session, "user", q)
        print("✔ Message saved to session")

        # -----------------------------
        # Phase-2: Build Context
        # -----------------------------
        context = context_builder.build(session)
        prompt = (
            "<|system|>\n"
            "You are a helpful assistant. Answer clearly and concisely.\n"
            "<|context|>\n"
            f"{context}\n"
            "<|user|>\n"
            f"{q}\n"
            "<|assistant|>\n"
        )

        max_tokens = min(decide_max_tokens(q), 300)  # hard safety cap
        # -----------------------------
        # Inference
        # -----------------------------
        output = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=0.6,
            top_p=0.9,
            stop=["<|user|>", "<|assistant|>", "<|context|>"]
        )

        answer = output["choices"][0]["text"].strip()
        answer = answer.replace("<|context|>", "").strip() # Safety cleanup (in case model leaks tokens)
        print(answer)

        # Save assistant response
        sm.add_message(session, "assistant", answer)        

if __name__ == "__main__":
    main()