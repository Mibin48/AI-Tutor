import abc
import hashlib
from pathlib import Path
import edge_tts
from backend import config


class BaseTTS(abc.ABC):
    """Abstract interface for text-to-speech engines."""

    @abc.abstractmethod
    async def synthesize(self, text: str) -> str:
        """Synthesize text into speech and return the public audio URL."""
        pass


class EdgeTTS(BaseTTS):
    """Edge-TTS synthesizer with local MD5 hash-based disk caching."""

    def __init__(self, voice: str = config.VOICE, cache_dir: Path = config.AUDIO_CACHE_DIR):
        self.voice = voice
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_filename(self, text: str) -> str:
        clean_text = text.strip()
        text_hash = hashlib.md5(f"{self.voice}:{clean_text}".encode("utf-8")).hexdigest()
        return f"{text_hash}.mp3"

    async def synthesize(self, text: str) -> str:
        clean_text = text.strip()
        if not clean_text:
            return ""

        filename = self._get_filename(clean_text)
        file_path = self.cache_dir / filename

        # Return cached audio if already generated
        if file_path.exists() and file_path.stat().st_size > 0:
            return f"/audio/{filename}"

        try:
            communicate = edge_tts.Communicate(clean_text, self.voice)
            await communicate.save(str(file_path))
            return f"/audio/{filename}"
        except Exception as e:
            print(f"TTS synthesis warning ({e}); returning fallback.")
            return ""


# Default singleton
_tts_engine: BaseTTS = EdgeTTS()


def get_tts_engine() -> BaseTTS:
    return _tts_engine
