#!/usr/bin/env python
# Anthor: Huang jian qiang
# From: SIMIT
# Date: 2016-01-11
# Description: sort the folders by size

import os
import sys
import platform
from progressbar import ProgressBar

from extend.Utils import StringUtils

#used to find the width of terminal
try:
    from array import array
    from fcntl import ioctl
    import termios
except:
    pass

class FoldSizeAnalyze():
    '''
        List the folders in size order
    '''
    def __init__(self, root):

        if root == None:
            print 'help'
        else:

            self.OSInfo = platform.system() # Used to identify the Linux or Windows
                                            # platform, which differ in codec in
                                            # folder name

            # try to find the width of terminal
            try:
                h, w = array('h', ioctl(sys.stderr, termios.TIOCGWINSZ, '\0' * 8))[:2]
            except:
                w = 80

            self.showWidth = w - 10 # Setup the width of list
            self.dirSizeList = []   # Store directories size info in list type
            self.dirSizeDict = {}   # Store directories size info in dict type

            # Progress Bar
            count = 0
            self.countDict = {}
            for (dirpath, dirnames, filenames) in os.walk(root):
                count += 1
                self.countDict[dirpath] = count
            self.pbar = ProgressBar(maxval=count, term_width=self.showWidth).start()

            self.getdirsize(root)
            self.dirSizeList = [(value, key) for key, value in self.dirSizeDict.items()]
            self.pbar.finish()
            self.sortBySize(self.dirSizeList)

    def getdirsize(self, root):
        '''
            calculate the size of folders one by one
            including the size of folder and size of files inside the folder

            input: str (path)
            return: int (size)
        '''
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
                        # some folders appear permmision problem
                        try:
                            dirpathname = os.path.join(dirpath, dirname)
                            if os.path.islink(dirpathname):
                                # assume size of link file is zero
                                size += 0 # os.path.getsize(dirpathname)
                            else:
                                size += self.getdirsize(os.path.join(dirpath, dirname))
                        except:
                            size += 0
                size += os.path.getsize(dirpath)
                self.dirSizeDict[dirpath] = size
                return size

    def sortBySize(self, dirSizeList):
        '''
            dirSizeList should be in format:
                [
                (2,   'folder1'),
                (102, 'folder2'),
                (212, 'folder3'),
                ...
                ]
            input: list
            return: NULL
        '''
        dirSizeList.sort()
        dirSizeList.reverse()

        # Generate title
        title = ' Sorted By Size '
        markerLen = (self.showWidth - len(title)) / 2
        print '-'*markerLen + title + '-'*markerLen

        # print out the sorted result
        for size, dirpath in dirSizeList:
            print self.formatStringLength(
                width=self.showWidth,
                header=dirpath,
                tailor=StringUtils().humanSizeString(size),
                marker='-')

    def formatStringLength(self, width, header, tailor, marker='-'):
        '''
            unify each line in the output list in the same width
            input:
                width  -> int (the output list width, pre-defined)
                header -> str (folder path)
                tailor -> str (folder size string info)
                marker -> str (divider marker, can be customed)
            return: str

        '''
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

class FoldStructureAnalyze():
    '''
        list the fold structure like tree
    '''

    def __init__(self):
        self.SPACE = " "*2
        self.SPLIT_PATTEN = '|_'
        pass

    def showDirTree(self, root='.', isDetail=True):
        tmpPath = ""
        for (dirpath, dirnames, filenames) in os.walk(root):
            if not tmpPath == dirpath:
                dirPeace = dirpath.split(os.path.sep)
                space = (self.SPACE + ' '*len(self.SPLIT_PATTEN)) * (len(dirPeace) - 1)
                print space + self.SPLIT_PATTEN + os.path.basename(dirpath)
            else:
                tmpPath = dirpath
            if isDetail:
                for filename in filenames:
                    space = (self.SPACE + ' '*len(self.SPLIT_PATTEN)) * len(dirPeace)
                    print space + self.SPLIT_PATTEN + filename

if __name__ == '__main__':

    if len(sys.argv) == 1:
        root = '.'
        FoldSizeAnalyze(root)
    else:
        root = sys.argv[1]
        FoldSizeAnalyze(root)

