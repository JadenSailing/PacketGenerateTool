#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Const

class Const(object):
    ParentDir = ""
    PacketPath = "packet"
    OutputPath = "output"

    PacketFileExtention = ".txt"
    LuaFileExtention = ".lua"

    Comment_Lua_Str = "--"

    New_Line_Str = "\n"
    Table_Str = "\t"

    
    Ord_New_Line = 0x0A
    Ord_Space = 0x20
    Ord_Table = 0x09

    PacketType_CG = 0
    PacketType_GC = 1
 
    #数据类型
    Packet_Attribute_Type_invalid = -1      #无效
    Packet_Attribute_Type_int = 0           #
    Packet_Attribute_Type_charArray = 1     #string
    Packet_Attribute_Type_int64 = 2         #
    Packet_Attribute_Type_intArray = 3      #
    Packet_Attribute_Type_struct = 4        #自定义结构
    Packet_Attribute_Type_structArray = 5   #自定义结构数组
    Packet_Attribute_Type_uint = 6          #
    Packet_Attribute_Type_uintArray = 7     #
    Packet_Attribute_Type_uint64 = 8        #
    Packet_Attribute_Type_uint64Array = 9   #
    Packet_Attribute_Type_short = 10        #
    Packet_Attribute_Type_shortArray = 11   #
    Packet_Attribute_Type_ushort = 12       #
    Packet_Attribute_Type_ushortArray = 13  #
    Packet_Attribute_Type_float = 14        #
    Packet_Attribute_Type_floatArray = 15   #
    Packet_Attribute_Type_double = 16       #
    Packet_Attribute_Type_doubleArray = 17  #
    Packet_Attribute_Type_double = 18       #
    Packet_Attribute_Type_doubleArray = 19  #
    Packet_Attribute_Type_bool = 20         #bool 非0=true
    Packet_Attribute_Type_boolArray = 21    #
    Packet_Attribute_Type_byte = 22         #
    Packet_Attribute_Type_byteArray = 23    #
    Packet_Attribute_Type_int64Array = 24   #
    

    
    Word_Type_Comment = 1
    Word_Type_String = 2
    Word_Type_Name = 3
    Word_Type_SYMBOL = 4

    Index_List = ["i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

class Util(object):
    commonDataType = [
        {"symbol" : "int",      "type" : Const.Packet_Attribute_Type_int, "aType" : Const.Packet_Attribute_Type_intArray, "read" : "ReadInt32", "write" : "WriteInt32", "dvalue" : 0},
        {"symbol" : "uint",     "type" : Const.Packet_Attribute_Type_uint, "aType" : Const.Packet_Attribute_Type_uintArray, "read" : "ReadUInt32", "write" : "WriteUInt32", "dvalue" : 0},
        {"symbol" : "short",    "type" : Const.Packet_Attribute_Type_short, "aType" : Const.Packet_Attribute_Type_shortArray, "read" : "ReadInt16", "write" : "WriteInt16", "dvalue" : 0},
        {"symbol" : "ushort",   "type" : Const.Packet_Attribute_Type_ushort, "aType" : Const.Packet_Attribute_Type_ushortArray, "read" : "ReadUInt16", "write" : "WriteInt16", "dvalue" : 0},
        {"symbol" : "int64",    "type" : Const.Packet_Attribute_Type_int64, "aType" : Const.Packet_Attribute_Type_int64Array, "read" : "ReadInt64", "write" : "WriteInt64", "dvalue" : 0},
        {"symbol" : "uint64",   "type" : Const.Packet_Attribute_Type_uint64, "aType" : Const.Packet_Attribute_Type_uint64Array, "read" : "ReadUInt64", "write" : "WriteUInt64", "dvalue" : 0},
        {"symbol" : "byte",     "type" : Const.Packet_Attribute_Type_byte, "aType" : Const.Packet_Attribute_Type_byteArray, "read" : "ReadByte", "write" : "WriteByte", "dvalue" : 0},
        {"symbol" : "float",    "type" : Const.Packet_Attribute_Type_float, "aType" : Const.Packet_Attribute_Type_floatArray, "read" : "ReadSingle", "write" : "WriteSingle", "dvalue" : 0},
        {"symbol" : "double",   "type" : Const.Packet_Attribute_Type_double, "aType" : Const.Packet_Attribute_Type_doubleArray, "read" : "ReadDouble", "write" : "WriteDouble", "dvalue" : 0},
        {"symbol" : "bool",     "type" : Const.Packet_Attribute_Type_bool, "aType" : Const.Packet_Attribute_Type_boolArray, "read" : "ReadBool", "write" : "WriteBool", "dvalue" : 0},
    ]

    def GetCommonDataBySymbol(symbol):
        for i in range(len(Util.commonDataType)):
            dict = Util.commonDataType[i]
            if(dict["symbol"] == symbol[0:len(dict["symbol"])]):
                return dict
        return None
    def GetCommonDataByType(type):
        for i in range(len(Util.commonDataType)):
            dict = Util.commonDataType[i]
            if(dict["type"] == type or dict["aType"] == type):
                return dict
        return None