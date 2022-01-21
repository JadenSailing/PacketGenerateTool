#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Helper

import os
import time
from .Const import *

class LuaPacketDefineItemStructOutput(object):
    def __init__(self, packetDefineItem):
        self.packetDefineItem = packetDefineItem
        pass

    def generateOutput(self):
        outStrList = []
        outStrList.append(
            "\t[%s]\t=\t\"Packet/AutoGenerate/%s\","
             % (self.packetDefineItem.id, self.packetDefineItem.name)
            )
        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

class LuaPacketDefineOutput(object):
    def __init__(self, packetDefine):
        self.packetDefine = packetDefine

    def generateOutput(self):
        outStrList = []

        #packet comment
        outStrList.append(Const.Comment_Lua_Str + Const.Cfg.get("Global", "Comment"))
        outStrList.append("")

        outStrList.append("local autoList = {")
        #每一项
        #[3119]		=	"Packet/AutoGenerate/GCChongLou",
        defineDict = Const.PacketDefine.getDefineDict()
        for item in defineDict.values():
            outputItem = LuaPacketDefineItemStructOutput(item)
            outStrList.append(outputItem.generateOutput())
        outStrList.append("}")
        outStrList.append("return autoList")
        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

