#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# lexer

import os
import time
from io import StringIO
from .Const import *

'''
//重楼装备操作
CGChongLou = 3108
//重楼返回
GCChongLou = 3119
'''

class Word(object):
    def __init__(self, type, content, line, lineoffset):
        self.type = type
        self.content = content
        self.line = line
        self.lineoffset = lineoffset

class Lexer(object):
    def __init__(self, intput):
        self.intput = intput
        self.io = StringIO(intput)
        self.ioLen = len(self.intput)
        self.wordList = []
        self.line = 1
        self.lineoffset = 0
        self.wordIndex = 0
        self.lastCh = ""

    def parse(self):
        while(not self.isEnd()):
            ch = self.nextch()
            if(self.isEmptyCh(ch)):
                continue
            if(ch == "/"):
                ch = self.nextch()
                if(ch == "/"):
                    #comment
                    self.wordList.append(Word(Const.Word_Type_Comment, self.read2LineEnd(), self.line, self.lineoffset))
                else:
                    self.raiseError("require \"/\", get \"%s\"" % ch)
            elif(ch == "="):
                self.wordList.append(Word(Const.Word_Type_SYMBOL, "=", self.line, self.lineoffset))
            else:
                self.backch()
                commonWord = self.readWord()
                self.wordList.append(Word(Const.Word_Type_SYMBOL, commonWord, self.line, self.lineoffset))

    def raiseError(self, errorStr):
        raise ValueError(errorStr + "[line]: " + str(self.line) + ", offset = " + str(self.lineoffset) + ",[file]: " + self.fileName)

    def isEnd(self):
        if(self.io.tell() >= self.ioLen):
            return True
        return False

    def isEmptyCh(self, ch):
        if(ord(ch) == Const.Ord_Space or ord(ch) == Const.Ord_Table or (ord(ch) == Const.Ord_New_Line)):
            return True
        return False
    
    def isNewLine(self, ch):
        if(ord(ch) == Const.Ord_New_Line):
            return True
        return False

    def nextch(self):
        if(self.isEnd()):
            return ""
        ch = self.io.read(1)
        self.lastCh = ch
        if(self.isNewLine(ch)):
            self.line = self.line + 1
            self.lineoffset = 0
        else:
            self.lineoffset = self.lineoffset + 1
        return ch

    def backch(self):
        self.io.seek(self.io.tell() - 1)
        if(self.isNewLine(self.lastCh)):
            self.line = self.line - 1
        else:
            self.lineoffset = self.lineoffset - 1

    #check if valid [a-zA-Z0-9_]+
    def isWordCh(self, ch):
        chOrd = ord(ch)
        if(chOrd >= ord("0") and chOrd <= ord("9")):
            return True
        if(chOrd >= ord("A") and chOrd <= ord("Z")):
            return True
        if(chOrd >= ord("a") and chOrd <= ord("z")):
            return True
        if(chOrd == ord("_")):
            return True
        if(chOrd == ord(".")):
            return True
        return False

    def readWord(self):
        strWord = ""
        while(not self.isEnd()):
            ch = self.nextch()
            if(self.isEmptyCh(ch)):
                break
            if(not self.isWordCh(ch)):
                self.backch()
                break
            strWord = strWord + ch
        return strWord
    
    def readString(self):
        strWord = ""
        while(not self.isEnd()):
            ch = self.nextch()
            if(self.isNewLine(ch)):
                self.raiseError("require \", get \"%s\"" % (ch))
                break
            if(ch == "\""):
                break
            strWord = strWord + ch
        return strWord

    def read2LineEnd(self):
        line = ""
        while(not self.isEnd()):
            ch = self.nextch()
            if(self.isNewLine(ch)):
                self.backch()
                break
            line = line + ch
        return line
        

