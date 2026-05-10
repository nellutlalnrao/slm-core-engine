from core.session.session_manager import SessionManager
from core.context.context_builder import ContextBuilder
# from core.token.token_limiter import decide_max_tokens
from core.model.llm_client import LLMClient
from core.completion.answer_orchestrator import AnswerOrchestrator
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

    llm_client = LLMClient(llm)
    orchestrator = AnswerOrchestrator(llm_client)
    print("✅ Model loaded")

    # -----------------------------
    # Init Session + Context Builder
    # -----------------------------
    sm = SessionManager()
    context_builder = ContextBuilder(
        session_manager=sm,
        recent_window=6,        # how many recent messages to keep verbatim
        max_prompt_tokens=3500  # token budget for prompt
    )

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
            "You are a helpful assistant. Answer clearly and concisely."
            "Give a complete, well-structured answer. "
            "Do not stop mid-response.\n"
            "<|user|>\n"
            f"{context}\n"
            f"{q}\n"
            "<|assistant|>\n"
        )

        # -----------------------------
        # Auto-Completion Orchestrated Inference
        # -----------------------------
        # max_tokens = min(decide_max_tokens(q), 300)  # hard safety cap
        final_answer = orchestrator.get_complete_answer(
            question=prompt
        )

        final_answer = final_answer.replace("<|context|>", "").strip()

        print(final_answer)
        # -----------------------------
        # Inference
        # -----------------------------
        # output = llm(
        #    prompt,
        #    max_tokens=max_tokens,
        #    temperature=0.6,
        #    top_p=0.9,
        #    stop=["<|user|>", "<|assistant|>"]
        #)#

        #answer = output["choices"][0]["text"].strip()
        #answer = answer.replace("<|context|>", "").strip() # Safety cleanup (in case model leaks tokens)
        # print(answer)

        # Save assistant response
        sm.add_message(session, "assistant", final_answer)        

if __name__ == "__main__":
    main()