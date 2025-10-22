__version__ = "1.0.0"
__author__ = "Manoj Santhoju"
__email__ = "manoj.santhoju@student.ncirl.ie"

from .core.framework import UnifiedForensicsFramework
from .core.os_detector import OSDetector
from .core.output_standardizer import OutputStandardizer

__all__ = [
    "UnifiedForensicsFramework",
    "OSDetector", 
    "OutputStandardizer"
]
