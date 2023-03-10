# NOTE: never import anything here, in order to maintain CLI speed
__version__ = "0.5.0"


def get_cache(path, cache_cls=None):
    """Return a cache, with a given folder path."""
    if cache_cls is None:
        from jupyter_cache.cache.main import JupyterCacheBase as cache_cls

    return cache_cls(path)
