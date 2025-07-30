import ctypes
import os

# Default Kyber mode
KYBER_MODE = "768"

MODES = {
    "512": (800, 1632, 768, 32, "libkyber512.dylib"),
    "768": (1184, 2400, 1088, 32, "libkyber768.dylib"),
    "1024": (1568, 3168, 1568, 32, "libkyber1024.dylib"),
}

# Internal state
PK_LEN, SK_LEN, CT_LEN, SS_LEN, libname = MODES[KYBER_MODE]
LIB_PATH = os.path.join(os.path.dirname(__file__), "lib", libname)
lib = ctypes.CDLL(LIB_PATH)

Uint8Array = ctypes.POINTER(ctypes.c_ubyte)

# Function signatures
lib.keypair.argtypes = [Uint8Array, Uint8Array]
lib.encapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]
lib.decapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]


def set_mode(mode: str):
    """Change Kyber mode at runtime. Use '512', '768', or '1024'."""
    global PK_LEN, SK_LEN, CT_LEN, SS_LEN, libname, lib, LIB_PATH

    if mode not in MODES:
        raise ValueError("Invalid mode. Choose '512', '768', or '1024'.")

    PK_LEN, SK_LEN, CT_LEN, SS_LEN, libname = MODES[mode]
    LIB_PATH = os.path.join(os.path.dirname(__file__), "lib", libname)
    lib = ctypes.CDLL(LIB_PATH)

    # Update function signatures
    lib.keypair.argtypes = [Uint8Array, Uint8Array]
    lib.encapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]
    lib.decapsulate.argtypes = [Uint8Array, Uint8Array, Uint8Array]


def keygen():
    pk = (ctypes.c_ubyte * PK_LEN)()
    sk = (ctypes.c_ubyte * SK_LEN)()
    lib.keypair(pk, sk)
    return bytes(pk), bytes(sk)


def encapsulate(pk: bytes):
    assert len(pk) == PK_LEN
    pk_buf = (ctypes.c_ubyte * PK_LEN).from_buffer_copy(pk)
    ct = (ctypes.c_ubyte * CT_LEN)()
    ss = (ctypes.c_ubyte * SS_LEN)()
    lib.encapsulate(pk_buf, ct, ss)
    return bytes(ct), bytes(ss)


def decapsulate(ct: bytes, sk: bytes):
    assert len(ct) == CT_LEN
    assert len(sk) == SK_LEN
    ct_buf = (ctypes.c_ubyte * CT_LEN).from_buffer_copy(ct)
    sk_buf = (ctypes.c_ubyte * SK_LEN).from_buffer_copy(sk)
    ss = (ctypes.c_ubyte * SS_LEN)()
    lib.decapsulate(ct_buf, sk_buf, ss)
    return bytes(ss)
