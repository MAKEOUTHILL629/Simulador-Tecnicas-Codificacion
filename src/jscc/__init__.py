"""
Joint Source-Channel Coding (JSCC) Module

This module implements JSCC decoders that exploit residual source redundancy
to improve error correction performance compared to traditional SSCC approaches.
"""

from .hmm_model import HMMSourceModel
from .jscc_decoder import JSCCDecoder, TurboJSCCDecoder

__all__ = ['HMMSourceModel', 'JSCCDecoder', 'TurboJSCCDecoder']
