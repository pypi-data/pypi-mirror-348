"""
Copyright (c) 2025, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE.txt.
"""

from .xml2python import Xml2Python

try:
    from ._version import version

    __version__ = version
except ImportError:
    __version__ = 'dev'
