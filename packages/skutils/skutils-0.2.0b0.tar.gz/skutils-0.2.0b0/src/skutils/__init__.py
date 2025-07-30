from .LegacyGretinaLoader import LegacyGretinaLoader

from .constants import FEMTODAQ_USB, __min_femtodaq_version__
from .FemtoDAQController import FemtoDAQController, BusyError
from .Loader import (
    ChannelData,
    EventInfo,
    EventCSVLoader,
    GretinaLoader,
    IGORPulseHeightLoader,
    IGORWaveLoader,
    BaseLoader,
    quickLoad,
)
from .SolidagoController import Stream, SolidagoController
from .quickPlotEvent import quickPlotEvent
import importlib.metadata

__version__ = importlib.metadata.version(__package__)

print("Skutils is in beta, please contact support@skutek.com with bugs, issues, and questions")
__all__ = [
    "LegacyGretinaLoader",
    "FemtoDAQController",
    "ChannelData",
    "EventInfo",
    "EventCSVLoader",
    "GretinaLoader",
    "IGORPulseHeightLoader",
    "IGORWaveLoader",
    "BaseLoader",
    "quickLoad",
    "BusyError",
    "Stream",
    "SolidagoController",
    "quickPlotEvent",
    "FEMTODAQ_USB",
    "__version__",
    "__min_femtodaq_version__",
]
