from importlib import metadata

from langchain_featherless_ai.chat_models import ChatFeatherlessAi

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
del metadata  # optional, avoids polluting the results of dir(__package__)

__all__ = [
    "ChatFeatherlessAi",
    "__version__",
]
