import argparse
import configparser
import os
import re
from typing import Optional, TextIO

from . import constants

def read_config_file(config, file_paths):
    for file_path in file_paths:
        try:
            config.read(os.path.expanduser(file_path))
            return config.get("settings", "exclude").replace(" ", "").split(",")
        except FileNotFoundError:
            continue
        except configparser.NoSectionError:
            continue
    return []


config = configparser.ConfigParser()
config_file_paths = ["~/Scripts/gendia_config.ini", "~/gendia_config.ini"]
exclude = read_config_file(config, config_file_paths)

maxdepth: int = None
currdepth: int = 0
showIcons: bool = False
matchpattern: str = ""
notmatchpattern: str = ""


def get_color(entry: str) -> str:
    """Returns color based on file type."""

    if os.path.isdir(entry):
        return constants.AnsiColor.BLUE
    elif os.path.islink(entry):
        return constants.AnsiColor.UNDERLINE

    ext_off = entry.find(".")

    try:
        entry_ext = entry[ext_off:] if ext_off != -1 else None
        return constants.ASSIGNED_COLORS[entry_ext]
    except KeyError:
        pass

    return constants.AnsiColor.RESET

def get_icon(entry : str) -> str:
    """Returns icon based on file type."""
    if os.path.isdir(entry):
        return constants.Icons.DIR
    
    ext_start_ind = entry.find(".")
    ext = entry[ext_start_ind:]

    if ext_start_ind == -1 or ext not in constants.ASSIGNED_ICONS.keys():
        return constants.Icons.FILE
    
    return constants.ASSIGNED_ICONS[ext]


def print_tree(
    directory: str,
    prefix: str = "",
    output: Optional[TextIO] = None,
    hidden: bool = False,
    directories_only: bool = False,
) -> None:
    global currdepth
    global maxdepth
    global exclude
    global matchpattern
    global showIcons 

    if currdepth == maxdepth:
        return

    currdepth += 1

    try:
        # List all entries in the directory
        entries = os.listdir(directory)

        # Filter entries based on pattern
        if matchpattern:
            entries = [entry for entry in entries if re.search(matchpattern, entry)]

        # Filter entries based on not pattern
        if notmatchpattern:
            entries = [
                entry for entry in entries if not re.search(notmatchpattern, entry)
            ]

        # Filter entries based on directories_only
        if directories_only:
            entries = [
                entry
                for entry in entries
                if os.path.isdir(os.path.join(directory, entry))
            ]

        # Filter entries based on hidden
        if not hidden:
            entries = [entry for entry in entries if not entry.startswith(".")]

        # Filter entries based on exclude
        if exclude:
            entries = [entry for entry in entries if entry not in exclude]

        # Sort the entries
        entries = sorted(
            entries,
            key=lambda s: (not os.path.isdir(f"{directory}/{s}"), s.lower()),
        )

    except PermissionError:
        print(f"\033[31mPermission denied to access {directory}\033[0m")
        return
    
    index = 0
    for entry in entries:
        path = f"{directory}/{entry}"
        is_last = index == len(entries) - 1
        color = get_color(path) if output is None else ""
        icon = get_icon(path) if showIcons else ""
        reset = constants.AnsiColor.RESET if output is None else ""

        # Print the current item with the appropriate prefix
        line = (
            f"{prefix}└──{icon}{color}{entry}{reset}"
            if is_last
            else f"{prefix}├──{icon}{color}{entry}{reset}"
        )
        if output:
            output.write(line + "\n")
        else:
            print(line)

        # Recursively print the contents of directories
        if os.path.isdir(path):
            new_prefix = f"{prefix}    " if is_last else f"{prefix}│   "
            print_tree(path, new_prefix, output, hidden, directories_only)
        
        index += 1

    currdepth -= 1


def main() -> None:
    global exclude
    global maxdepth
    global matchpattern
    global notmatchpattern
    global showIcons 

    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Display a color-coded tree-like directory structure"
    )
    parser.add_argument(
        "directory",
        type=str,
        nargs="?",
        default=".",
        help="The directory to display (default: current directory)",
    )
    parser.add_argument(
        "-o", "--output", type=str, help="The output file to write the diagram to"
    )
    parser.add_argument(
        "-H",
        "--hidden",
        action="store_true",
        help="Exclude hidden files and directories",
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 1.6.1")
    parser.add_argument(
        "--exclude",
        type=str,
        help="Exclude files and directories that match the given pattern",
    )
    parser.add_argument("--depth", type=int, help="Limit the depth of the tree diagram")
    parser.add_argument("-d", action="store_true", help="Show directories only")
    parser.add_argument("-P", type=str, help="Show only files matching the pattern")
    parser.add_argument("-l", type=str, help="Do not show files matching the pattern")
    parser.add_argument(
        "--ignore-config", action="store_true", help="Ignore the configuration file"
    )
    parser.add_argument("-i", "--icon", action="store_true", help="Show icon base on file type")
    args = parser.parse_args()

    try:
        exclude.extend(args.exclude.replace(" ", "").split(","))
    except AttributeError:
        exclude.extend([])

    maxdepth = args.depth
    matchpattern = args.P
    notmatchpattern = args.l
    showIcons = args.icon

    if args.ignore_config:
        exclude = []

    # Get the absolute path of the directory
    directory = os.path.abspath(args.directory)
    if os.path.isdir(directory):
        try:
            if args.output:
                try:
                    with open(args.output, "w+") as output_file:
                        output_file.write(directory + "\n")
                        print_tree(
                            directory,
                            output=output_file,
                            hidden=args.hidden,
                            directories_only=args.d,
                        )
                    print(
                        f"\033[32mDirectory structure written to {args.output}\033[0m"
                    )
                except IsADirectoryError:
                    print(
                        f"\033[31m{args.output} is a directory, please provide a valid file name\033[0m"
                    )
                except PermissionError:
                    print(f"\033[31mPermission denied to write to {args.output}\033[0m")
            else:
                print(f"\033[1m{directory}\033[0m")
                print_tree(
                    directory=directory, hidden=args.hidden, directories_only=args.d
                )
        except KeyboardInterrupt:
            print("\033[31m\nProgram terminated\033[0m")
    else:
        print(f"\033[31m{directory} is not a valid directory\033[0m")


if __name__ == "__main__":
    main()
