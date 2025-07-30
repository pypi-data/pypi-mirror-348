# Used for system info and other data
# Variables are handled in varproc.py

# THIS FILE SHOULD NOT IMPORT DPL MODULES AS A CIRCULAR IMPORT WILL HAPPEN
# ALMOST EVERY FILE IN lib.core IMPORTS THIS

import os
import sys
import platform

unique_imports = set()

program_flags = set()
<<<<<<< HEAD

# turns out ffi.cdef doesnt support directives.
# good to know...
safe_py_bindings = """

typedef struct {
    char* content;
    char* type;
} Expr;

typedef struct {
    char* key;
    Expr value;
} DictEntry;

typedef struct {
    DictEntry *items;
    size_t length;
    size_t cap;
} Dict;

Dict make_dict(DictEntry e[]);
void dict_add_item(Dict *d, char* k, char* s);
void* dict_get_item(Dict d, char* k);
void* dict_pop_item(Dict *d, char* k);
"""

# provide the bindings for interacting with python
# albeit simpler
py_bindings = f"""
#ifndef _DPL_PY_BINDINGS_H_
#define _DPL_PY_BINDINGS_H_

#include <stdint.h>
#include <stdlib.h>
{safe_py_bindings}
#endif // _DPL_PY_BINDINGS_H_
"""
=======
program_vflags = {}
>>>>>>> 1.4.8

try:
    from . import constants
except ImportError:

    class constants:
        nil = 0
        true = 1
        false = 0
        none = None


ARGV = sys.argv
ARGC = len(ARGV)

INC_EXT = {
    "match",
    "case",
    "fn",
    "module",
    "method",
    "for",
    "pub",
    "loop",
    "while",
    "if",
    "body",
    "dict",
    "with",
    "default",
    "sched",
    "enum",
    "ifmain",
    "switch",
    "begin"
}

INC = {}

INCREMENTS = set(INC.keys()) | INC_EXT

DEC = {"end"}

RT_EXPR = {
    "tuple", "?tuple",
    "dict", "?dict",
    "?int", "?float", "?str",
    "length", "type", "range", "rawrange", "drange",
    "drawrange", 'nil?', 'none?', 'def?',
    "eval",
}

def add_runtime_dependent_method(keyword):
    RT_EXPR.add(keyword)

FUNCTIONS = {
    'cmd',
    'exit',
    'wait_for_threads',
    'exec', 'sexec',
    'dump_vars', 'dump_scope', 'fallthrough',
}

CONSTANTS = {
    'true', 'false', 'nil', 'none', '...'
}

KEYWORDS = {
    'skip',
    'stop',
    'in', 'as', 'not', 'and', 'or',
    'raise', 'tc_register',
    'export',
    'set',
    'del',
}

ALL_INTRINSICS = INC_EXT | set(INC.keys()) | DEC | KEYWORDS

CHARS = {
    "\\\\": "\\[escape]",
    "\\n": "\n",
    "\\t": "\t",
    "\\s": " ",
    "\\v": "\v",
    "\\f": "\f",
    "\\r": "\r",
    "\\a": "\a",
    "\\0": "\0",
    "\\[escape]": "\\",
}

OPEN_P = "[("
CLOSE_P = ")]"

class flags:
    WARNINGS = True      # Specific to warnings.
    ERRORS = True        # Logs, Warnings and Such

VERSION_TRIPLE = (1, 4, 8)

def isCompat(version, VERSION=VERSION_TRIPLE):
    major, minor, patch = version
    if major != VERSION[0]:
        return False
    elif minor != VERSION[1]:
        return False
    if VERSION[2] is None or patch is None:
        return True
    if patch >= VERSION[2]:
        return True
    else:
        return False


def getDiff(version_triple, VERSION=VERSION_TRIPLE):
    major, minor, patch = version_triple
    if major < VERSION[0]:
        return "Script is outdated!"
    elif major > VERSION[0]:
        return "Interpreter is outdated!"
    elif minor < VERSION[1]:
        return "Script is outdated!"
    elif minor > VERSION[1]:
        return "Interpreter is outdated!"
    if VERSION[2] is None or patch is None:
        return 0
    if patch < VERSION[2]:
        return "Script is outdated!"
    else:
        return 0


def isLater(version_triple, VERSION=VERSION_TRIPLE):
    major, minor, patch = version_triple
    b_major, b_minor, b_patch = VERSION

    b_patch = b_patch or 0

    if major >= b_major:
        if minor >= b_minor:
            if b_patch is None or patch is None:
                return True
            if patch >= b_patch:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


class Version:
    def __init__(self, major, minor, patch=None):
        self.ver = (major, minor, patch)

    def isCompat(self, version_triple):
        if isinstance(version_triple, tuple):
            return isCompat(version_triple, self.ver)
        elif isinstance(version_triple, (Version, VersionSpec)):
            return isCompat(version_triple.ver, self.ver)

    def isLater(self, version_triple):
        if isinstance(version_triple, tuple):
            return isLater(version_triple, self.ver)
        elif isinstance(version_triple, (Version, VersionSpec)):
            return isLater(version_triple.ver, self.ver)

    def getDiff(self, version_triple, VERSION=None):
        VERSION = VERSION
        major, minor, patch = version_triple
        if major < VERSION[0]:
            return "Script is outdated!"
        elif major > VERSION[0]:
            return "Interpreter is outdated!"
        elif minor < VERSION[1]:
            return "Script is outdated!"
        elif minor > VERSION[1]:
            return "Interpreter is outdated!"
        if VERSION[2] is None or patch is None:
            return 0
        if patch < VERSION[2]:
            return "Script is outdated!"
        else:
            return 0

    def __repr__(self):
        if self.ver[2] is None:
            return ".".join(map(str, self.ver[:2])) + ".x"
        return "v" + ".".join(map(str, self.ver))


class VersionSpec(Version):
    def __init__(self, ver_str):
        if not (ver := tuple(filter(str.isdigit, ver_str.split(".")))):
            raise Exception(f"Invalid version format!")
        ver = (*map(int, ver),)
        self.ver = ver + (0,) * (3 - len(ver))


VERSION = Version(*VERSION_TRIPLE)

BINDIR = os.path.dirname(ARGV[0])
LIBDIR = os.path.join(BINDIR, "lib")
CORE_DIR = os.path.join(BINDIR, "lib", "core")

if os.name == "nt":
    UNIX = False
else:
    UNIX = True

PYTHON_VER = sys.version
PYTHON_RAW_VER = (temp := sys.version_info).major, temp.minor, temp.micro

SYS_ARCH, EXE_FORM = platform.architecture()
EXE_FORM = EXE_FORM or constants.none
SYS_PROC = platform.processor() or constants.none
SYS_MACH = platform.machine()
SYS_INFO = platform.platform()
SYS_MACH_INFO = platform.uname()
SYS_OS_NAME = SYS_MACH_INFO.system.lower()

if UNIX: # probably linux so use distro to fetch more info
    try:
        import distro
        LINUX_DISTRO = distro.name() or 0
        LINUX_VERSION = distro.version() or 0
        LINUX_CODENAME = distro.codename() or 0
    except:
        LINUX_DISTRO = 0
        LINUX_VERSION = 0
        LINUX_CODENAME = 0


def get_path_with_lib(path):
    return os.path.join(LIBDIR, path)


def get_path_with_cwd(path):
    return os.path.join(os.getcwd(), path)


def print_info():
    for name, value in globals().copy().items():
        if name in {"os", "sys", "print_info", "platform"} or not name.isupper():
            continue
        if not name.startswith("__") and not name.startswith("__"):
            print(f"{name} = {value!r}")


if __name__ == "__main__":
    print_info()
