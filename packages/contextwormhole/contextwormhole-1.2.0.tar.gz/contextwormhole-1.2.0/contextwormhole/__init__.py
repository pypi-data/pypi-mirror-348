"""
ContextWormhole: A library for extending context length in transformer models.

This library provides strategies for handling inputs that exceed the maximum
context length of transformer models, including sliding window, hierarchical
context processing, and attention sink mechanisms.
"""

__version__ = "1.2.0"

# Import main components for easy access
from contextwormhole.core import (
    ContextWormholeModel,
    ExtendedContextConfig,
    sliding_window,
    hierarchical_context,
    attention_sink,
    extended_context,
    configure_extended_context,
    create_extended_model,
    auto_detect_context_length,
    ContextWormholeError,
    ConfigurationError,
    ModelError,
    ExtendedContextMixin,
)

# Define what's available for import with "from contextwormhole import *"
__all__ = [
    "ContextWormholeModel",
    "ExtendedContextConfig",
    "sliding_window",
    "hierarchical_context",
    "attention_sink",
    "extended_context",
    "configure_extended_context",
    "create_extended_model",
    "auto_detect_context_length",
    "ContextWormholeError",
    "ConfigurationError",
    "ModelError",
]