# PMFDPL
# Package Manager For DPL
# Damn Im making my life harder...

import os
from re import sub
import sys
import zipfile
import json
import shutil

import subprocess
import shlex

from itertools import zip_longest

mfile = None

import os
import subprocess
import shutil

def summon_editor(filepath):
    editor = os.environ.get('EDITOR') or os.environ.get('VISUAL')
    fallback_editors = ["vim", "nvim", "subl", "vi", "nano", "notepad", "ed"]
    if not editor:
        for ed in fallback_editors:
            if shutil.which(ed):
                editor = ed
                break
    if not editor:
        raise RuntimeError("No text editor found. Please set the $EDITOR or $VISUAL environment variable.")
    subprocess.run([editor, filepath])

def compare_zip_contents(zip1_path, zip2_path):
    with zipfile.ZipFile(zip1_path) as zip1, zipfile.ZipFile(zip2_path) as zip2:
        names1 = set(zip1.namelist())
        names2 = set(zip2.namelist())

        only_in_zip1 = names1 - names2
        only_in_zip2 = names2 - names1
        in_both = names1 & names2

        if sorted(only_in_zip1): print("Only in", os.path.basename(zip1_path))
        for name in sorted(only_in_zip1):
            print(f"  {name}")

        if sorted(only_in_zip2): print("\nOnly in", os.path.basename(zip2_path))
        for name in sorted(only_in_zip2):
            print(f"  {name}")

        if sorted(in_both): print("\nDiffering files:")
        for name in sorted(in_both):
            with zip1.open(name) as f1, zip2.open(name) as f2:
                content1 = f1.read()
                content2 = f2.read()
                if content1 != content2:
                    print(f"------ File [{name}] ------")
                    f2.seek(0); f1.seek(0)
                    for pos, [l1, l2] in enumerate(zip_longest(f1, f2), 1):
                        if l1 != l2:
                            print(f"  Line {pos}\n  Current: {l2.decode(errors='ignore').rstrip()}\n  Previous: {l1.decode(errors='ignore').rstrip()}")

        if sorted(in_both): print("\nIdentical files:")
        for name in sorted(in_both):
            with zip1.open(name) as f1, zip2.open(name) as f2:
                content1 = f1.read()
                content2 = f2.read()
                if content1 == content2:
                    print(f"  {name}")



def is_same_zip(zip1_path, zip2_path):
    with zipfile.ZipFile(zip1_path) as zip1, zipfile.ZipFile(zip2_path) as zip2:
        names1 = set(zip1.namelist())
        names2 = set(zip2.namelist())
        only_in_zip1 = names1 - names2
        only_in_zip2 = names2 - names1
        in_both = names1 & names2
        if sorted(only_in_zip1): return False
        if sorted(only_in_zip2): return False
        for name in sorted(in_both):
            with zip1.open(name) as f1, zip2.open(name) as f2:
                content1 = f1.read()
                content2 = f2.read()
                if content1 != content2:
                    return False
        for name in sorted(in_both):
            with zip1.open(name) as f1, zip2.open(name) as f2:
                content1 = f1.read()
                content2 = f2.read()
                if content1 != content2:
                    return False
    return True

def find_upwards(name):
    curpath = os.getcwd()
    t = 50
    if os.path.exists(path:=os.path.join(curpath, name)):
        return path
    while (curpath:=os.path.dirname(curpath)) and t > 0:
        if os.path.exists(path:=os.path.join(curpath, name)):
            return path
            t -= 1
    return None

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path+".zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname=rel_path)

def unzip_archive(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        zipf.extractall(extract_to)

def make_project(name):
    # Tree should look like
    # {name}
    # | versions/
    # | src/
    # | pkg_meta.json
    # | README.txt
    # | include-dpl.txt
    
    print(f"Initialized package {name!r}")
    
    dirs = [
        name,
        os.path.join(name, "src"),
        os.path.join(name, "versions")
    ]
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    with open(os.path.join(name, ".root"), "w") as f: f.write("this file is to recognize the root folder. DO NOT REMOVE!")
    with open(os.path.join(name, "pkg_meta.json"), "w") as f:
        f.write(json.dumps({
            "project_name":name,
            "author":"author_name",
            "description":"description",
            "install_script":"",
            "main_script":"main.dpl", # relative to project_root/src
            "flags":["-skip-non-essential"],
            "current_version":"???"
        }))
    with open(os.path.join(name, "README.txt"), "w") as f: f.write("""Welcome to DPLPM!

DPLPM is not a replacement for git!
DPLPM is merely a simple package manager specifically for DPL projects.
DPLPM is not a full fledged tool but rather a temporary solution.

DPLPM offers simplicity and functionality.

Features supported by DPLPM
* Versions (basically branches though order isnt kept)
* Observing differences (via `dplpm compare other_version version`)
  If '-current' is supplied as [version] it will use the current version for 'src' dir
  basically automatically generating a temporary version in 'versions' dir
* Running the main script (via `dplpm run ...args`)
* Minimalistic configuration (`pkg_meta.json`)
* Simplistic dir structure.
* DOESNT DOWNLOAD BLOAT

If youre looking for a more better alternative use
git along with the `dpl package` command.""")
    with open(os.path.join(name, "src", "main.dpl"), "w") as f: f.write('&use {std/text_io.py}\nio:println "Hello, world!"')
    with open(os.path.join(name, "include-dpl.txt"), "w") as f: f.write("# DPL detects this file when we import the package.\nsrc/main.dpl")


def update_pkg_meta(name, value):
    if (path:=find_upwards("pkg_meta.json")):
        try:
            with open(path) as f:
                configs =  json.loads(f.read())
        except:
            print(":: Problem while loading pkg_meta.json")
            return 1
    else:
        configs = {}
    node = configs
    while name:
        n = name.pop(0)
        if len(name) != 0 and n in node and isinstance(node[n], dict):
            node = node[n]
        elif len(name) == 0 and n in node:
            node[n] = value
        else:
            print(":: Invalid attribute!")
            return 1
    with open(path, "w") as f:
        f.write(json.dumps(configs))


def get_pkg_meta():
    if (path:=find_upwards("pkg_meta.json")):
        try:
            with open(path) as f:
                return json.loads(f.read())
        except:
            print(":: Problem while loading pkg_meta.json")
            return {}
    return {}

def set_config(node, name="???"):
    print("Editing", name)
    while True:
        act = input(": ").strip()
        if act == "help":
            print("set [name] - set attribute [name]\nlist - lists attributes\nsave - write changes\nexit - exit the program.")
        elif act.startswith("set "):
            if act[4:] in node:
                while True:
                    try:
                        if isinstance(node[act[4:]], dict): set_config(node[act[4:]], act[4:])
                        else: node[act[4:]] = type(node[act[4:]])(input(f"{act[4:]} = "))
                        break
                    except:
                        print("Invalid input!")
            else:
                print("Invalid attribute!")
        elif act == "list":
            print(f"Editing {name}")
            for n, v in node.items():
                print(f"{n} = {v!r}")
        elif act == "exit":
            return

def edit_main():
    main_path = get_pkg_meta().get("main_script")
    if main_path: summon_editor(path_from_root("src", main_path))
    else: print(":: Main script seems to be not specified in config!"); exit(1)

def configure_pkg_meta():
    root_path = find_upwards(".root")
    if (path:=find_upwards("pkg_meta.json")):
        try:
            configs = json.loads(open(path).read())
        except:
            print(":: Problem while loading pkg_meta.json")
            return 1
    else:
        print(":: Config data not found.")
        return 1
    print("Config TUI\nhelp for more.")
    while True:
        act = input(": ").strip()
        if act == "help":
            print("set [name] - set attribute [name]\nlist - lists attributes\nsave - write changes\nexit - exit the program.")
        elif act.startswith("set "):
            if act[4:] in configs:
                while True:
                    try:
                        if isinstance(configs[act[4:]], dict): set_config(configs[act[4:]], act[4:])
                        else: configs[act[4:]] = type(configs[act[4:]])(input(f"{act[4:]} = "))
                        break
                    except:
                        print("Invalid input!")
            else:
                print("Invalid attribute!")
        elif act == "list":
            for n, v in configs.items():
                print(f"{n} = {v!r}")
        elif act == "exit":
            return
        elif act == "save":
            with open(path, "w") as f:
                f.write(json.dumps(configs))

def path_from_root(*path):
    root_path = os.path.dirname(find_upwards(".root"))
    return os.path.join(root_path, *path)

def clear_directory(path):
    if not os.path.isdir(path):
        raise ValueError(f"{path} is not a valid directory.")
    for item in os.listdir(path):
        item_path = os.path.join(path, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")

def run(code):
    env = {".stack":[]}
    c = []
    p = 0
    for pos, line in enumerate(code.split("\n"), 1):
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        elif line.endswith(":"):
            env[line[:-1]] = p
            continue
        c.append((pos, shlex.split(line)))
        p += 1
    p = 0
    while p < len(c):
        pos, line = c[p]
        env["line_"] = p
        env["line__"] = p+1
        res = handle_cmd(list(map(lambda x: x if not x.startswith("$") else env.get(x[1:], x), line)), env)
        if isinstance(res, int):
            print(f"\nError at line {pos}")
            return res
        elif isinstance(res, tuple):
            p = res[0]
            continue
        p += 1

class control:
    @staticmethod
    def push(version):
        zip_folder(path_from_root("src"), path_from_root("versions", str(version)))
        update_pkg_meta(["current_version"], version)
    @staticmethod
    def pull(version):
        zip_folder(path_from_root("src"), (temp_path:=path_from_root("versions", "current")))
        path = path_from_root("versions", str(version)+".zip")
        if not os.path.exists(path):
            print(":: Version", version, "doesnt exist!")
            return 1
        for ziped in os.listdir(path_from_root("versions")):
            if ziped == "current.zip" or not ziped.endswith(".zip"): continue
            if (t:=is_same_zip(temp_path+".zip", path_from_root("versions", ziped))):
                break
        else:
            print(":: Unsaved work!")
            compare_zip_contents(path_from_root("versions", version+".zip"), temp_path+".zip")
            os.remove(path_from_root("versions", "current.zip"))
            return 1
        clear_directory(path_from_root("src"))
        unzip_archive(path, path_from_root("src"))
        print(":: Pulled", version)
        update_pkg_meta(["current_version"], version)
    @staticmethod
    def get_config():
        return get_pkg_meta()

def handle_cmd(args, env=None):
    env = env if env is not None else {}
    match args:
        case ["init", name]:
            make_project(name)
        case ["init"]:
            make_project(".")
        case ["config"]:
            return configure_pkg_meta()
        case ["pull", version]:
            control.pull(version)
        case ["view", version]:
            if not os.path.exists(path:=path_from_root("versions", f"msg-{version}.txt")):
                print("Doesnt exist!")
                return 1
            with open(path, "r") as f:
                print(">>", version)
                print(f.read()+"\n")
        case ["version"]:
            print(":: "+get_pkg_meta().get("current_version", "Version couldnt be found!"))
        case ["edit-main"]:
            edit_main()
        case ["push", version]:
            control.push(version)
            print(":: Pushed", version)
        case ["message", version]:
            with open(path_from_root("versions", f"msg-{version}.txt"), "w") as f:
                with open(path_from_root("temp.txt"), "w") as temp: temp.write("Message here!")
                summon_editor(path_from_root("temp.txt"))
                with open(path_from_root("temp.txt"), "r") as temp:
                    f.write(temp.read())
                os.remove(path_from_root("temp.txt"))
        case ["list"]:
            v = filter(lambda x: x.endswith(".zip"), os.listdir(path_from_root("versions")))
            print(f"\nVersions [{len(v:=tuple(v)):,} total]:")
            for ver in v:
                print("*", ver[:-4])
        case ["remove", version]:
            path = path_from_root("versions", version+".zip")
            if not os.path.isfile(path):
                print(":: Version does not exist!")
                return 1
            if input("Enter yes to delete version: ") == "yes":
                os.remove(path)
        case ["compare", version, current]:
            root_path = os.path.dirname(find_upwards(".root"))
            ver = path_from_root("versions", str(version)+".zip")
            cur = path_from_root("versions", str(current)+".zip")
            if not os.path.exists(ver):
                print(f":: {version} doesnt exist!")
                return 1
            if current == "-current":
                zip_folder(path_from_root("src"), (temp_path:=path_from_root("versions", "current")))
                cur = path_from_root("versions", "current.zip")
            elif not os.path.exists(cur):
                if (input(f":: {current} hasnt been pushed yet!\nPush automatically? [y/N] ").lower()+" ")[0] == "y":
                    zip_folder(path_from_root("src"), path_from_root("versions", cur[:-4]))
                    print(":: Pushed", current)
                else:
                    return 1
            compare_zip_contents(ver, cur)
        case ["if", var, "=>", *cmd]:
            if env.get(var): return handle_cmd(cmd, env)
        case ["set", var, "=", *value]:
            try:
                env[var] = eval(" ".join(map(str,value)), {"__builtins__":{}, "os":os, **env})
            except:
                env[var] = " ".join(map(str,value))
        case ["set", var, "<<", "stdin"]:
            env[var] = input()
        case ["echo", *value]:
            print(*value)
        case ["print", *value]:
            print(*value, end="")
        case ["vdump", name]:
            print(env.get(name, ""), end="")
        case ["vsdump"]:
            print(*env.keys(), sep=",")
        case ["exec", file]:
            with open(file) as f:
                return run(f.read())
        case ["goto", index]:
            return index,
        case ["call", index, "=>", current]:
            env[".stack"].append(current)
            return index,
        case ["return"]:
            return env[".stack"].pop(),
        case ["exit", code]:
            sys.exit(code)
        case ["cmd", command]:
            return os.system(command)
        case ["install", *args]:
            file = get_pkg_meta().get("install_script")
            if not file:
                print(':: Invalid installation file!')
                return 1
            return subprocess.run(["bash", file, *args]).returncode
        case ["run", *args]:
            data = get_pkg_meta()
            file = data.get("main_script")
            file = path_from_root("src", file)
            if (not file) or not os.path.isfile(file):
                print(':: Invalid path to main script!', data)
                return 1
            return subprocess.run(["python3", mfile, *data.get("flags", []), "run", file, *args]).returncode
        case ["help"]:
            print("""Basic Commands

install [...args] - Installs the package if install_script is set in pkg_meta.json
push [version] [message?] - Saves the current source in the specified version.
                            If message is specified it is also saved.
pull [version] - Loads the specified version.
view [version] - View the message with the associated version.
list - list all versions.
init [name] - Initialize a new package [name]
init - Initialize the new package in the current directory.
run [...args] - runs the main script.
version - prints current version""")
        case cmd:
            print(cmd, "is not recognized!")
            return 1

if __name__ == "__main__":
    sys.exit(handle_cmd(sys.argv[1:]) or 0)