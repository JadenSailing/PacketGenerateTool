#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Helper

import os
import time
from .Const import *
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

class LuaPacketStructOutput(object):
    def __init__(self, packetAttribute, packetItem):
        self.packetItem = packetItem
        self.attribute = packetAttribute
        pass

    def generateWrite(self, prefix, attributePrefix, listIndex = 0):
        outStrList = []
        struct = self.packetItem.getStructByName(self.attribute.dataStructName)
        for attribute in struct.attributes:
            commonData = Util.GetCommonDataByType(attribute.dataType)
            if(commonData != None):
                if(commonData["type"] == attribute.dataType):
                    outStrList.append(prefix + "self:%s(self.%s)" % (commonData["write"], attributePrefix + "." + attribute.dataName))
                else:
                    if(is_number(attribute.arraySize)):
                        outStrList.append(prefix + "for %s = 1, %s do" % (Const.Index_List[listIndex], attribute.arraySize))
                        outStrList.append(prefix + Const.Table_Str + "self:%s(self.%s[%s])" % (commonData["write"], attributePrefix + "." + attribute.dataName, Const.Index_List[listIndex]))
                        outStrList.append(prefix + "end")
                    else:
                        outStrList.append(prefix + "for %s = 1, self.%s do" % (Const.Index_List[listIndex], attribute.arraySize))
                        outStrList.append(prefix + Const.Table_Str + "self:%s(self.%s[%s])" % (commonData["write"], attributePrefix + "." + attribute.dataName, Const.Index_List[listIndex]))
                        outStrList.append(prefix + "end")
            elif(attribute.dataType == Const.Packet_Attribute_Type_charArray):
                if(is_number(attribute.arraySize)):
                    outStrList.append(prefix + "self:WriteCharArray(self.%s, %s, true, true)" % (attributePrefix + "." + attribute.dataName, attribute.arraySize))
                else:
                    outStrList.append(prefix + "self:WriteCharArray(self.%s, self.%s, true, true)" % (attributePrefix + "." + attribute.dataName, attribute.arraySize))
            elif(attribute.dataType == Const.Packet_Attribute_Type_struct):
                outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateWrite(prefix, attributePrefix + "." + attribute.dataName, listIndex))
            elif(attribute.dataType == Const.Packet_Attribute_Type_structArray):
                if(is_number(attribute.arraySize)):
                    outStrList.append(prefix + "for %s = 1, %s do" % (Const.Index_List[listIndex], attribute.arraySize))
                    outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateWrite(prefix + Const.Table_Str, attributePrefix + "." + attribute.dataName + "[" + Const.Index_List[listIndex] + "]", listIndex + 1))
                    outStrList.append(prefix + "end")
                else:
                    outStrList.append(prefix + "for %s = 1, self.%s do" % (Const.Index_List[listIndex], attribute.arraySize))
                    outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateWrite(prefix + Const.Table_Str, attributePrefix + "." + attribute.dataName + "[" + Const.Index_List[listIndex] + "]", listIndex + 1))
                    outStrList.append(prefix + "end")

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

    def generateRead(self, prefix, attributePrefix, listIndex = 0):
        outStrList = []
        struct = self.packetItem.getStructByName(self.attribute.dataStructName)
        outStrList.append(prefix + "self.%s = {}" % (attributePrefix))
        for attribute in struct.attributes:
            commonData = Util.GetCommonDataByType(attribute.dataType)
            if(commonData != None):
                if(commonData["type"] == attribute.dataType):
                    outStrList.append(prefix + "self.%s = self.%s()" % (attributePrefix + "." + attribute.dataName, commonData["read"]))
                else:
                    if(is_number(attribute.arraySize)):
                        outStrList.append(prefix + "for %s = 1, %s do" % (Const.Index_List[listIndex], attribute.arraySize))
                        outStrList.append(prefix + Const.Table_Str + "self.%s[%s] = self.%s()" % (attributePrefix + "." + attribute.dataName, Const.Index_List[listIndex], commonData["read"]))
                        outStrList.append(prefix + "end")
                    else:
                        outStrList.append(prefix + "for %s = 1, self.%s do" % (Const.Index_List[listIndex], attribute.arraySize))
                        outStrList.append(prefix + Const.Table_Str + "self.%s[%s] = self.%s()" % (attributePrefix + "." + attribute.dataName, Const.Index_List[listIndex], commonData["read"]))
                        outStrList.append(prefix + "end")
            elif(attribute.dataType == Const.Packet_Attribute_Type_charArray):
                if(is_number(attribute.arraySize)):
                    outStrList.append(prefix + "self.%s = self.ReadString(%s)" % (attributePrefix + "." + attribute.dataName, attribute.arraySize))
                else:
                    outStrList.append(prefix + "self.%s = self.ReadString(self.%s)" % (attributePrefix + "." + attribute.dataName, attribute.arraySize))
            elif(attribute.dataType == Const.Packet_Attribute_Type_struct):
                outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateRead(prefix, attributePrefix + "." + attribute.dataName, listIndex))
            elif(attribute.dataType == Const.Packet_Attribute_Type_structArray):
                if(is_number(attribute.arraySize)):
                    outStrList.append(prefix + "for %s = 1, %s do" % (Const.Index_List[listIndex], attribute.arraySize))
                    outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateRead(prefix + Const.Table_Str, attributePrefix + "." + attribute.dataName + "[" + Const.Index_List[listIndex] + "]", listIndex + 1))
                    outStrList.append(prefix + "end")
                else:
                    outStrList.append(prefix + "for %s = 1, self.%s do" % (Const.Index_List[listIndex], attributePrefix + "." + attribute.arraySize))
                    outStrList.append(LuaPacketStructOutput(attribute, self.packetItem).generateRead(prefix + Const.Table_Str, attributePrefix + "." + attribute.dataName + "[" + Const.Index_List[listIndex] + "]", listIndex + 1))
                    outStrList.append(prefix + "end")

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

class LuaPacketAttributeOutput(object):
    def __init__(self, packetAttribute, packetItem = None):
        self.attribute = packetAttribute
        self.packetItem = packetItem
        pass

    def generateDefault(self):
        outStrList = []
        commonData = Util.GetCommonDataByType(self.attribute.dataType)
        if(commonData != None and commonData["type"] == self.attribute.dataType):
            outStrList.append(Const.Table_Str + "self.%s = %s" % (self.attribute.dataName, self.attribute.dataValue))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_charArray):
            outStrList.append(Const.Table_Str + "self.%s = \"%s\"" % (self.attribute.dataName, self.attribute.dataValue))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_struct):
            outStrList.append(Const.Table_Str + "self.%s = {}" % (self.attribute.dataName))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_structArray):
            outStrList.append(Const.Table_Str + "self.%s = {}" % (self.attribute.dataName))
            pass
        
        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

    #attribute消息写入
    def generateWrite(self, prefix = ""):
        outStrList = []
        if(len(self.attribute.comment) > 0):
            outStrList.append(prefix + "--" + self.attribute.comment)
        commonData = Util.GetCommonDataByType(self.attribute.dataType)
        if(commonData != None):
            if(commonData["type"] == self.attribute.dataType):
                outStrList.append(prefix + "self:%s(self.%s)" % (commonData["write"], self.attribute.dataName))
            else:
                if(is_number(self.attribute.arraySize)):
                    outStrList.append(prefix + "for %s = 1, %s do" % (Const.Index_List[0], self.attribute.arraySize))
                    outStrList.append(prefix + Const.Table_Str + "self:%s(self.%s[%s])" % (commonData["write"], self.attribute.dataName, "i"))
                    outStrList.append(prefix + "end")
                else:
                    outStrList.append(prefix + "for %s = 1, self.%s do" % (Const.Index_List[0], self.attribute.arraySize))
                    outStrList.append(prefix + Const.Table_Str + "self:%s(self.%s[%s])" % (commonData["write"], self.attribute.dataName, "i"))
                    outStrList.append(prefix + "end")
                pass
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_charArray):
            if(is_number(self.attribute.arraySize)):
                outStrList.append(prefix + "self:WriteCharArray(self.%s, %s, true, true)" % (self.attribute.dataName, self.attribute.arraySize))
            else:
                outStrList.append(prefix + "self:WriteCharArray(self.%s, self.%s, true, true)" % (self.attribute.dataName, self.attribute.arraySize))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_struct):
            outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateWrite(prefix, self.attribute.dataName, 0))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_structArray):
            if(is_number(self.attribute.arraySize)):
                outStrList.append(prefix + "for i = 1, %s do" % self.attribute.arraySize)
                outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateWrite(prefix + Const.Table_Str, self.attribute.dataName + "[i]", 1))
                outStrList.append(prefix + "end")
            else:
                outStrList.append(prefix + "for i = 1, self.%s do" % self.attribute.arraySize)
                outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateWrite(prefix + Const.Table_Str, self.attribute.dataName + "[i]", 1))
                outStrList.append(prefix + "end")

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

    #attribute消息读取
    def generateRead(self, prefix = ""):
        outStrList = []
        if(len(self.attribute.comment) > 0):
            outStrList.append(prefix + "--" + self.attribute.comment)

        commonData = Util.GetCommonDataByType(self.attribute.dataType)
        if(commonData != None):
            if(commonData["type"] == self.attribute.dataType):
                outStrList.append(prefix + "self.%s = self:%s()" % (self.attribute.dataName, commonData["read"]))
            else:
                outStrList.append(prefix + "self.%s = {}" % (self.attribute.dataName))
                if(is_number(self.attribute.arraySize)):
                    outStrList.append(prefix + "for i = 1, %s do" % self.attribute.arraySize)
                    outStrList.append(prefix + Const.Table_Str + "self.%s[%s] = self.%s()" % (self.attribute.dataName, "i", commonData["read"]))
                    outStrList.append(prefix + "end")
                else:
                    outStrList.append(prefix + "for i = 1, self.%s do" % self.attribute.arraySize)
                    outStrList.append(prefix + Const.Table_Str + "self.%s[%s] = self.%s()" % (self.attribute.dataName, "i", commonData["read"]))
                    outStrList.append(prefix + "end")
                pass
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_charArray):
            if(is_number(self.attribute.arraySize)):
                outStrList.append(prefix + "self.%s = self:ReadString(%s)" % (self.attribute.dataName, self.attribute.arraySize))
            else:
                outStrList.append(prefix + "self.%s = self:ReadString(self.%s)" % (self.attribute.dataName, self.attribute.arraySize))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_struct):
            outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateRead(prefix, self.attribute.dataName, 0))
        elif(self.attribute.dataType == Const.Packet_Attribute_Type_structArray):
            outStrList.append(prefix + "self.%s = {}" % (self.attribute.dataName))
            if(is_number(self.attribute.arraySize)):
                outStrList.append(prefix + "for i = 1, %s do" % self.attribute.arraySize)
                outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateRead(prefix + Const.Table_Str, self.attribute.dataName + "[i]", 1))
                outStrList.append(prefix + "end")
            else:
                outStrList.append(prefix + "for i = 1, self.%s do" % self.attribute.arraySize)
                outStrList.append(LuaPacketStructOutput(self.attribute, self.packetItem).generateRead(prefix + Const.Table_Str, self.attribute.dataName + "[i]", 1))
                outStrList.append(prefix + "end")

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

class LuaPacketOutput(object):
    def __init__(self, packet):
        self.packet = packet
    
    def generateOutputCG(self):

        outStrList = []
        outStrList.append("local %s = class(\"%s\", LuaRequestPacket)" % (self.packet.name, self.packet.name))
        outStrList.append("")

        outStrList.append("function %s:Init()" % (self.packet.name))

        outStrList.append(Const.Table_Str + "self:SetupGameServerPacket(%s)" % (self.packet.id))

        #属性默认值
        for attribute in self.packet.attributes:
            outStrList.append(LuaPacketAttributeOutput(attribute, self.packet).generateDefault())
        outStrList.append("end\n")

        #写入
        outStrList.append("function %s:WriteStream()" % (self.packet.name))
        for attribute in self.packet.attributes:
            outStrList.append(LuaPacketAttributeOutput(attribute, self.packet).generateWrite(Const.Table_Str))

        outStrList.append("end\n")

        outStrList.append("return " + self.packet.name)

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

    def generateOutputGC(self):
        outStrList = []
        outStrList.append("local %s = class(\"%s\", LuaResponsePacket)" % (self.packet.name, self.packet.name))
        outStrList.append("")
        #读取
        outStrList.append("function %s:ReadStream()" % (self.packet.name))
        for attribute in self.packet.attributes:
            outStrList.append(LuaPacketAttributeOutput(attribute, self.packet).generateRead(Const.Table_Str))
        outStrList.append("end\n")

        #处理
        outStrList.append("function %s:Handler()" % (self.packet.name))
        outStrList.append(Const.Table_Str + "Log.Info(\"%s:Handler...\")" % self.packet.name)
        outStrList.append("end\n")

        outStrList.append("return " + self.packet.name)

        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

    def generateOutput(self):
        outStrList = []

        #packet comment
        outStrList.append(Const.Comment_Lua_Str + self.packet.name)
        outStrList.append(Const.Comment_Lua_Str + "Date " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        outStrList.append(Const.Comment_Lua_Str + "Author " + self.packet.author)
        outStrList.append("")

        for comment in self.packet.titleComment:
            outStrList.append(Const.Comment_Lua_Str + comment)

        if(self.packet.type == Const.PacketType_CG):
            outStrList.append(self.generateOutputCG())
        elif(self.packet.type == Const.PacketType_GC):
            outStrList.append(self.generateOutputGC())
        
        outStr = ""
        for i in range(len(outStrList)):
            outStr = outStr + outStrList[i]
            if(i < len(outStrList) - 1):
                outStr = outStr + Const.New_Line_Str
        return outStr

