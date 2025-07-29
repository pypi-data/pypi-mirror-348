"""
Page Generator Package

This package provides modules for generating the GitLab anomaly report HTML pages.
Each module handles a specific aspect of the generation process:

- data_loader: Handles data loading and environment variables
- css_generator: Generates CSS styles
- js_view_logic: Handles view switching and UI logic
- js_rendering: Handles rendering of components
- js_event_listeners: Sets up event listeners
"""

from .data_loader import _read_data, load_environment_variables
from .css_generator import generate_css
from .js_view_logic import generate_view_logic
from .js_rendering import generate_rendering
from .js_event_listeners import generate_event_listeners

__all__ = [
    '_read_data',
    'load_environment_variables',
    'generate_css',
    'generate_view_logic',
    'generate_rendering',
    'generate_event_listeners'
]
