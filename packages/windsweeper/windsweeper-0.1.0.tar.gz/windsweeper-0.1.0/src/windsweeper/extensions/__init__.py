"""
Extensions package for the Windsweeper SDK.
Provides a plugin architecture for customizing and extending SDK behavior.
"""

from .extension import (
    WindsweeperExtension,
    RequestInterceptor,
    ExtensionRegistry,
    extension_registry,
    create_extension,
    create_interceptor
)

__all__ = [
    'WindsweeperExtension',
    'RequestInterceptor',
    'ExtensionRegistry',
    'extension_registry',
    'create_extension',
    'create_interceptor'
]
