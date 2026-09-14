"""Speech-to-text and text-to-speech over Entra ID auth.

The Speech SDK requires an unusual token format: aad#{resourceId}#{aadToken}.
Tokens expire in roughly 10 minutes, so the config is rebuilt per call.
"""
import azure.cognitiveservices.speech as speechsdk
from config.settings import get_settings, credential

RECOGNITION_LANGUAGE = "en-IN"
SYNTHESIS_VOICE = "en-IN-NeerjaNeural"


def speech_config() -> speechsdk.SpeechConfig:
    s = get_settings()
    if not s.ai_services_resource_id:
        raise RuntimeError("AI_SERVICES_RESOURCE_ID is not set in .env")
    token = credential().get_token("https://cognitiveservices.azure.com/.default").token
    cfg = speechsdk.SpeechConfig(
        auth_token=f"aad#{s.ai_services_resource_id}#{token}",
        region=s.azure_region)
    cfg.speech_recognition_language = RECOGNITION_LANGUAGE
    cfg.speech_synthesis_voice_name = SYNTHESIS_VOICE
    return cfg


def listen(timeout_seconds: int = 10) -> dict:
    """Capture one utterance from the default microphone."""
    cfg = speech_config()
    cfg.set_property(speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs,
                     str(timeout_seconds * 1000))
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=cfg,
        audio_config=speechsdk.audio.AudioConfig(use_default_microphone=True))

    result = recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {"ok": True, "text": result.text}
    if result.reason == speechsdk.ResultReason.NoMatch:
        return {"ok": False, "text": "", "error": "no speech recognised"}
    cancel = result.cancellation_details
    return {"ok": False, "text": "",
            "error": f"{cancel.reason}: {cancel.error_details}"}


def transcribe_file(path: str) -> dict:
    """Transcribe a WAV file. Useful for repeatable tests without a microphone."""
    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config(),
        audio_config=speechsdk.audio.AudioConfig(filename=path))
    result = recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return {"ok": True, "text": result.text}
    return {"ok": False, "text": "", "error": str(result.reason)}


def speak(text: str, to_file: str | None = None) -> dict:
    """Synthesise speech to the default speaker, or to a WAV file."""
    audio_cfg = (speechsdk.audio.AudioOutputConfig(filename=to_file) if to_file
                 else speechsdk.audio.AudioOutputConfig(use_default_speaker=True))
    synth = speechsdk.SpeechSynthesizer(speech_config=speech_config(),
                                        audio_config=audio_cfg)
    result = synth.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return {"ok": True, "audio_bytes": len(result.audio_data), "file": to_file}
    cancel = result.cancellation_details
    return {"ok": False, "error": f"{cancel.reason}: {cancel.error_details}"}


if __name__ == "__main__":
    import sys

    print("1. Building speech config (validates Entra ID auth) ...")
    try:
        speech_config()
        print("   OK")
    except Exception as e:
        print(f"   FAILED: {e}")
        sys.exit(1)

    print("\n2. Text-to-speech, to file ...")
    r = speak("What documents are required for a personal loan?",
              to_file="data/tts_test.wav")
    print(f"   {r}")

    if r.get("ok"):
        print("\n3. Round trip: transcribing the file we just generated ...")
        t = transcribe_file("data/tts_test.wav")
        print(f"   recognised: {t.get('text') or t.get('error')}")
