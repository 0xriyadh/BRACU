'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_EXT_packed_pixels'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_EXT_packed_pixels',error_checker=_errors._error_checker)
GL_UNSIGNED_BYTE_3_3_2_EXT=_C('GL_UNSIGNED_BYTE_3_3_2_EXT',0x8032)
GL_UNSIGNED_INT_10_10_10_2_EXT=_C('GL_UNSIGNED_INT_10_10_10_2_EXT',0x8036)
GL_UNSIGNED_INT_8_8_8_8_EXT=_C('GL_UNSIGNED_INT_8_8_8_8_EXT',0x8035)
GL_UNSIGNED_SHORT_4_4_4_4_EXT=_C('GL_UNSIGNED_SHORT_4_4_4_4_EXT',0x8033)
GL_UNSIGNED_SHORT_5_5_5_1_EXT=_C('GL_UNSIGNED_SHORT_5_5_5_1_EXT',0x8034)
