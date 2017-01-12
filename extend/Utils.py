#!/usr/bin/env python
# Anthor: Huang jianqiang
# From: Shenzhen
# Date: 2017-01-12
# Description: utils for string

class StringUtils():

    def __init__(self):
        pass

    def humanSizeString(self, size):
        '''
            convert size from 'Bytes' to readable name as 'KB', 'MB', etc.
            input: int (size)
            return: str
        '''
        if size < 1024:
            return '%d Bytes'%size
        elif (1024 <= size) and (size < 1048576):
            return '%d KB'%(size / 1024)
        elif (1048576 <= size) and (size < 1073741824):
            return '%d MB'%(size / 1048576)
        elif (1073741824 <= size) and (size < 1099511627776):
            return '%d GB'%(size / 1073741824)
        else:
            return '%d TB'%(size / 1099511627776)

    def colorfulString(self, showType = 0, frontColor = 40, backgroundColor = 30, string = ""):
        return '\033[%d;%d;%dm'%(showType, frontColor, backgroundColor) + string + '\033[0m'

class ColorUtils():

    def __init__(self):
        import ctypes,sys
        STD_INPUT_HANDLE = -10
        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12

        # Windows CMD text colors definition
        FOREGROUND_BLACK = 0x00 # black.
        FOREGROUND_DARKBLUE = 0x01 # dark blue.
        FOREGROUND_DARKGREEN = 0x02 # dark green.
        FOREGROUND_DARKSKYBLUE = 0x03 # dark skyblue.
        FOREGROUND_DARKRED = 0x04 # dark red.
        FOREGROUND_DARKPINK = 0x05 # dark pink.
        FOREGROUND_DARKYELLOW = 0x06 # dark yellow.
        FOREGROUND_DARKWHITE = 0x07 # dark white.
        FOREGROUND_DARKGRAY = 0x08 # dark gray.
        FOREGROUND_BLUE = 0x09 # blue.
        FOREGROUND_GREEN = 0x0a # green.
        FOREGROUND_SKYBLUE = 0x0b # skyblue.
        FOREGROUND_RED = 0x0c # red.
        FOREGROUND_PINK = 0x0d # pink.
        FOREGROUND_YELLOW = 0x0e # yellow.
        FOREGROUND_WHITE = 0x0f # white.

        BACKGROUND_BLUE = 0x10 # dark blue.
        BACKGROUND_GREEN = 0x20 # dark green.
        BACKGROUND_DARKSKYBLUE = 0x30 # dark skyblue.
        BACKGROUND_DARKRED = 0x40 # dark red.
        BACKGROUND_DARKPINK = 0x50 # dark pink.
        BACKGROUND_DARKYELLOW = 0x60 # dark yellow.
        BACKGROUND_DARKWHITE = 0x70 # dark white.
        BACKGROUND_DARKGRAY = 0x80 # dark gray.
        BACKGROUND_BLUE = 0x90 # blue.
        BACKGROUND_GREEN = 0xa0 # green.
        BACKGROUND_SKYBLUE = 0xb0 # skyblue.
        BACKGROUND_RED = 0xc0 # red.
        BACKGROUND_PINK = 0xd0 # pink.
        BACKGROUND_YELLOW = 0xe0 # yellow.
        BACKGROUND_WHITE = 0xf0 # white.

        # get handle
        std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    def set_cmd_text_color(color, handle):
        Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
        return Bool

    def resetColor():
        '''
            reset white
        '''
        set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)

    #dark blue
    def printDarkBlue(mess):
        set_cmd_text_color(FOREGROUND_DARKBLUE)
        sys.stdout.write(mess)
        resetColor()

if __name__ == '__main__':
    c = ColorUtils().printDarkBlue('hello world')

