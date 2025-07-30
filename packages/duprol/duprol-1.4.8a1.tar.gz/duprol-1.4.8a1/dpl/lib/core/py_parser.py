# Parser and Preprocessor
# The heart, the interpreter of DPL

import time
import itertools
import dill
from copy import deepcopy as copy
from . import py_argument_handler
arguments_handler = py_argument_handler.arguments_handler
from .runtime import *
from . import utils
from . import objects
from . import extension_support as ext_s
from . import constants
from . import type_checker
check_ins = type_checker.check_ins
tc_register = type_checker.register
from . import info
import traceback
import sys
import os

<<<<<<< HEAD
if "no-cffi" not in info.program_flags:
    from cffi import FFI
    ext_s.dpl.ffi = FFI()

IS_STILL_RUNNING = Event()

threads = []
thread_events = [] # Thread events, so any threads can be killed manually or automatically

def clean_threads():  # kill all threads and wait for them to terminate
    for i in thread_events:
        i.set()
    for i in threads:
        i.join()

def my_exit(code=0):
    IS_STILL_RUNNING.set()
    clean_threads()
    og_exit(code)


def my_exit_atexit(code=0):
    if info.unique_imports:
        print(f"\nPerformed {len(info.imported):,} non-identical imports\nPerformed {info.unique_imports:,} total imports")

atexit.register(my_exit_atexit)

og_exit = sys.exit
ext_s.dpl.exit = my_exit
sys.exit = my_exit
exit = my_exit

# setup runtime stuff. And yes on import.
# user will have to manually define type signatures
# or lower the type checker strictness by setting TC_DEFAULT_WHEN_NOT_FOUND
try:
    import psutil

    CUR_PROCESS = psutil.Process()

    def get_memory(_, __):
        memory_usage = CUR_PROCESS.memory_info().rss
        return (utils.convert_bytes(memory_usage),)

    varproc.meta["internal"]["HasGetMemory"] = 1
    varproc.meta["internal"]["GetMemory"] = get_memory
except ModuleNotFoundError as e:
    varproc.meta["internal"]["HasGetMemory"] = 0
    varproc.meta["internal"]["GetMemory"] = lambda _, __: (state.bstate("nil"),)

varproc.meta["internal"]["SetEnv"] = os.putenv,
varproc.meta["internal"]["GetEnv"] = os.getenv

varproc.meta["internal"]["os"] = {
    "uname": info.SYS_MACH_INFO,  # uname
    "architecture": info.SYS_ARCH,  # system architecture (commonly x86 or ARMv7 or whatever arm proc)
    "executable_format": info.EXE_FORM,  # name is self explanatory
    "machine": info.SYS_MACH,  # machine information
    "information": info.SYS_INFO,  # basically the tripple
    "processor": info.SYS_PROC,  # processor (intel and such)
    "threads": os.cpu_count(),  # physical thread count,
    "os_name":info.SYS_OS_NAME.lower(),
}

if info.UNIX and info.SYS_OS_NAME == "linux":
    varproc.meta["internal"]["os"]["linux"] = {
        "name": info.LINUX_DISTRO,
        "version": info.LINUX_VERSION,
        "codename": info.LINUX_CODENAME
}


varproc.meta["threading"] = {
    "runtime_event": IS_STILL_RUNNING,
    "is_still_running": lambda: IS_STILL_RUNNING.is_set(),
}

if "get-internals" in info.program_flags:
    varproc.meta["argument_processing"] = {
        "process_argument":process_arg,
        "process_argumemts":process_args,
        "preprocess_arguments":exprs_preruntime,
        "evaluate":evaluate
    }
    
    varproc.meta["variable_processing"] = {
        "rset":rset,
        "rget":rget,
        "rpop":rpop,
        "new_frame":new_frame,
        "pop_scope":pscope,
        "new_scope":nscope
    }

def get_size_of(_, __, object):
    return (utils.convert_bytes(sys.getsizeof(object)),)


try:
    get_size_of(0, 0, 0)
    varproc.meta["internal"]["SizeOf"] = get_size_of
except:
    def temp(_, __, ___):
        return f"err:{error.PYTHON_ERROR}:Cannot get memory usage of an object!\nIf you are using pypy, pypy does not support this feature."

    varproc.meta["internal"]["SizeOf"] = temp

=======
>>>>>>> 1.4.8
def get_block(code, current_p, supress=False, start=1):
    "Get a code block"
    instruction_pointer = current_p + 1
    pos, file, ins, _ = code[instruction_pointer]
    k = start
    if k == 0 and ins not in info.INCREAMENTS:
        error.error(pos, file, "Expected to have started with an instruction that indents.")
        return None
    res = []
    while instruction_pointer < len(code):
        _, _, ins, _ = code[instruction_pointer]
        if ins in info.INC_EXT:
            k += 1
        elif ins in info.INC:
            k -= info.INC[ins]
        elif ins in info.DEC:
            k -= 1
        if k == 0:
            break
        instruction_pointer += 1
    else:
        if not supress:
            print(f"Error in line {pos} file {file!r}\nCause: Block wasnt closed!")
        return None
    return instruction_pointer, code[current_p+(2-start):instruction_pointer]


def has(attrs, dct):
    return True if False not in map(lambda x: x in dct, attrs) else False


def pprint(d, l=0, seen=None, hide=True):
    if seen is None:
        seen = set()
    if id(d) in seen:
        print("  "*l+"...")
        return
    seen.add(id(d))
    if isinstance(d, list):
        for i in d:
            if isinstance(i, list):
                print("  "*l+"[")
                pprint(i, l+1, seen)
                print("  "*l+"]")
            elif isinstance(i, dict):
                print("  "*l+"{")
                pprint(i, l+1, seen)
                print("  "*l+"}")
            else:
                print("  "*l+repr(i))
        return
    elif not isinstance(d, dict):
        print("  "*l+repr(d))
        return
    if not d:
        print("{}")
    for name, value in d.items():
        if isinstance(name, str) and name.startswith("_") and hide:
            ...
        elif isinstance(value, dict):
            print("  "*l+f"{name!r} => {{")
            pprint(value, l+1, seen)
            print("  "*l+"}")
        elif isinstance(value, list):
            print("  "*l+f"{name!r} => [")
            pprint(value, l+1, seen)
            print("  "*l+"]")
        else:
            print("  "*l+f"{name!r} = {value!r}")

def process(fcode, name="__main__"):
    "Preprocess a file"
    res = []
    nframe = new_frame()
    multiline = False
    last_comment = 0
    for lpos, line in filter(
        lambda x: (
            True
            if x[1] and not x[1].startswith("#") and not x[1].startswith("...")
            else False
        ),
        enumerate(map(str.strip, fcode.split("\n")), 1),
    ):
        if multiline:
            if line.endswith("--"):
                multiline = False
            continue
        elif len(line) >= 4 and line.startswith("--") and line.endswith("--"):
            continue
        elif line.startswith("--"):
            last_comment = lpos
            multiline = True
            continue
        line = line.replace("!__line__", str(lpos))
        line = line.replace("!__file__", name if name != "__main__" else meta_attributes["internal"]["main_file"])
        if line.startswith("&"):
            ins, *args = group(line[1:].lstrip())
            args = nest_args(exprs_preruntime(args))
            args = process_args(nframe, args)
            argc = len(args)
            if ins == "include" and argc == 1:
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(args[0][1:-1]))
                else:
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), args[0])
                    else:
                        file = os.path.join(os.getcwd(), args[0])
                if not os.path.exists(file):
                    error.error(lpos, file, f"Not found: {file}")
                    return error.PREPROCESSING_ERROR
                if os.path.isdir(file):
                    if os.path.isfile(files:=os.path.join(file, "include-dpl.txt")):
                        with open(files) as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith("#:"):
                                    print("{name} [{lpos}] {line}:",line[2:]) # for messages like deprecation warnings
                                    continue
                                elif line.startswith("#?"):
                                    print(line[2:]) # for messages like deprecation warnings
                                    continue
                                elif line.startswith("#") or not line:
                                    continue
                                line = os.path.join(file, line)
                                with open(line, "r") as f:
                                    if isinstance(err:=process(f.read(), name=line), int):
                                        return err
                                    res.extend(err["code"])
                                    if not err["frame"] is None: nframe[0].update(err["frame"][0])
                                meta_attributes["dependencies"]["dpl"].add(os.path.realpath(line))
                    else:
                        error.error(lpos, name, f"While including the directory {file!r} the include-dpl.txt file wasnt found!")
                        return error.PREPROCESSING_ERROR
                else:
                    with open(file, "r") as f:
                        if isinstance(err:=process(f.read(), name=file), int):
                            return err
                        res.extend(err["code"])
                        if not err["frame"] is None: nframe[0].update(err["frame"][0])
                    file = os.path.realpath(file)
                    meta_attributes["dependencies"]["dpl"].add(file)
            elif ins == "set_name" and argc == 1:
                name = str(args[0])
            elif ins == "define_error" and argc == 1:
                error.register_error(args[0])
            elif ins == "includec" and argc == 1:
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(args[0][1:-1]))
                else:
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), args[0])
                if not os.path.exists(file):
                    error.error(lpos, file, f"Not found: {file}")
                    return error.PREPROCESSING_ERROR
                if os.path.isdir(file):
                    if os.path.isfile(files:=os.path.join(file, "include-cdpl.txt")):
                        with open(files) as f:
                            for line in f:
                                line = line.strip()
                                if line.startswith("#:"):
                                    print("{name} [{lpos}] {line}:",line[2:]) # for messages like deprecation warnings
                                    continue
                                elif line.startswith("#?"):
                                    print(line[2:]) # for messages like deprecation warnings
                                    continue
                                elif line.startswith("#") or not line:
                                    continue
                                with open(line, "rb") as f:
                                    if isinstance(err:=process(dill.loads(f.read()), name=line), int):
                                        return err
                                    res.extend(err["code"])
                                    if not err["frame"] is None: nframe[0].update(err["frame"][0])
                                meta_attributes["dependencies"]["dpl"].add(os.path.realpath(line))
                else:
                    with open(file, "rb") as f:
                        if isinstance(err:=process(dill.loads(f.read()), name=file), int):
                            return err
                        res.extend(err["code"])
                        if not err["frame"] is None: nframe[0].update(err["frame"][0])
                    file = os.path.realpath(file)
                    meta_attributes["dependencies"]["dpl"].add(file)
            elif ins == "extend" and argc == 1:
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(args[0][1:-1]))
                else:
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), args[0])
                if not os.path.isfile(file):
                    print("File not found:", file)
                    break
                with open(file, "r") as f:
                    res.extend(process(f.read(), name=name))
                file = os.path.realpath(file)
                meta_attributes["dependencies"]["dpl"].add(file)
            elif ins == "use" and argc == 1:
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(ofile := args[0][1:-1]))
                    search_path = "_std"
                else:
                    file = os.path.join(os.path.dirname(name), (ofile := args[0]))
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), file)
                    search_path = "_loc"
                if not os.path.exists(file):
                    error.error(lpos, file, f"Not found while including: {file}")
                    return error.PREPROCESSING_ERROR
                if ext_s.py_import(nframe, file, search_path, loc=os.path.dirname(name)):
                    print(f"python: Something wrong happened...\nLine {lpos}\nFile {name}")
                    return error.PREPROCESSING_ERROR
            elif ins == "use" and argc == 3 and args[1] == "as":
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(ofile := args[0][1:-1]))
                    search_path = "_std"
                else:
                    file = os.path.join(os.path.dirname(name), (ofile := args[0]))
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), file)
                    search_path = "_loc"
                if not os.path.exists(file):
                    error.error(lpos, file, f"Not found while including: {file}")
                    return error.PREPROCESSING_ERROR
                if ext_s.py_import(nframe, file, search_path, loc=os.path.dirname(name), alias=args[2]):
                    print(f"python: Something wrong happened...\nLine {lpos}\nFile {name}")
                    return error.PREPROCESSING_ERROR
            elif ins == "use:luaj" and argc == 1:
                if args[0].startswith("{") and args[0].endswith("}"):
                    file = os.path.abspath(info.get_path_with_lib(ofile := args[0][1:-1]))
                    search_path = "_std"
                else:
                    if name != "__main__":
                        file = os.path.join(os.path.dirname(name), args[0])
                    search_path = "_loc"
                if ext_s.luaj_import(nframe, file, search_path, loc="."):
                    print(f"luaj: Something wrong happened...\nLine {lpos}\nFile {name}")
                    return error.PREPROCESSING_ERROR
            elif ins == "embed" and argc == 3 and args[1] == "as":
                if args[0] == name:
                    nframe[-1][args[2]] = fcode
                    continue
                file = os.path.join(os.path.dirname(name), args[0])
                if os.path.isfile(file):
                    with open(file) as f:
                        nframe[-1][args[2]] = f.read()
                else:
                    print("File not found:", file)
                    return error.PREPROCESSING_ERROR
            elif ins == "embed_binary" and argc == 3 and args[1] == "as":
                if args[0] == name:
                    nframe[-1][args[2]] = bytes(fcode)
                    continue
                file = os.path.join(os.path.dirname(name), args[0])
                if os.path.isfile(file):
                    with open(file, "rb") as f:
                        nframe[-1][args[2]] = f.read()
                else:
                    print("File not found:", file)
                    return error.PREPROCESSING_ERROR
            elif ins.startswith("enable:") and ins[7:] in preprocessing_flags:
                preprocessing_flags[ins[7:]] = True
            elif ins.startswith("disable:") and ins[8:] in preprocessing_flags:
                preprocessing_flags[ins[8:]] = False
            elif ins == "set" and argc == 2:
                rset(nframe[-1], args[0], args[1])
            else:
                error.pre_error(
                    lpos, name, f"{name!r}:{lpos}: Invalid directive {ins!r}"
                )
                break
        else:
            ins, *args = group(line)
            if ins != "pass":
                args = nest_args(exprs_preruntime(args))
                if preprocessing_flags["EXPRESSION_FOLDING"]: args = to_static(nframe,
                    args
                )  # If there are static parts in the arguments run them before runtime.
            res.append((lpos, name, ins, args if len(args) else None))
    else:
        if multiline:
            error.pre_error(
                last_comment,
                name,
                f"{name!r}:{last_comment}: Unclosed multiline comment!",
            )
            return error.PREPROCESSING_ERROR
        nres = []
        if preprocessing_flags["DEAD_CODE_OPT"]:
            instruction_pointer = 0
            warn_num = 0
            nres = []
            while instruction_pointer < len(res):
                line = line_pos, file, ins, args = res[instruction_pointer]
                if args is None:
                    args = []
                if (
                    ins in {"for", "loop", "while"}
                    and instruction_pointer + 1 < len(res)
                    and res[instruction_pointer + 1][2] in {"end", "stop", "skip"}
                ):
                    if preprocessing_flags["WARNINGS"]:
                        (error.warnf if not preprocessing_flags["STRICT"] else error.error)(
                            line_pos, file,
                            f"{ins!r} statement is empty!"
                        )
                        if preprocessing_flags["STRICT"]:
                            return error.PREPROCESSING_ERROR
                    temp = get_block(res, instruction_pointer)
                    if temp:
                        instruction_pointer, _ = temp
                    else:
                        return []
                    warn_num += 1
                elif (
                    ins in {"if", "module", "body"}
                    and instruction_pointer + 1 < len(res)
                    and res[instruction_pointer + 1][2] == "end"
                ):
                    if preprocessing_flags["WARNINGS"]:
                        (error.warnf if not preprocessing_flags["STRICT"] else error.error)(
                            line_pos, file,
                            f"{ins!r} statement is empty!"
                        )
                        if preprocessing_flags["STRICT"]:
                            return error.PREPROCESSING_ERROR
                    temp = get_block(res, instruction_pointer)
                    if temp:
                        instruction_pointer, _ = temp
                    else:
                        return []
                    warn_num += 1
                elif (
                    ins in {"case", "match", "with", "default"}
                    and instruction_pointer + 1 < len(res)
                    and res[instruction_pointer + 1][2] in {"end", "return"}
                ):
                    if ins != "default" and len(args) == 0:
                        error.error(
                            line_pos, file,
                            f"Error: Malformed {ins!r} statement/sub-statements!\nLine {line_pos}\nIn file {file!r}"
                        )
                        return error.PREPROCESSING_ERROR
                    if preprocessing_flags["WARNINGS"]:
                        (error.warnf if not preprocessing_flags["STRICT"] else error.error)(
                            line_pos, file,
                            f"{ins!r} statement is empty!"
                        )
                        if preprocessing_flags["STRICT"]:
                            return error.PREPROCESSING_ERROR
                    temp = get_block(res, instruction_pointer)
                    if temp:
                        instruction_pointer, _ = temp
                    else:
                        return []
                    warn_num += 1
                elif (
                    ins in {"fn", "method"}
                    and instruction_pointer + 1 < len(res)
                    and res[instruction_pointer + 1][2] in {"end", "return"}
                ):
                    if res[instruction_pointer + 1][2] == "return" and len(res[instruction_pointer + 1][3]) != 0:
                        nres.append(line)
                        instruction_pointer += 1
                        continue
                    if len(args) == 0:
                        error.warn(
                            f"Error: Malformed function definition!\nLine {line_pos}\nIn file {file!r}"
                        )
                        return error.PREPROCESSING_ERROR
                    if preprocessing_flags["WARNINGS"]:
                        (error.warnf if not preprocessing_flags["STRICT"] else error.error)(
                            line_pos, file,
                            f"{ins!r} statement is empty!"
                        )
                        if preprocessing_flags["STRICT"]:
                            return error.PREPROCESSING_ERROR
                    temp = get_block(res, instruction_pointer)
                    if temp:
                        instruction_pointer, _ = temp
                    else:
                        return []
                    warn_num += 1
                else:
                    nres.append(line)
                instruction_pointer += 1
            if preprocessing_flags["WARNINGS"] and warn_num:
                print(f"Warning Info: {warn_num:,} Total warnings.")
        else:
            nres = res
        # pass for switches
        res = []
        offset = 0
        whole_offset = 0
        for instruction_pointer, [line_pos, file, ins, args] in enumerate(nres):
            # compile the switch statement
            # this uses _intern.switch
            if ins == "switch" and len(args) == 1:
                body = {None:[]}
                arg_val = args[0]
                og_lpos = line_pos
                temp = get_block(nres, instruction_pointer)
                if temp is None:
                    error.error(line_pos, file, "Switch statement is invalid!")
                    return error.PREPROCESSING_ERROR
                whole_offset, switch_block = temp 
                for instruction_pointer, [line_pos, _, ins, args] in enumerate(switch_block):
                    if ins == "case" and len(args) == 1:
                        temp = get_block(switch_block, instruction_pointer)
                        if temp is None:
                            error.error(line_pos, file, f"Switch statement is invalid! For case '{args[0]}'")
                            return error.PREPROCESSING_ERROR
                        offset, body[args[0]] = temp
                    elif ins == "default" and args is None:
                        temp = get_block(switch_block, instruction_pointer)
                        if temp is None:
                            error.error(line_pos, file, f"Switch statement is invalid! For case '{args[0]}'")
                            return error.PREPROCESSING_ERROR
                        offset, body[None] = temp
                    else:
                        if instruction_pointer > offset:
                            error.error(line_pos, file, "Invalid switch statement!")
                            return error.PREPROCESSING_ERROR
                whole_offset += 1
                res.append([og_lpos, file, "_intern.switch", [body, arg_val]])
            elif instruction_pointer >= whole_offset and ins != "pass":
                res.append([line_pos, file, ins, args])
        return {
            "code": res,
            "frame": nframe or None,
        }
    return error.PREPROCESSING_ERROR


def run(code, frame=None):
    "Run code generated by 'process'"
    global check_ins
    instruction_pointer = 0
    if isinstance(code, int):
        return code
    if isinstance(code, dict):
        code, nframe = code["code"], code["frame"]
    else:
        nframe = new_frame()
    if frame is not None:
        frame[0].update(nframe[0])
    else:
        frame = nframe
    tc_cache = set()
    
    while instruction_pointer < len(code):
        pos, file, ins, oargs = code[instruction_pointer]
            
        ins = process_arg(frame, ins)
        if not oargs is None:
            try:
                args = process_args(frame, oargs)
                argc = len(args)
                if debug_settings["type_checker"]:
                    if (tmp:=(pos, file, ins)) not in tc_cache:
                        tc_cache.add(tmp)
                        if not check_ins(ins, args):
                            itypesr = type_checker.get_ins(ins, args)
                            if itypesr is None and not is_debug_enabled("TC_DEFAULT_WHEN_NOT_FOUND"):
                                error.error(pos, file, f"Type signature for {ins} is not defined.\nUse tc_register to register your function.")
                                return error.TYPE_ERROR
                            itypes = tuple(map(lambda x: getattr(x, "__name__", x), itypesr))
                            atypes = tuple(map(lambda x: type(x).__name__, args))
                            error.error(pos, file, f"Type mismatch [{ins}]: Expected {itypes} but got {atypes}")
                            return error.TYPE_ERROR
            except Exception as e:
                error.error(
                    pos,
                    file,
                    f"Something went wrong when arguments were processed:\n{e}\n> {oargs!r}",
                )
                return error.PYTHON_ERROR
        else:
            args = []
            argc = 0
        if ins == "inc" and argc == 1:
            rset(frame[-1], args[0], rget(frame[-1], args[0], default=0) + 1)
        elif ins == "dec" and argc == 1:
            rset(frame[-1], args[0], rget(frame[-1], args[0], default=0) - 1)
        elif ins == "fn" and argc == 2:
            name, params = args
            block = get_block(code, instruction_pointer)
            if block is None:
                break
            else:
                instruction_pointer, body = block
            args = list(params)
            func = objects.make_function(name, body, args)
            if any(filter(lambda x: isinstance(x, dict), params)):
                func["defaults"] = {}
                for pos, i in filter(lambda x: isinstance(x[1], dict), enumerate(params)):
                    func["defaults"].update(i)
                    args[pos] = kwarg(tuple(i.items())[0][0])
            rset(frame[-1], name, func)
        elif ins == "_intern.switch" and argc == 2:
            body = args[0].get(args[1], args[0][None])
            if not body:
                instruction_pointer += 1
                continue
            if err:=run(body, frame):
                error.error(pos, file, f"Error in switch block '{args[1]}'")
                return err
        elif ins == "if" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if args[0]:
                err = run(body, frame=frame)
                if err:
                    return err
        elif ins == "ifmain" and argc == 0:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if file == "__main__":
                err = run(body, frame=frame)
                if err:
                    return err
        elif ins == "match" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if (err := parse_match(frame, body, args[0])) > 0:
                return err
        elif ins == "get_time" and argc == 1:
            frame[-1][args[0]] = time.time()
        elif ins == "_intern.get_index" and argc == 1:
            frame[-1][args[0]] = instruction_pointer
        elif ins == "_intern.jump" and argc == 1:
            instruction_pointer = args[0]
        elif ins == "_intern.jump" and argc == 2:
            if args[1]: instruction_pointer = args[0]
        elif ins == "pub" and argc >= 2 and args[0] == "fn":
            _, name, params = args
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            rset(
                frame[-1], "_export." + name, (temp:=objects.make_function(name, body, params))
            )
            rset(frame[-1], name, temp)
        elif ins == "export" and argc == 4 and args[0] == "set" and args[2] == "=":
            _, name, _, value = args
            rset(frame[-1], "_export." + name, value)
            rset(frame[-1], name, value)
        elif ins == "tc_register" and argc == 1:
            tc_register(args[0])
        elif ins == "for" and argc == 3 and args[1] == "in":
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if body:
                name, _, iter = args
                index = None
                if isinstance(name, tuple):
                    index, name = name
                    iter = enumerate(iter)
                for i in iter:
                    if index is not None:
                        frame[-1][index], i = i
                    frame[-1][name] = i
                    err = run(body, frame)
                    if err:
                        if err == error.STOP_RESULT:
                            break
                        elif err == error.SKIP_RESULT:
                            continue
                        return err
        elif ins == "enum" and argc == 1:
            name = args[0]
            names = set()
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            for _, _, ins, _ in body:
                names.add(ins)
            tmp = frame[-1][name] = {}
            for n in names:
                tmp[n] = f"enum:{file}:{name}:{n}"
        elif ins == "loop" and argc == 0:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if body:
                while True:
                    err = run(body, frame)
                    if err:
                        if err == error.STOP_RESULT:
                            break
                        elif err == error.SKIP_RESULT:
                            continue
                        return err
        elif ins == "dump_scope" and argc == 0:
            pprint(frame[-1])
        elif ins == "dump_vars" and argc == 1 and isinstance(args[0], dict):
            pprint(args[0], hide=False)
        elif ins == "loop" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if body:
                for _ in range(args[0]):
                    err = run(body, frame)
                    if err:
                        if err == error.STOP_RESULT:
                            break
                        elif err == error.SKIP_RESULT:
                            continue
                        return err
        elif ins == "while" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if body:
                while (tmp:=evaluate(frame, args[0])):
                    err = run(body, frame)
                    if err:
                        if err == error.STOP_RESULT:
                            break
                        elif err == error.SKIP_RESULT:
                            continue
                        return err
<<<<<<< HEAD
        elif ins == "dlopen" and argc == 2:
            if args[1].startswith("{") and args[1].endswith("}"):
                file = info.get_path_with_lib(args[1][1:-1])
            else:
                file = args[1]
            if not os.path.isfile(file):
                error.error(pos, file, f"File {file!r} couldnt be loaded!")
                return error.FILE_NOT_FOUND_ERROR
            try:
                frame[-1][args[0]] = ext_s.dpl.ffi.dlopen(file)
            except Exception as perror:
                error.error(pos, file, f"Dynamic library couldnt be opened!\nError: {perror!r}\nReasons:\n* Permissions\n* Unsupported\n* Corrupt file")
                return error.PYTHON_ERROR
        elif ins == "dlclose" and argc == 1:
            ext_s.dpl.ffi.dlclose(args[0])
        elif ins == "getc" and argc == 2:
            frame[-1][args[0]] = getattr(args[1], args[0], constants.none)
        elif ins == "cdef" and argc == 1:
            ext_s.dpl.ffi.cdef(args[0])
=======
        elif ins == "dlopen":
            error.error(pos, file, "DEPRECATED AS OF 1.4.8 FFI IS TOO MESSY\nA REPLACEMENT WILL BE PUT IN AS SOON AS POSSIBLE")
            return error.PYTHON_ERROR
        elif ins == "dlclose":
            error.error(pos, file, "DEPRECATED AS OF 1.4.8 FFI IS TOO MESSY\nA REPLACEMENT WILL BE PUT IN AS SOON AS POSSIBLE")
            return error.PYTHON_ERROR
        elif ins == "getc":
            error.error(pos, file, "DEPRECATED AS OF 1.4.8 FFI IS TOO MESSY\nA REPLACEMENT WILL BE PUT IN AS SOON AS POSSIBLE")
            return error.PYTHON_ERROR
        elif ins == "cdef":
            error.error(pos, file, "DEPRECATED AS OF 1.4.8 FFI IS TOO MESSY\nA REPLACEMENT WILL BE PUT IN AS SOON AS POSSIBLE")
            return error.PYTHON_ERROR
>>>>>>> 1.4.8
        elif ins == "stop" and argc == 0:
            return error.STOP_RESULT
        elif ins == "skip" and argc == 0:
            return error.SKIP_RESULT
        elif ins == "sched" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            while time.time() < args[0]:
                pass
            err = run(body, frame=frame)
            if err:
                return err
        elif ins == "exec" and argc == 3:
            if err:=run(process(args[0], name=args[1]), frame=args[2]):
                return err
        elif ins == "sexec" and argc == 4:
            error.silent()
            frame[-1][args[0]] = run(process(args[1], name=args[2]), frame=args[3])
            error.active()
        elif ins == "fallthrough" and argc == 0:
            return error.FALLTHROUGH
        elif ins == "set" and argc == 3 and args[1] == "=":
            if args[0] != "_":
                if isinstance(args[0], tuple):
                    for name, value in zip(args[0], args[2]):
                        rset(frame[-1], name, value)
                else:
                    rset(frame[-1], args[0], args[2])
        elif ins == "del" and argc >= 1:
            for name in args:
                rpop(frame[-1], name)
        elif ins == "module" and argc == 1:
            name = args[0]
            temp = [frame[-1]]
            nscope(temp)
            temp[-1]["_export"] = {}
            btemp = get_block(code, instruction_pointer)
            if btemp is None:
                break
            else:
                instruction_pointer, body = btemp
            err = run(body, temp)
            if err:
                return err
            rset(frame[-1], name, temp[1]["_export"])
            del temp
        elif ins == "object" and argc == 1:
            rset(frame[-1], args[0], objects.make_object(args[0]))
        elif ins == "new" and argc == 2:
            obj = args[0]
            if obj == constants.nil:
                error.error(pos, file, f"Unknown object")
                break
            rset(obj, "_internal.instance_name", args[1])
            rset(frame[-1], args[1], copy(obj))
        elif ins == "method" and argc >= 2:
            name, params = args
            self = rget(frame[-1], name.rsplit(".", 1)[0])
            if self == constants.nil:
                error.error(
                    pos, file, "Cannot bind a method to a value that isnt a context!"
                )
                return error.RUNTIME_ERROR
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            func = objects.make_method(name, body, params, self)
            if any(filter(lambda x: isinstance(x, dict), params)):
                func["defaults"] = {}
            for i in filter(lambda x: isinstance(x, dict), params):
                func["defaults"].update(i)
            rset(self, name, func)
        elif ins == "START_TIME" and argc == 0:
            start_time = time.perf_counter()
        elif ins == "STOP_TIME" and argc == 0:
            end_time = time.perf_counter() - start_time
        elif ins == "LOG_TIME" and argc == 0:
            ct, unit = utils.convert_sec(time.perf_counter() - start_time)
            error.info(f"Elapsed time: {ct:,.8f}{unit}")
        elif ins == "LOG_TIME" and argc == 1:
            ct, unit = utils.convert_sec(time.perf_counter() - start_time)
            error.info(f"Elapsed time: {args[0]} {ct:,.8f}{unit}")
        elif ins == "cmd" and argc == 1:
            os.system(args[0])
        elif ins == "cmd" and argc == 2:
            frame[-1][args[1]] = os.system(args[0])
        elif ins == "pass":
            ...
        elif ins == "exit" and argc == 0:
            sys.exit()
        elif ins == "exit" and argc == 1:
            sys.exit(args[0])
        elif ins == "return":  # Return to the latched names
            if (temp := rget(frame[-1], "_returns")) != constants.nil:
                if (
                    "_safe_call" in frame[-1]
                    and frame[-1]["_safe_call"] == constants.true
                ):
                    args = (0, args)
                if len(temp) == 1:
                    rset(frame[-1], f"_nonlocal.{temp[0]}", args[0] if isinstance(args, (tuple, list)) and len(args) == 1 else args, meta=False)
                    #pprint(rget(frame[-1], f"_nonlocal"), hide=False)
                else:
                    if temp != "_":
                        for name, value in zip(temp, args):
                            rset(frame[-1], f"_nonlocal.{name}", value, meta=False)
                if (tmp := frame[-1].get("_memoize")) not in constants.constants_false:
                    tmp[0][tmp[1]] = tuple(
                        map(
                            lambda x: (
                                x
                                if isinstance(x, (str, int, float, tuple, complex))
                                else f"{type(x)}:{id(x)}"
                            ),
                            args,
                        )
                    )
            return error.STOP_FUNCTION
        elif (
            ins == "freturn"
        ):  # Return to the latched names with no memoization detection (faster)
            if not (temp := rget(frame[-1], "_returns")) != constants.nil:
                ...
            else:
                if (
                    "_safe_call" in frame[-1]
                    and frame[-1]["_safe_call"] == constants.true
                ):
                    args = (0, args)
                for name, value in zip(temp, args):
                    rset(frame[-1], f"_nonlocal.{name}", value)
            return error.STOP_FUNCTION
        elif ins == "help" and argc == 1:
            if not isinstance(args[0], dict) and hasattr(args[0], "__doc__"):
                doc = getattr(args[0], "__doc__")
                if doc:
                    print(
                        f"\nHelp on {getattr(args[0], '__name__', '???')}, line [{pos}]:\n{doc}"
                    )
                else:
                    help(args[0])
            elif not isinstance(args[0], dict):
                return error.TYPE_ERROR
            else:
                temp = rget(
                    args[0], "docs", default=rget(args[0], "_internal.docs")
                )
                if temp == constants.nil:
                    print(f"\nHelp, line [{pos}]: No documentation was found!")
                else:
                    print(f"\nHelp, line [{pos}]:\n{temp}")
        elif ins == "catch" and argc >= 2:  # catch return value of a function
            rets, func_name, *args = args
            if (temp := rget(frame[-1], func_name)) == constants.nil or not isinstance(temp, dict):
                error.error(pos, file, f"Invalid function {func_name!r}!")
                break
            nscope(frame)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            if temp["defaults"]:
                for name, value in itertools.zip_longest(temp["args"], args):
                    if value is None:
                        frame[-1][name] = temp["defaults"].get(name, constants.nil)
                    else:
                        frame[-1][name] = value
            else:
                if len(args) != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {func_name!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args):
                    frame[-1][name] = value
            if temp["capture"] != constants.nil:
                frame[-1]["_capture"] = temp["capture"]
            frame[-1]["_returns"] = rets
            err = run(temp["body"], frame)
            if err > 0:
                error.error(pos, file, f"Error in function {ins!r}")
                return err
            pscope(frame)
        elif ins == "DEFINE_ERROR" and 0 < argc < 3:
            error.register_error(*args)
        elif ins == "mcatch" and argc >= 2:  # catch return value of a function
            rets, func_name, *args = args
            mem_args = tuple(
                map(
                    lambda x: (
                        x
                        if isinstance(x, (str, int, float, tuple, complex))
                        else f"{type(x)}:{id(x)}"
                    ),
                    args,
                )
            )
            if (
                (temp := rget(frame[-1], func_name, default=None)) is None
            ):
                error.error(pos, file, f"Invalid function {func_name!r}!")
                break
            if mem_args in temp["memoize"]:
                for name, value in zip(rets, temp["memoize"][mem_args]):
                    rset(frame[-1], name, value)
                instruction_pointer += 1
                continue
            nscope(frame)
            if temp["defaults"]:
                for name, value in itertools.zip_longest(temp["args"], args):
                    if value is None:
                        frame[-1][name] = temp["defaults"].get(name, constants.nil)
                    else:
                        frame[-1][name] = value
            else:
                if len(args) != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {func_name!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args):
                    rset(frame[-1], name, value)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            if temp["capture"] != constants.nil:
                frame[-1]["_capture"] = temp["capture"]
            frame[-1]["_returns"] = rets
            frame[-1]["_memoize"] = (temp["memoize"], mem_args)
            err = run(temp["body"], frame)
            if err > 0:
                error.error(pos, file, f"Error in function {ins!r}")
                return err
            pscope(frame)
        elif ins == "smcatch" and argc >= 2 and len(args[0]) >= 1:  # safe catch return value of a function
            rets, func_name, *args = args
            mem_args = tuple(
                map(
                    lambda x: (
                        x
                        if isinstance(x, (str, int, float, tuple, complex))
                        else f"{type(x)}:{id(x)}"
                    ),
                    args,
                )
            )
            if (
                (temp := rget(frame[-1], func_name)) == constants.nil
                and isinstance(temp, dict)
                and mem_args in temp
            ):
                error.error(pos, file, f"Invalid function {func_name!r}!")
                break
            if mem_args in temp["memoize"]:
                for name, value in zip(rets, temp["memoize"][mem_args]):
                    rset(frame[-1], name, value)
                instruction_pointer += 1
                continue
            nscope(frame)
            if temp["defaults"]:
                for name, value in itertools.zip_longest(temp["args"], args):
                    if value is None:
                        frame[-1][name] = temp["defaults"].get(name, constants.nil)
                    else:
                        frame[-1][name] = value
            else:
                if len(args) != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {func_name!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args):
                    rset(frame[-1], name, value)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            if temp["capture"] != constants.nil:
                frame[-1]["_capture"] = temp["capture"]
            frame[-1]["_returns"] = rets
            frame[-1]["_safe_call"] = constants.true
            frame[-1]["_memoize"] = (temp["memoize"], mem_args)
            error.silent()
            err = run(temp["body"], frame)
            if err:
                frame[-1][args[0][0]] = err
            error.active()
            pscope(frame)
        elif ins == "scatch" and argc >= 2 and len(args[0]) >= 1:  # catch return value of a function
            rets, func_name, *args = args
            if (temp := rget(frame[-1], func_name)) == constants.nil or not isinstance(temp, dict):
                error.error(pos, file, f"Invalid function {func_name!r}!")
                break
            nscope(frame)
            if temp["defaults"]:
                for name, value in itertools.zip_longest(temp["args"], args):
                    if value is None:
                        frame[-1][name] = temp["defaults"].get(name, constants.nil)
                    else:
                        frame[-1][name] = value
            else:
                if len(args) != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {func_name!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args):
                    rset(frame[-1], name, value)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            if temp["capture"] != constants.nil:
                frame[-1]["_capture"] = temp["capture"]
            frame[-1]["_returns"] = rets
            frame[-1]["_safe_call"] = constants.true
            error.silent()
            err = run(temp["body"], frame)
            if err:
                frame[-1][args[0][0]] = err
            error.active()
            pscope(frame)
        elif ins == "pycatch" and argc >= 2:  # catch return value of a python function
            rets, name, *args = args
            if (function := rget(frame[-1], name)) == constants.nil or not hasattr(function, "__call__"):
                error.error(pos, file, f"Invalid function {name!r}!")
                return error.NAME_ERROR
            try:
                if argc == 3 and isinstance(args[0], dict) and args[0].get("[RGS]"):
                    args[0].pop("[RGS]")
                    pa = args[0].pop("[PARGS]", tuple())
                    res = ext_s.call(
                        function, frame, meta_attributes["internal"]["main_path"], pa, args[0]
                    )
                else:
                    func_params = ext_s.get_py_params(function)[2:]
                    if func_params and any(map(lambda x: x.endswith("_body") or x.endswith("_xbody"), func_params)):
                        t_args = []
                        for i, _ in zip(func_params, args):
                            if i.endswith("_xbody"):
                                temp = get_block(code, instruction_pointer, start=0)
                                if temp is None:
                                    error.error(pos, file, f"Function '{function.__name__}' expected a block!")
                                    return (error.RUNTIME_ERROR, error.SYNTAX_ERROR)
                                instruction_pointer, body = temp
                                t_args.append(body)
                            elif i.endswith("_body"):
                                temp = get_block(code, instruction_pointer)
                                if temp is None:
                                    error.error(pos, file, f"Function '{function.__name__}' expected a block!")
                                    return (error.RUNTIME_ERROR, error.SYNTAX_ERROR) # say "runtime error" caised by "syntax error"
                                instruction_pointer, body = temp
                                t_args.append(body)
                            else:
                                t_args.append(args.pop(0))
                    else:
                        t_args = args
                    res = ext_s.call(
                        function, frame, meta_attributes["internal"]["main_path"], t_args
                    )
                if (
                    res is None
                    and info.WARNINGS
                    and is_debug_enabled("warn_no_return")
                ):
                    error.warn(
                        "Function doesnt return anything. To reduce overhead please dont use pycatch.\nLine {pos}\nFile {file}"
                    )
                if isinstance(res, tuple):
                    if rets != "_":
                        for name, value in zip(rets, res):
                            rset(frame[-1], name, value)
                elif isinstance(res, int) and res:
                    return res
                elif isinstance(res, str):
                    if res == "err":
                        break
                    elif res == "stop":
                        return error.STOP_RESULT
                    elif res == "skip":
                        return error.SKIP_RESULT
                    elif res.startswith("err:"):
                        _, ecode, message = res.split(":", 2)
                        error.error(pos, file, message)
                        return int(ecode)
            except:
                error.error(pos, file, traceback.format_exc()[:-1])
                return error.PYTHON_ERROR
        elif ins == "dict" and argc == 1:
            temp = get_block(code, instruction_pointer)
            if temp is None:
                break
            else:
                instruction_pointer, body = temp
            if parse_dict(frame, args[0], body):
                break
        elif ins == "raise" and isinstance(args[0], int) and argc == 2:
            error.error(pos, file, args[1])
            if (
                (temp := frame[-1].get("_returns"))
                and "_safe_call" in frame[-1]
                and frame[-1]["_safe_call"] == constants.true
            ):
                args = (args[0], constants.nil)
                for name, value in zip(temp, args):
                    rset(frame[-1], f"_nonlocal.{name}", value)
            return args[0]
        elif ins == "raise" and argc == 1 and isinstance(args[0], int):
            error.error(pos, file, "Raised an error.")
            if (
                (temp := frame[-1].get("_returns"))
                and "_safe_call" in frame[-1]
                and frame[-1]["_safe_call"] == constants.true
            ):
                args = (args[0], constants.nil)
                for name, value in zip(temp, args):
                    rset(frame[-1], f"_nonlocal.{name}", value)
            return args[0]
        elif (
            ins == "safe"
            and (
                temp := rget(
                    frame[-1], args[0], default=rget(frame[0], args[0])
                )
            )
            != constants.nil
            and isinstance(temp, dict)
            and has(["defaults", "self", "body", "args", "capture"], temp)
        ):  # Call a function
            nscope(frame)
            if temp["defaults"]:
                for name, value in itertools.zip_longest(temp["args"], args[1:]):
                    if value is None:
                        frame[-1][name] = temp["defaults"].get(name, constants.nil)
                    else:
                        frame[-1][name] = value
            else:
                if len(args) - 1 != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {func_name!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args[1:]):
                    rset(frame[-1], name, value)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            error.silent()
            run(temp["body"], frame)
            error.active()
            pscope(frame)
        elif (
            (temp := rget(frame[-1], ins, default=rget(frame[0], ins)))
            != constants.nil
            and isinstance(temp, dict)
            and has(["defaults", "self", "body", "args", "capture"], temp)
        ):  # Call a function
            nscope(frame)
            if temp["self"] != constants.nil:
                frame[-1]["self"] = temp["self"]
            if temp["defaults"]:
                frame[-1].update(temp["defaults"])
                for name, value in itertools.zip_longest(temp["args"], args):
                    if value is None:
                        continue
                    elif isinstance(value, kwarg):
                        frame[-1][value.name] = value.value
                    else:
                        if isinstance(name, kwarg):
                            if name.value is None:
                                frame[-1][name.name] = value
                            else:
                                frame[-1][name.name] = name.value
                        else:
                            frame[-1][name] = value
            else:
                if len(args) != len(temp["args"]):
                    error.error(
                        pos,
                        file,
                        f"Function {ins!r} has a parameter mismatch!\nGot {'more' if len(args) > len(temp['args']) else 'less'} than expected.",
                    )
                    break
                for name, value in itertools.zip_longest(temp["args"], args):
                    rset(frame[-1], name, value)
            if temp["capture"] != constants.nil:
                frame[-1]["_capture"] = temp["capture"]
            err = run(temp["body"], frame)
            if err and err != error.STOP_FUNCTION:
                if err > 0: error.error(pos, file, f"Error in function {ins!r}")
                return err
            pscope(frame)
        elif (
            function := rget(frame[-1], ins, default=rget(frame[0], ins))
        ) != constants.nil and hasattr(
            function, "__call__"
        ):  # call a python function
            try:
                func_params = ext_s.get_py_params(function)[2:]
                if func_params and any(map(lambda x: x.endswith("_body") or x.endswith("_xbody"), func_params)):
                    t_args = []
                    for i, _ in zip(func_params, args):
                        if i.endswith("_xbody"):
                            temp = get_block(code, instruction_pointer, start=0)
                            if temp is None:
                                error.error(pos, file, f"Function '{function.__name__}' expected a block!")
                                return (error.RUNTIME_ERROR, error.SYNTAX_ERROR)
                            instruction_pointer, body = temp
                            t_args.append(body)
                        elif i.endswith("_body"):
                            temp = get_block(code, instruction_pointer)
                            if temp is None:
                                error.error(pos, file, f"Function '{function.__name__}' expected a block!")
                                return (error.RUNTIME_ERROR, error.SYNTAX_ERROR) # say "runtime error" caised by "syntax error"
                            instruction_pointer, body = temp
                            t_args.append(body)
                        else:
                            t_args.append(args.pop(0))
                else:
                    t_args = args
                res = ext_s.call(
                    function, frame, meta_attributes["internal"]["main_path"], t_args
                )
                if isinstance(res, int) and res:
                    return res
                elif isinstance(res, str):
                    if res == "break":
                        break
                    elif res.startswith("err:"):
                        _, ecode, message = res.split(":", 2)
                        error.error(pos, file, message)
                        return int(ecode)
            except:
                error.error(pos, file, traceback.format_exc()[:-1])
                return error.PYTHON_ERROR
        elif ins == "local" and argc == 1:
            run(args[0]["body"], frame)
        elif ins == "end" and argc == 0:
            error.error(pos, file, "Lingering end statement!")
            return error.SYNTAX_ERROR
        elif ins == "!" and argc >= 2:
            it, func, *args = args
            try:
                if it == "call":
                    if args and isinstance(args[0], arguments_handler): args[0].call(func)
                    else: func(*args)
                elif it == "catch" and len(args) >= 1:
                    if len(args) >= 2 and isinstance(args[1], arguments_handler): [frame[-1].__setitem__(name, value)
                    for name, value in zip(args[0], args[1].call(func))]
                    else: [frame[-1].__setitem__(name, value)
                    for name, value in zip(args[0], func(*args[1:]))]
            except Exception as e:
                error.error(pos, file, traceback.format_exc())
                return error.PYTHON_ERROR
        else:
            if not isinstance((obj := rget(frame[-1], ins)), dict) and obj in (
                None,
                constants.none,
            ):
                print(
                    "\nAdditional Info: User may have called a partially defined function!",
                    end="",
                )
            error.error(pos, file, f"Invalid instruction {ins}")
            return error.RUNTIME_ERROR
        instruction_pointer += 1
    else:
        return 0
    error.error(pos, file, "Error was raised!")
    return error.SYNTAX_ERROR

# Doesnt use module.name = value
# so that when we change the names
# we dont need to go scour every file.

# to avoid circular imports
# this is classified as dark magic...
# basically instead of an "import"
# is equivalent to "export to"
ext_s.register_run(run)
ext_s.register_process(process)
argproc_setter.set_run(run)