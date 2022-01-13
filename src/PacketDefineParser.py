#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
from .PacketDefineLexer import *
from .Const import *

class PacketDefine(object):

    def __init__(self) -> None:
        super().__init__()
        self.defineDict = {"Invalid" : -1}

    def Parse(self, content):
        self.lexer = Lexer(content)
        self.lexer.parse()

        self.wordIndex = 0
        wordLen = len(self.lexer.wordList)
        while(self.wordIndex < wordLen - 2):
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
            self.defineDict[w.content] = w3.content

            
    def getPacketID(self, packetName):
        if(packetName in self.defineDict):
            return self.defineDict[packetName]
        return 0

    
    def raiseError(self, errorStr):
        if(self.wordIndex >= len(self.lexer.wordList)):
            self.wordIndex = len(self.lexer.wordList) - 1
        word = self.lexer.wordList[self.wordIndex]
        raise ValueError(errorStr + "[line]: " + str(word.line) + ", offset = " + str(word.lineoffset))

    pass