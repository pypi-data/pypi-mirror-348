from diskcache import Cache

from .constants import cache_root

audio_cache = Cache[str, bytes](directory=cache_root / "yt-dlp")
