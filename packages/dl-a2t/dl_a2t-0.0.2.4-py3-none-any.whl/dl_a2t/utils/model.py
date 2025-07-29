from .constants import cache_root


def get_download_root(model: str):
    path = cache_root / "whisper" / model
    path.mkdir(exist_ok=True, parents=True)
    return str(path)


def load_model(model: str):
    from whisper import load_model

    return load_model(model, download_root=get_download_root(model))
