from .client import Kairoz
from .prompt import Prompt
from .version import __version__

# Default instance
kairoz = Kairoz()

# Exports for direct imports
__all__ = ["Kairoz", "Prompt", "kairoz", "__version__"]
