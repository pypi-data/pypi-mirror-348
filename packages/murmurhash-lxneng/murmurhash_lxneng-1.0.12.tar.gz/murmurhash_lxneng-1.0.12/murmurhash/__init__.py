import os

from .about import *
from .mrmr import hash, hash64_py, hash_bytes, hash_unicode


def get_include():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "include")
