#!/usr/bin/python

import curses


if __name__ == '__main__':
    mainwindow = curses.initscr()
    mainwindow.clear()
    curses.textpad.rectangle(mainwindow, 20, 20, 25, 25)
    curses.endwin()
    
