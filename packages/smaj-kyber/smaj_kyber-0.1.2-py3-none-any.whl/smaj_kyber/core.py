import ctypes
import os
import platform

# Default Kyber mode
KYBER_MODE = "768"

# Get platform-specific shared library extension
EXTENSIONS = {
    "Darwin": ".dylib",  # macOS
    "Linux": ".so",  # Linux
    "Windows": ".dll"  # Windows
}
SYSTEM = platform.system()
LIB_EXT = EXTENSIONS.get(SYSTEM)

print("SYSTEM", SYSTEM)

if LIB_EXT is None:
    raise RuntimeError(f"Unsupported platform: {SYSTEM}")

# Mode configuration: (PK_LEN, SK_LEN, CT_LEN, SS_LEN, lib base name)
MODES = {
    "512": (800, 1632, 768, 32, f"libkyber512{LIB_EXT}"),
    "768": (1184, 2400, 1088, 32, f"libkyber768{LIB_EXT}"),
    "1024": (1568, 3168, 1568, 32, f"libkyber1024{LIB_EXT}"),
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
