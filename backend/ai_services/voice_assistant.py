"""Voice assistant: speech in, grounded RAG answer, speech out."""
from backend.ai_services.speech import listen, speak, transcribe_file
from backend.rag.pipeline import answer

MAX_SPOKEN_CHARS = 700


def spoken_form(text: str) -> str:
    """Trim to something listenable. Drop the Source line; the UI shows citations."""
    body = text.split("Source:")[0].strip()
    if len(body) > MAX_SPOKEN_CHARS:
        body = body[:MAX_SPOKEN_CHARS].rsplit(".", 1)[0] + "."
    return body


def ask_by_voice(question: str | None = None, wav_path: str | None = None,
                 speak_reply: bool = True) -> dict:
    """question -> skip STT. wav_path -> transcribe a file. Neither -> microphone."""
    if question:
        heard = {"ok": True, "text": question}
    elif wav_path:
        heard = transcribe_file(wav_path)
    else:
        print("Listening ...")
        heard = listen()

    if not heard["ok"]:
        return {"ok": False, "error": heard.get("error"), "question": None}

    result = answer(heard["text"])
    reply = spoken_form(result["answer"])

    if speak_reply:
        speak(reply)

    return {
        "ok": True,
        "question": heard["text"],
        "answer": result["answer"],
        "spoken": reply,
        "sources": result["sources"],
        "grounded": result["grounded"],
        "usage": result["usage"],
    }


if __name__ == "__main__":
    import sys

    use_mic = "--mic" in sys.argv

    if use_mic:
        r = ask_by_voice()
    else:
        print("Synthesising the question to a WAV, then running the full pipeline.")
        print("(Use --mic to speak it instead.)\n")
        speak("What documents are required for a personal loan?", to_file="data/q.wav")
        r = ask_by_voice(wav_path="data/q.wav")

    if not r["ok"]:
        print(f"FAILED: {r['error']}")
        sys.exit(1)

    print(f"\nHEARD    : {r['question']}")
    print(f"GROUNDED : {r['grounded']}")
    print(f"TOKENS   : {r['usage']['total_tokens']}")
    print(f"\nANSWER\n{r['answer']}")
    print(f"\nSOURCES")
    for s in r["sources"][:3]:
        print(f"  {s['file']} | {s['section']} | score={s['score']}")
    print(f"\nSPOKEN ({len(r['spoken'])} chars) — played to your speakers.")
