execGlobal=globals()
from time import sleep
import curses
from ASnake import build, execPy, ASnakeVersion
import subprocess
import io
from contextlib import redirect_stdout

import sys
import platform
compileDict = {'CPython': 'Python', 'PyPy': 'PyPy3'}

if hasattr(sys, "pyston_version_info"):
    # ^ Pyston dev's suggested this: https://github.com/pyston/pyston/issues/39
    # What scaredy cats!!
    compileTo = 'Pyston'
else:
    compileTo = compileDict[platform.python_implementation()]
del sys, compileDict, platform


# constants
ReplVersion = 'v0.2.1'
PREFIX = ">>> "


# for debugging only
def file_out(write_mode, *args):
    with open("streams.txt", write_mode, encoding='utf-8') as f:
        f.write(f"{args}\n")


def buildCode(code):
    global variableInformation
    output = build(code, comment=False, optimize=False, debug=False, compileTo=compileTo,
        pythonVersion=3.9, enforceTyping=True, variableInformation=variableInformation,
        outputInternals=True)
    variableInformation = output[2]
    return output[0]


bash_history = []
variableInformation = {}

def main(stdscr):
    # stdscr.nodelay(10)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.echo()
    stdout = io.StringIO()

    code = ''
    codePosition=0
    stdscr.addstr(f"ASnake {ASnakeVersion} \nRepl {ReplVersion}\n\n")
    stdscr.addstr(PREFIX, curses.color_pair(1))

    while True:
        c = stdscr.getch()
        codeLength = len(code)
        # notetoself: x and y are cursor position
        y, x = stdscr.getyx()
        height, width = stdscr.getmaxyx()

        if codePosition > codeLength:
            codePosition = codeLength
        elif codePosition < 0:
            codePosition = 0

        if c == curses.KEY_LEFT:
            if not x < 5:
                stdscr.move(y, x - 1)
                if codePosition <= codeLength and x-len(PREFIX) <= codePosition:
                    codePosition -= 1

        elif c == curses.KEY_RIGHT:
            if codePosition < codeLength:
                stdscr.addstr(code[codePosition])
                codePosition += 1
            stdscr.move(y, x + 1)

        # todo -> bash history
        elif c == curses.KEY_UP:
            pass

        elif c in {curses.KEY_BACKSPACE, 127}:
            if not x < 4:
                stdscr.delch(y, x)
                if 0 < codePosition < len(code) - 1:
                    tmpStart=codePosition-1 if codePosition-1 > 0 else 0
                    code = code[:tmpStart] + code[codePosition:]
                else:
                    code = code[:-1]
                codePosition -= 1
                # file_out("a", code)
            else:
                stdscr.move(y, x + 1)

        elif c in {curses.KEY_ENTER, 10, 13}:
            if y >= height - 1:
                stdscr.clear()
                stdscr.refresh()
            else:
                stdscr.move(y + 1, 0)
                with redirect_stdout(stdout):
                    exec(buildCode(code),execGlobal)

                output = stdout.getvalue()
                # file_out("w", output.split("\n"), len(output.split("\n")))
                out_arr = output.splitlines()

                for i in range(len(out_arr)):
                    y, _ = stdscr.getyx()
                    if y >= height - 1:
                        stdscr.clear()
                        stdscr.addstr(f"{out_arr[i]}\n")
                    else:
                        stdscr.addstr(f"{out_arr[i]}\n")
                    # file_out("a", out_arr[i], y)

                stdout = io.StringIO()
                stdscr.addstr(">>> ", curses.color_pair(1))
                # file_out("w", bash_history)
                code = ''
                codePosition = 0
                stdscr.refresh()

        else:
            if codePosition == len(code):
                code += chr(c)
                codePosition += 1
            else:
                if codePosition == 1:
                    code = chr(c) + code[codePosition:]
                else:
                    code = code[:codePosition] + chr(c) + code[codePosition:]
                    codePosition += 1

                for xx in range(x - 1 + len(code[codePosition:]), x - 1, -1):
                    stdscr.delch(y, xx)
                stdscr.addstr(code[codePosition:])
                stdscr.move(y, x)
                stdscr.refresh()

        #file_out('w', code,f"{codePosition}/{len(code)} x={x} y={y}")

    stdscr.refresh()


if __name__ == "__main__":
    curses.wrapper(main)

