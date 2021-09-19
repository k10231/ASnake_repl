import time
import curses
from ASnake import build, execPy
import subprocess

# import os

def runCode(code):
    asn = build(code, comment=False, optimize=False, debug=False, compileTo="Pyston", pythonVersion=3.9, enforceTyping=True)
    return execPy(asn, fancy=False, pep=False, run=True, execTime=False, headless=False)
    # return subprocess.run(["python3", "-c", asn], capture_output=True, text=True)

def main(stdscr):

    stdscr.nodelay(1)
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)
    curses.echo()
    
    code = ''
    stdscr.addstr(">>> ", curses.color_pair(1))

    while True:

        c = stdscr.getch()
        y, x = stdscr.getyx()

        code += 's'
        # stdscr.addstr(y+1, x, code)

        if c == curses.KEY_LEFT:
            if not x < 5:
                stdscr.move(y, x-1) 
            
        if c == curses.KEY_RIGHT:
            stdscr.move(y, x+1)

        if c == curses.KEY_BACKSPACE:
            if not x < 4:
                stdscr.delch(y, x)
                code = code[0:-2]
                with open("streams.txt",'w',encoding = 'utf-8') as f:
                    f.write(f"{code}\n")
            else: 
                stdscr.move(y, x+1)

        if c == curses.KEY_ENTER or c in [10, 13]:
            if c <= y:
                stdscr.clear()
                stdscr.refresh()
            else:
                stdscr.move(y+1,x)
                stdscr.addstr(runCode(code))
                stdscr.addstr(">>> ", curses.color_pair(1))
                code = ''

        
    stdscr.refresh()


curses.wrapper(main)