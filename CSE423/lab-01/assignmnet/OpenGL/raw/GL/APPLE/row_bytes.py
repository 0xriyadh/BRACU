'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_APPLE_row_bytes'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_APPLE_row_bytes',error_checker=_errors._error_checker)
GL_PACK_ROW_BYTES_APPLE=_C('GL_PACK_ROW_BYTES_APPLE',0x8A15)
GL_UNPACK_ROW_BYTES_APPLE=_C('GL_UNPACK_ROW_BYTES_APPLE',0x8A16)

