#!/usr/bin/env python
# Anthor: Huang jian qiang
# From: SIMIT
# Date: 2016-01-11
# Description: sort the folders by size

import os
import sys
import platform
from progressbar import ProgressBar

#used to find the width of terminal
try:
    from array import array
    from fcntl import ioctl
    import termios
except:
    pass

class FoldAnalyze():
    def __init__(self, root='.'):
        self.OSInfo = platform.system()

        # try to find the width of terminal
        try:
            h, w = array('h', ioctl(sys.stderr, termios.TIOCGWINSZ, '\0' * 8))[:2]
        except:
            w = 80

        self.showWidth = w - 10
        self.dirSizeList = []
        self.dirSizeDict = {}
        self.dirList = []

        # Progress Bar
        count = 0
        self.countDict = {}
        for (dirpath, dirnames, filenames) in os.walk(root):
            count += 1
            self.countDict[dirpath] = count
        self.count2 = 0
        self.pbar = ProgressBar(maxval=count, term_width=self.showWidth).start()

        self.getdirsize(root)
        self.dirSizeList = [(value, key) for key, value in self.dirSizeDict.items()]
        self.pbar.finish()
        self.sortBySize(self.dirSizeList)

    def getdirsize(self, root):
        for (dirpath, dirnames, filenames) in os.walk(root):
            try:
                self.pbar.update(self.countDict[dirpath])
            except:
                pass
            size = 0
            for filename in filenames:
                try:
                    size += os.path.getsize(os.path.join(dirpath, filename))
                except:
                    size += 0

            if [] == dirnames:
                try:
                    # add fold size
                    size += os.path.getsize(dirpath)
                except:
                    size += 0
                self.dirSizeDict[dirpath] = size
                return size
            else:
                for dirname in dirnames:
                    # add file size into the fold
                    dirPath = os.path.join(dirpath, dirname)
                    if dirPath in self.dirSizeDict:
                        size += self.dirSizeDict[dirPath]
                    else:
                        try:
                            size += self.getdirsize(os.path.join(dirpath, dirname))
                        except:
                            size += 0
                size += os.path.getsize(dirpath)
                self.dirSizeDict[dirpath] = size
                return size

    def sortBySize(self, dirSizeList):
        dirSizeList.sort()
        dirSizeList.reverse()
        title = ' Sorted By Size '
        markerLen = (self.showWidth - len(title)) / 2
        print '-'*markerLen + title + '-'*markerLen
        for size, dirpath in dirSizeList:
            print self.formatStringLength(
                width=self.showWidth,
                header=dirpath,
                tailor=self.humanSizeString(size),
                marker='-')

    def humanSizeString(self, size):
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

    def formatStringLength(self, width, header, tailor, marker='-'):
        headerString = header[:]
        tailorString = tailor[:]
        if 'Linux' == self.OSInfo:
            try:
                lenHeader = (len(headerString) + len(headerString.decode('utf-8')))/2
                lenTailor = (len(tailorString) + len(tailorString.decode('utf-8')))/2
            except:
                lenHeader = len(headerString)
                lenTailor = len(tailorString)

        elif 'Windows' == self.OSInfo:
            lenHeader = len(headerString)
            lenTailor = len(tailorString)
        outString = ''

        #print [headerString], lenHeader
        while True:
            if width > (lenHeader + lenTailor + 3):
                marker = marker * (width - lenHeader - lenTailor - 2)
                outString += (headerString + ' %s '%marker + tailorString)
                return outString
            else:
                if lenHeader > width:
                    outString += (headerString[:width] + '\n')
                    headerString = headerString[width:]
                    if 'Linux' == self.OSInfo:
                        try:
                            lenHeader = (len(headerString) + len(headerString.decode('utf-8'))) / 2
                        except:
                            lenHeader = len(headerString)
                    elif 'Windows' == self.OSInfo:
                        lenHeader = len(headerString)
                else:
                    outString += headerString + ' ' + '%s'%marker*(width-lenHeader-1) + '\n'
                    headerString = ''
                    lenHeader = 0

if __name__ == '__main__':
    if len(sys.argv) == 1:
        #a = FoldAnalyze
        FoldAnalyze()
    else:
        FoldAnalyze(sys.argv[1])

