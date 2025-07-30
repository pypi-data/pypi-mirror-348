import re
import sys
from colorama import Fore, Style

def print_usage():
    print("hlcli (--red|--green|--blue|--yellow|regular_expression)*")
    print("Highlight regular expressions in different colours.")
    print("Colours come before expressions. You can change colour.")

def main():
    color = Fore.RED
    expressions = []

    if "--help" in sys.argv[1:]:
        print_usage()
        sys.exit(0)


    for x in sys.argv[1:]:
        if x.startswith("--"):
            match x:
                case "--red":
                    color = Fore.RED
                case "--blue":
                    color = Fore.BLUE
                case "--green":
                    color = Fore.GREEN
                case "--yellow":
                    color = Fore.YELLOW
                case _:
                    print_usage()
                    sys.exit(1)
            continue
        expressions.append((color, x))

    for line in sys.stdin:
        for color, expression in expressions:
            m = re.search(expression, line)
            if m:
                start, end = m.span()
                before = line[:start]
                highlighed = line[start:end]
                end = line[end:]
                print(before, end="")
                print(color, end="")
                print(highlighed, end="")
                print(Style.RESET_ALL, end="")
                print(end, end="", flush=True)
                break
        else:
            print(line, flush=True, end="")
