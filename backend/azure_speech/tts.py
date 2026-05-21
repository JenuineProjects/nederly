"""Azure TTS wrapper. Synthesizes Dutch audio (MP3) for a word/phrase.

When AZURE_SPEECH_KEY is unset, returns None so the app can fall back to
on-device TTS (expo-speech) during early development without Azure setup.
"""
from __future__ import annotations

import os
from pathlib import Path

try:
    import azure.cognitiveservices.speech as speechsdk
except ImportError:
    speechsdk = None


AUDIO_DIR = Path(__file__).resolve().parent.parent / "audio_cache"
AUDIO_DIR.mkdir(exist_ok=True)


def synthesize(text: str, out_name: str) -> Path | None:
    key = os.getenv("AZURE_SPEECH_KEY")
    region = os.getenv("AZURE_SPEECH_REGION", "westeurope")
    voice = os.getenv("NEDERLY_TTS_VOICE", "nl-NL-ColetteNeural")

    if not key or speechsdk is None:
        return None

    out_path = AUDIO_DIR / f"{out_name}.mp3"
    if out_path.exists():
        return out_path

    config = speechsdk.SpeechConfig(subscription=key, region=region)
    config.speech_synthesis_voice_name = voice
    config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio24Khz48KBitRateMonoMp3
    )
    audio_config = speechsdk.audio.AudioOutputConfig(filename=str(out_path))
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()

    if result.reason != speechsdk.ResultReason.SynthesizingAudioCompleted:
        return None
    return out_path
