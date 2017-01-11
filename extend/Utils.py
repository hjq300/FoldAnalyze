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

if __name__ == '__main__':
    print dir(StringUtils)
