#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Package initialization file for pyprintf string formatting library.

Exposes core functionality at the package level and defines version information.
"""

from .core import sprintf, vsprintf, config

__all__ = ["sprintf", "vsprintf", "config"]
__version__ = "0.0.5"
