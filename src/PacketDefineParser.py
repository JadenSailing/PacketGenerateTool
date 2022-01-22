#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from .PacketDefineLexer import *
from .Const import *

class PacketDefineItem(object):
    def __init__(self, name, id, isValid = True):
        self.name = name
        self.id = id
        self.isValid = isValid
    pass

class PacketDefine(object):

    def __init__(self) -> None:
        super().__init__()
        self.defineDict = {}

    def Parse(self, content):
        self.lexer = Lexer(content)
        self.lexer.parse()
        self.wordIndex = 0
        #leftbrace
        while(not self.isEnd()):
            w = self.nextword()
            if(w.type != Const.Word_Type_SYMBOL):
                continue
            if(w.content != "{"):
                self.raiseError("require \"{\", get \"%s\"" % w.content)
            self.ParseLine()
            w = self.nextword()
            if(w.content != "}"):
                self.raiseError("require \"}\", get \"%s\"" % w.content)
        while(not self.isEnd()):
            w = self.lexer.wordList[self.wordIndex]
            self.wordIndex = self.wordIndex + 1
            if(w.type != Const.Word_Type_SYMBOL):
                continue
            w2 = self.lexer.wordList[self.wordIndex]
            self.wordIndex = self.wordIndex + 1
            if(w2.type != Const.Word_Type_SYMBOL):
                self.raiseError("require \"=\", get \"%s\"" % w2.content)
            w3 = self.lexer.wordList[self.wordIndex]
            self.wordIndex = self.wordIndex + 1
            if(w3.type != Const.Word_Type_SYMBOL):
                self.raiseError("require packet id, get \"%s\"" % w3.content)
            if(self.existSameID(w3.content)):
                self.raiseError("same packet id %s" % w3.content)
            self.defineDict[w.content] = w3.content

    def ParseLine(self):
        w1 = self.nextword()
        if(w1.type != Const.Word_Type_SYMBOL):
            self.raiseError("require packet name, get \"%s\"" % w2.content)
        w2 = self.nextword()
        if(w2.type != Const.Word_Type_SYMBOL):
            self.raiseError("require \"=\", get \"%s\"" % w2.content)
        if(w2.content != "="):
            self.raiseError("require \"=\", get \"%s\"" % w2.content)
        w3 = self.nextword()
        if(w3.type != Const.Word_Type_SYMBOL):
            self.raiseError("require packet id, get \"%s\"" % w3.content)
        if(self.existSameID(w3.content)):
            #可能有重复
            #self.raiseError("same packet id %s" % w3.content)
            pass
        self.defineDict[w1.content] = PacketDefineItem(w1.content, w3.content)
        #分隔符
        w4 = self.nextword()
        if(w4.content == "}"):
            self.backword()
            return
        
        w5 = self.nextword()
        w6 = self.nextword()
        if(w4.content == "valid"):
            self.defineDict[w1.content].isValid = w6.content == "1"

    def existSameID(self, target):
        for item in self.defineDict.values():
            if(item.id == target):
                return True
        return False

    def getPacketID(self, packetName):
        if(packetName in self.defineDict):
            return self.defineDict[packetName].id
        return 0

    def getDefineDict(self):
        return self.defineDict

    def isPacketValid(self, packetName):
        if(not (packetName in self.defineDict)):
            return False
        return self.defineDict[packetName].isValid
    
    def raiseError(self, errorStr):
        if(self.wordIndex >= len(self.lexer.wordList)):
            self.wordIndex = len(self.lexer.wordList) - 1
        word = self.lexer.wordList[self.wordIndex]
        raise ValueError(errorStr + "[line]: " + str(word.line) + ", offset = " + str(word.lineoffset))

    def isEnd(self):
        if(self.wordIndex == len(self.lexer.wordList) - 1):
            return True
        return False
    def nextword(self):
        self.wordIndex = self.wordIndex + 1
        return self.lexer.wordList[self.wordIndex]
    def backword(self):
        self.wordIndex = self.wordIndex - 1