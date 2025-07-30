# Used to handle arguments and expressions
# NOT FOR THE CLI

from sys import flags
import traceback
import operator

simple_ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '//': operator.floordiv,
    '%': operator.mod,
    '<': lambda *x: constants.true if operator.lt(*x) else constants.false,
    '<=': lambda *x: constants.true if operator.le(*x) else constants.false,
    '>': lambda *x: constants.true if operator.gt(*x) else constants.false,
    '>=': lambda *x: constants.true if operator.ge(*x) else constants.false,
    '==': lambda *x: constants.true if operator.eq(*x) else constants.false,
    '!=': lambda *x: constants.true if operator.ne(*x) else constants.false,
    'and': lambda a, b: constants.true if a and b else constants.false,
    'or': lambda a, b: constants.true if a or b else constants.false,
    'in': lambda a, b: constants.true if a in b else constants.false,
    'is': lambda a, b: constants.true if a is b else constants.false,
    "**": operator.pow,
    "=": lambda name, value: {name: value},
    "=>": lambda *x: kwarg(*x)
}

chars = {
    "\\":"\\",
    "n": "\n",
    "b": "\b",
    "f": "\f",
    "v": "\v",
    "a": "\a",
    "r": "\r",
    "s": " ",
    "t": "\t",
    "N": "\n\r",
    "e": chr(27)
}


# from requests.models import parse_header_links
from . import state
from . import constants
from . import varproc
from . import error
from .info import *
from . import py_argument_handler as pah

rget = varproc.rget
get_debug = varproc.get_debug

run_code = None  # to be set by py_parser

class argt:
    class Evaluated:
        def __init__(self, value):
            self.value = value
        def unwrap(self):
            return self.value
        def __repr__(self):
            return f"Evaluated({self.value!r})"
    class NotEvaluated:
        def __init__(self, value):
            self.value = value
        def unwrap(self):
            return self.value
        def __repr__(self):
            return f"NotEvaluated({self.value!r})"

def nest_args(tokens):
    stack = [[]]
    for token in tokens:
        if not isinstance(token, str):
            stack[-1].append(token)
            continue
        if token in OPEN_P:
            new_list = []
            stack[-1].append(new_list)
            stack.append(new_list)
        elif token in CLOSE_P:
            if len(stack) == 1:
                raise ValueError("Mismatched parentheses")
            stack.pop()
            if token == ")":
                stack[-1].append(tuple(stack[-1].pop()))
        else:
            stack[-1].append(token)
    if len(stack) > 1:
        raise ValueError(f"Mismatched parentheses: {tokens}")
    return stack[0]


def get_block(code, current_p):
    "Get a code block"
    pos, file, _, _ = code[current_p]
    p = current_p + 1
    k = 1
    res = []
    while p < len(code):
        _, _, ins, _ = code[p]
        if ins in INC_EXT:
            k += 1
        elif ins in INC:
            k -= INC[ins]
        elif ins in DEC:
            k -= 1
        if k == 0:
            break
        else:
            res.append(code[p])
        p += 1
    else:
        print(f"Error in line {pos} file {file!r}\nCause: Block wasnt closed!")
        return None
    return p, res


# Functions in utils that couldnt be imported
# without dark magic.

def parse_match(frame, body, value):
    name = None
    np = 0
    ft = False
    if value != constants.nil:
        for p, [pos, file, ins, args] in enumerate(body):
            if ins == "as":
                varproc.rset(frame[-1], process_args(frame, args)[0], value)
            elif ins == "case":
                if (v := process_args(frame, args))[0]:
                    temp = get_block(body, p)
                    if temp is None:
                        error.error(pos, file, "Expected a case block!")
                        return error.SYNTAX_ERROR
                    if name:
                        frame[-1][name] = value
                    res = run_code(temp[1], frame=frame)
                    if res != error.FALLTHROUGH:
                        return res
                    ft = True
            elif ins == "with":
                if (v := process_args(frame, args))[0] == value:
                    temp = get_block(body, p)
                    if temp is None:
                        error.error(pos, file, "Expected a case block!")
                        return error.SYNTAX_ERROR
                    if name:
                        frame[-1][name] = value
                    res = run_code(temp[1], frame=frame)
                    if res != error.FALLTHROUGH:
                        return res
                    ft = True
            elif ins == "default":
                temp = get_block(body, p)
                if temp is None:
                    error.error(pos, file, "Expected a case block!")
                    return error.SYNTAX_ERROR
                if name:
                    frame[-1][name] = value
                return run_code(temp[1], frame=frame)
    else:
        for p, [pos, file, ins, args] in enumerate(body):
            if ins == "case":
                if (v := process_args(frame, args))[0]:
                    temp = get_block(body, p)
                    if temp is None:
                        error.error(pos, file, "Expected a case block!")
                        return error.SYNTAX_ERROR
                    if name:
                        frame[-1][name] = value
                    res = run_code(temp[1], frame=frame)
                    if res != error.FALLTHROUGH:
                        return res
                    ft = True
            elif ins == "default":
                temp = get_block(body, p)
                if temp is None:
                    error.error(pos, file, "Expected a case block!")
                    return error.SYNTAX_ERROR
                if name:
                    frame[-1][name] = value
                return run_code(temp[1], frame=frame)
    return 0


def parse_dict(frame, temp_name, body):
    data = {}
    varproc.rset(frame[-1], temp_name, data)
    for p, [pos, file, ins, args] in enumerate(body):
        argc = len(args)
        if ins == "set" and argc == 3 and args[1] == "=>":
            name, _, value = args
            data[name] = value
        elif ins == "def" and argc == 1:
            name, = args
            # TODO: check if previous item is a int
            data[name] = tuple(data.items())[-1][1] + 1
        else:
            error.error(pos, file, f"Invalid statement!")
            return 1

def flatten_dict(d, parent_key="", sep=".", seen=None, hide=False):
    if seen is None:
        seen = set()
    items = {}
    dict_id = id(d)
    if dict_id in seen:
        return d
    seen.add(dict_id)
    for key, value in d.items():
        if hide and isinstance(key, str) and key.startswith("_"):
            continue
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_dict(value, new_key, sep, seen))
        elif isinstance(value, (list, tuple)):
            items[f"{new_key}"] = value
            for i, item in enumerate(value):
                items[f"{new_key}[{i}]"] = item
        else:
            items[new_key] = value
    seen.remove(dict_id)
    return items


methods = {}
matches = {}


# Need I explain?
def is_int(arg):
    arg = arg.replace("_", "")
    if arg.count("-") > 1:
        return False
    return arg.replace("-", "").replace(",", "").isdigit()


def is_hex(arg):
    if not arg.startswith("0x"):
        return False
    try:
        int(arg[2:], 16)
        return True
    except:
        return False


def is_bin(arg):
    if not arg.startswith("0b"):
        return False
    try:
        int(arg[2:], 2)
        return True
    except:
        return False


def is_float(arg):
    arg = arg.replace("_", "")
    if arg.count("-") > 1 or 0 <= arg.count(".") > 1:
        return False
    return arg.replace("-", "").replace(",", "").replace(".", "").isdigit()


def is_id(arg):
    return arg.replace(".", "").replace("_", "a").replace(":", "a").replace("?", "a").replace("-", "a").isalnum()


def is_fvar(arg):
    return arg.startswith(":") and is_id(arg[1:])


def is_pfvar(arg):
    return arg.startswith(".:") and is_id(arg[2:])


def expr_preruntime(arg):
    "Process arguments at preprocessing"
    if not isinstance(arg, str):
        return arg
    elif is_int(arg):
        return int(arg.replace(",", ""))
    elif is_float(arg.replace(",", "")):
        return float(arg)
    elif is_bin(arg):
        return int(arg, 2)
    elif is_hex(arg):
        return int(arg, 16)
    elif arg == "true":
        return constants.true
    elif arg == "false":
        return constants.false
    elif arg == "none":
        return constants.none
    elif arg == "nil":
        return constants.nil
    elif arg == "...":
        return constants.elipsis
    elif arg == ".dict":
        return {}
    elif arg == ".list":
        return []
    elif arg == ".set":
        return set()
    elif arg == ".None":
        return None
    elif arg == "π":
        return 22/7
    return arg


def expr_runtime(frame, arg):
    "Process an argument at runtime"
    if isinstance(arg, list):
        return evaluate(frame, arg)
    elif not isinstance(arg, str):
        return arg
    elif is_fvar(arg):
        if varproc.debug_settings["allow_automatic_global_name_resolution"]:
            v = varproc.rget(
                frame[-1],
                arg[1:],
                default=varproc.rget(frame[0], arg[1:]),
            )
        else:
            v = rget(frame[-1], arg[1:])
        if get_debug("disable_nil_values") and v == constants.nil:
            raise Exception(f"{arg!r} is nil!")
        return v
    elif arg == ".input":
        return input()
    elif is_id(arg):
        return arg
    elif arg.startswith('"') and arg.endswith('"'):
        return arg[1:-1]
    elif arg.startswith("'") and arg.endswith("'"):
        text = arg[1:-1]
        for name, value in flatten_dict(frame[-1]).items():
            text = text.replace(f"${{{name}}}", str(value))
            if (tmp:=f"${{{name}!}}") in text: text = text.replace(tmp, repr(value))
        return text
    elif (arg.startswith("{") and arg.endswith("}")) or arg in sep or arg in special_sep:
        return arg
    elif arg in ("?tuple", "?args", "?float", "?int", "?string", "?bytes", "?set", "?list", "nil?", "none?", "def?") or arg in sym:
        return arg
    else:
        raise Exception(f"Invalid literal: {arg}")


def add_method(name=None, from_func=False, process=True):
    def wrapper(func):
        fname = name if name is not None else getattr(func, "__name__", "_dump")
        methods[fname] = (
            lambda *arg: func(None, None, *arg) if from_func else func,
            process,
        )
        return func

    return wrapper


def my_range(start, end):
    def pos(start, end):
        while start < end:
            yield start
            start += 1

    def neg(start, end):
        while start > end:
            yield start
            start -= 1

    return pos(start, end) if start < end else neg(start, end)


def is_static(frame, code):
    for i in code:
        if isinstance(i, list):
            if not is_static(frame, i):
                return False
        elif not isinstance(i, str):
            continue
        elif i in RT_EXPR:
            return False
        elif is_pfvar(i) and varproc.rget(frame[-1], i[2:], default=None, meta=False) is None:
            return False
        elif is_fvar(i):
            return False
    return True


def to_static(frame, code):
    for pos, i in enumerate(code):
        if isinstance(i, list):
            if is_static(frame, i):
                code[pos] = evaluate(frame, to_static(frame, i))
            else:
                code[pos] = to_static(frame, i)
        elif not isinstance(i, str):
            continue
        elif is_pfvar(i) and (not (var:=varproc.rget(frame[-1], i[2:], default=None)) is None):
            code[pos] = var
    return code


def get_names(args):
    names = set()
    for i in args:
        if not isinstance(i, str):
            continue
        if isinstance(i, list):
            names.update(*get_names(i))
        elif is_fvar(i) or is_var(i):
            names.add(i[1:])
    return names


class kwarg:
    def __init__(self, name, value=None):
        self.name = name
        self.value = value
    def keys():
        return [name]
    def __getitem__(self, _):
        return self.value
    def __repr__(self):
        return f"<{self.name} = {self.value!r}>"

def evaluate(frame, expression):
    "Evaluate an expression"
    if not isinstance(expression, (list, tuple)):
        return expression
    processed = process_args(frame, expression)
    if len(processed) == 3 and isinstance(processed[1], str) and processed[1] in simple_ops:
        return simple_ops[processed[1]](processed[0], processed[2])
    elif processed and processed[0] == "!":
        return processed[1:]
    elif len(processed) == 2 and processed[0] == "not":
        return constants.true if not processed[1] else constants.false
    elif len(processed) == 2 and processed[0] == "-":
        return -processed[1]
    elif len(processed) == 2 and processed[0] == "~":
        return ~processed[1]
    elif len(processed) == 2 and processed[0] == "type":
        return getattr(type(processed[1]), "__name__", constants.nil)
    elif len(processed) >= 1 and processed[0] == "sum":
        args = processed[1:]
        t = type(args[0])
        start = args[0]
        for i in args[1:]:
            start += t(i)
        return start
    elif len(processed) == 2 and processed[0] == "eval":
        return evaluate(frame, processed[1])
    elif len(processed) == 2 and processed[0] == "fast-format":
        local = flatten_dict(frame[-1], hide=True)
        text = processed[1]
        for name, value in flatten_dict(frame[-1]).items():
            if f"${{{name}}}" in text:
                text = text.replace(f"${{{name}}}", str(value)) 
        return text
    elif len(processed) == 2 and processed[0] == "to_ascii":
        return chr(processed[1])
    elif len(processed) == 2 and processed[0] == "from_ascii":
        return ord(processed[1])
        return processed[1] % processed[2]
    elif len(processed) == 2 and processed[0] == "len":
        return len(processed[1])
    elif len(processed) == 2 and processed[0] == "head:rest:tail":
        head, *rest, tail = processed[1]
        return head, rest, tail
    elif len(processed) == 2 and processed[0] == "head:rest":
        head, *rest = processed[1]
        return head, rest
    elif len(processed) == 2 and processed[0] == "rest:tail":
        *res, tail = processed[1]
        return rest, tail
    elif len(processed) == 2 and processed[0] == "head":
        return processed[1][0]
    elif len(processed) == 2 and processed[0] == "head":
        return processed[1][-1]
    match (processed):
        # conditionals
        case ["if", value, "then", true_v, "else", false_v]:
            return true_v if value else false_v
        case [obj, tuple(index)]:
            if not isinstance(obj, (tuple, list, str)):
                return constants.nil
            if isinstance(obj, (tuple, list, str)) and index[0] >= len(obj):
                return constants.nil
            elif isinstance(obj, dict) and index[0] not in obj:
                return constants.nil
            else:
                return obj[index[0]]
        # types
        case ["tuple", *lst]:
            return tuple(lst)
        case ["?tuple", lst]:
            return tuple(lst)
        case ["?set", lst]:
            return set(lst)
        case ["?dict", lst]:
            return dict(lst)
        case ["?string", item]:
            return str(item)
        case ["?bytes", item]:
            try:
                return bytes(item)
            except:
                return constants.nil
        case ["?int", item]:
            try:
                return int(item)
            except:
                return constants.nil
        case ["?float", item]:
            try:
                return float(item)
            except:
                return constants.nil
        case ["dict", *args]:
            temp = {}
            for i in args:
                temp.update(i)
            return temp
        # values
        case ["nil?", value]:
            return value == constants.nil
        case ["none?", value]:
            return value == constants.none
        case ["def?", name]:
            value = varproc.rget(frame[-1], name, default=None, meta=False)
            if value is None:
                return constants.false
            return constants.true
        # ranges
        case ["rawrange", num]:
            return range(num)
        case ["range", num]:
            return tuple(range(num))
        case ["drange", num]:
            return tuple(my_range(0, num))
        case ["drawrange", num]:
            return my_range(0, num)
        case ["drange", num, end]:
            return tuple(my_range(num, end))
        case ["drawrange", num, end]:
            return my_range(num, end)
        case ["length", item]:
            try:
                return len(item)
            except:
                return 0
        # values
        case ["set", name, "=", value]:
            varproc.rset(frame[-1], name, value)
            return value
        case ["fset", name, "=", value]:
            varproc.rset(frame[-1], name, value, meta=False)
            return constants.nil
        case ["#", method, *args] if method in methods:
            return methods[method](frame, *args)[0]
        case ["##", ins, *args]:
            return ins(frame, "_", *args)[0]
        case [obj, "@", method, *args] if hasattr(
            obj, method
        ):  # direct python method calling
            if args and isinstance(args[0], pah.arguments_handler):
                return args[0].call(getattr(obj, method))
            return getattr(obj, method)(*args)
        # other
        case ["?args", *args]:
            lst = []
            dct = {}
            for i in args:
                if isinstance(i, kwarg):
                    dct[i.name] = i.value
                else:
                    lst.append(i)
            temp = pah.arguments_handler(lst, dct)
            return temp
        case default:
            for name, fn in matches.items():
                try:
                    if not (res:=fn(frame, default)) is None:
                        return res
                except:
                    raise Exception(f"Error while evaluating: {default}\n{traceback.format_exc()}") from None
    raise Exception(f"Unknown expression: {processed!r}")

sep = " ,"
special_sep = "@()+/*#[]π<>=!π%"
sym = [">=", "<=", "->", "=>", "==", "!=", "**", "//"]

def group(text):
    res = []
    str_tmp = []
    id_tmp = []
    this = False
    is_bytes = False
    rq = False
    quotes = {"str": '"', "pre": "}", "str1": "'"}
    str_type = "str"
    for i in text:
        if str_tmp:
            if this:
                if i in chars:
                    str_tmp.append(chars[i])
                else:
                    str_tmp.append(i)
                this = False
                continue
            if i == "\\":
                this = True
            elif i == quotes[str_type]:
                text = "".join(str_tmp) + quotes[str_type]
                res.append(text[1:-1].encode("utf-8") if is_bytes else text)
                if is_bytes: is_bytes = False
                str_tmp.clear()
            else:
                str_tmp.append(i)
            continue
        elif i in sep:
            if id_tmp:
                res.append("".join(id_tmp))
                id_tmp.clear()
        elif i in special_sep:
            if id_tmp:
                res.append("".join(id_tmp))
                id_tmp.clear()
            res.append(i)
        elif i in "\"{'":
            if id_tmp:
                if len(id_tmp) == 5 and "".join(id_tmp) == "cstr?":
                    is_bytes = True
                    id_tmp.clear()
                else:
                    res.append("".join(id_tmp))
                    id_tmp.clear()
            str_tmp.append(i)
            if i == '"':
                str_type = "str"
            elif i == "{":
                str_type = "pre"
            elif i == "'":
                str_type = "str1"
            else:
                str_type = "str"
        else:
            id_tmp.append(i)
    if id_tmp:
        res.append("".join(id_tmp))
    nres = []
    while res:
        i = res.pop(0)
        if not isinstance(i, str):
            nres.append(i)
        elif res and isinstance(res[0], str) and (tmp:=i+res[0]) in sym:
            nres.append(tmp)
            res.pop(0)
        else:
            nres.append(i)
    return nres


def exprs_preruntime(args):
    return [*map(expr_preruntime, args)]

def process_arg(frame, e):
    return expr_runtime(frame, e)

def process_args(frame, e):
    return list(map(lambda x: expr_runtime(frame, x), e))

class argproc_setter:
    def set_run(func):
        global run_code
        run_code = func