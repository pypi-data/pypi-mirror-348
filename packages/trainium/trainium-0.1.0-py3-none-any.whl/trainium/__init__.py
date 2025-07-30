"""
Trainium - Autopilot Your ML

A Python library that automates your machine learning workflow from
data preparation to model deployment.
"""

__version__ = "0.1.0"

# Import main functions for easy access
from .core import load_data, AutoTrain

__all__ = ["load_data", "AutoTrain"]
