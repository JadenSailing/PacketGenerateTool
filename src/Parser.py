#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File

import os
import time
from io import StringIO
from Const import *
from Lexer import *

'''
//测试发送消息
cg message CGTest
{
	id = 2001
	dir = Test
	
	struct item
	{
		id
		name
	}
	
	int index = 100 
	int[10] indexArray
	
	char[30] name = "hello" //名字 30定长	
	int nameLen = 10
	char[nameLen] itemName //不定长字符串	
	
	item item1 //item结构
	int itemLen = 10
	item[itemLen] itemList //不定长item数组
}
'''

#需要序列化的属性
class JPacketAttribute(object):
	def __init__(self):
		self.dataName = ""
		self.dataType = 0
		self.dataValue = 0
		self.dataStructName = ""
		self.comment = ""
		self.arraySize = 0
		pass
#自定义结构体
class JPacketStruct(object):
	def __init__(self):
		self.titleComment = []
		self.name = ""
		self.attributes = []
		pass

#一条完整消息
class JPacketItem(object):
	def __init__(self):
		self.titleComment = []
		self.name = ""
		self.author = ""
		self.type = 0
		self.id = 0
		self.dir = ""

		self.structs = [] #自定义结构列表

		self.attributes = []
	def getStructByName(self, name):
		for struct in self.structs:
			if(struct.name == name):
				return struct
		return None

#整个消息配置，多条消息
class JPacket(object):
	def __init__(self, fileName, packetstr):
		self.packetstr = packetstr
		self.fileName = fileName
		self.packetList = []
		self.lexer = Lexer(self.fileName, self.packetstr)
		self.lexer.parse()
		self.wordIndex = -1
		
	#处理入口
	def parse(self):
		while(not self.isEnd()):
			self.currentItem = JPacketItem()
			#注释
			self.parseTitleComment()
			#消息类型
			self.parsePacketTitle()
			
			self.parseLeftBrace()
			#消息参数 id等
			self.parsePacketDefine()
			#消息内自定义结构体列表
			self.parsePacketStuct()
			#消息的属性列表，每一条会序列化
			self.currentItem.attributes = self.parsePacketAttributes()
			
			self.parseRightBrace()
			
			self.packetList.append(self.currentItem)

	def isEnd(self):
		if(self.wordIndex == len(self.lexer.wordList) - 1):
			return True
		return False
	
	def raiseError(self, errorStr):
		word = self.lexer.wordList[self.wordIndex]
		raise ValueError(errorStr + "[line]: " + str(word.line) + ", offset = " + str(word.lineoffset) + ",[file]: " + self.fileName)
	
	def nextword(self):
		self.wordIndex = self.wordIndex + 1
		return self.lexer.wordList[self.wordIndex]

	def backword(self):
		self.wordIndex = self.wordIndex - 1
		
	def parseTitleComment(self):
		word = self.nextword()
		while(word.type == Const.Word_Type_Comment):
			self.currentItem.titleComment.append(word.content)
			word = self.nextword()
		self.backword()
	
	def parsePacketTitle(self):
		typeWord = self.nextword()
		if(typeWord.content == "cg"):
			self.currentItem.type = Const.PacketType_CG
		elif(typeWord.content == "gc"):
			self.currentItem.type = Const.PacketType_GC
		else:
			self.raiseError("require \"cg\" or \"gc\", get \"%s\"" % typeWord.content)
		
		msgWord = self.nextword()
		if(msgWord.content != "message"):
			self.raiseError("require \"message\", get \"%s\"" + msgWord.content)
			return
		
		self.currentItem.name = self.nextword().content
		
		
	def parseLeftBrace(self):
		word = self.nextword()
		if(word.content != "{"):
			self.raiseError("missing { at the message start")
			
	def parseRightBrace(self):
		word = self.nextword()
		if(word.content != "}"):
			
			self.raiseError("missing } at the message end, get " + word.content)
	
	def readString(self):
		ch = self.nextch()
		if(ch != "\""):
			self.raiseError("read string error, require \", get " + ch)
		ret = ""
		ch = self.nextch()
		while(ch != "\"" and ord(ch) != Const.Ord_New_Line):
			ret = ret + ch
			ch = self.nextch()
			
		if(ch != "\""):
			self.raiseError("read string error, require \", get " + ch)
		
		
		ch = self.nextch()
		
		self.backch()
		return ret
	
	def readComment(self):
		ch = self.nextch()
		if(ch != "/"):
			self.raiseError("read comment error, require /, get " + ch)
		ch = self.nextch()
		if(ch != "/"):
			self.raiseError("read comment error, require //, get " + ch)
		ret = ""
		ch = self.nextch()
		while(ch != "" and ord(ch) != Const.Ord_New_Line):
			ret = ret + ch
			ch = self.nextch()
		return ret
	
	def parsePacketDefine(self):
		tword = self.nextword()
		while(True):
			if(tword.type != Const.Word_Type_Comment):
				if(tword.content == "id"):
						nextword = self.nextword()
						if(nextword.content == "="):
							self.currentItem.id = self.nextword().content
						else:
							self.raiseError("message id format error, require id value, get \"%s\"" % nextword.content)
				elif(tword.content == "dir"):
					nextword = self.nextword()
					if(nextword.content == "="):
						self.currentItem.dir = self.nextword().content
					else:
						self.raiseError("message dir format error, require dir value, get \"%s\"" % nextword.content)
				elif(tword.content == "author"):
					nextword = self.nextword()
					if(nextword.content == "="):
						self.currentItem.author = self.nextword().content
					else:
						self.raiseError("message dir format error, require dir value, get \"%s\"" % nextword.content)
				else:
					self.backword()
					break
			tword = self.nextword()

	def parsePacketStuct(self):
		tword = self.nextword()
		if(tword.content != "struct"):
			self.backword()
			return
		while(tword.content == "struct"):
			struct = JPacketStruct()
			struct.name = self.nextword().content
			word = self.nextword()
			if(word.type == Const.Word_Type_Comment):
				struct.titleComment = word.content
				word = self.nextword()
			if(word.content != "{"):
				self.raiseError("struct require \"{\", get \"%s\"" % word)
			#struct的属性列表
			struct.attributes = self.parsePacketAttributes()
			self.currentItem.structs.append(struct)
			tword = self.nextword()

			#skip }
			if(tword.content == "}"):
				tword = self.nextword()
		self.backword()
			
	#获取消息或结构的属性信息，嵌套下会出现递归调用
	def parsePacketAttributes(self):
		tword = self.nextword()
		attributeList = []
		while(not self.isEnd()):
			attribute = JPacketAttribute()
			attribute.dataType = Const.Packet_Attribute_Type_invalid
			if(tword.type != Const.Word_Type_Comment):
				commonData = Util.GetCommonDataBySymbol(tword.content)
				if(commonData != None):
					nextword = self.nextword()
					if(nextword.content == "["):
						attribute.dataType = commonData["aType"]
						attribute.arraySize = self.nextword().content
						nextword = self.nextword()
						if(nextword.content != "]"):
							self.raiseError("syntax error, require \"]\", find " + nextword.content)
						attribute.dataName = self.nextword().content
						nextword = self.nextword()
						if(nextword.content == "="):
							attribute.dataValue = self.nextword().content
						else:
							self.backword()
					else:
						attribute.dataType = commonData["type"]
						attribute.dataName = nextword.content
						nextword = self.nextword()
						if(nextword.content == "="):
							attribute.dataValue = self.nextword().content
						else:
							self.backword()

				elif(tword.content == "char"):
					attribute.dataType = Const.Packet_Attribute_Type_charArray
					nextword = self.nextword()
					if(nextword.content == "["):
						attribute.dataType = Const.Packet_Attribute_Type_charArray
						attribute.arraySize = self.nextword().content
						nextword = self.nextword()
						if(nextword.content != "]"):
							self.raiseError("char[] syntax error, require \"]\", find " + nextword.content)
						attribute.dataName = self.nextword().content
						nextword = self.nextword()
						if(nextword.content == "="):
							attribute.dataValue = self.nextword().content
						else:
							self.backword()
				elif(tword.content == "}"):
					break
				else:
					#此处可能是自定义结构
					struct = self.currentItem.getStructByName(tword.content)
					if(struct != None):
						#继续判断是否是自定义结构的数组
						nextword = self.nextword()
						if(nextword.content == "["):
							attribute.dataType = Const.Packet_Attribute_Type_structArray
							attribute.dataStructName = tword.content
							attribute.arraySize = self.nextword().content
							nextword = self.nextword()
							if(nextword.content != "]"):
								self.raiseError("char[] syntax error, require \"]\", find " + nextword.content)
							attribute.dataName = self.nextword().content
							nextword = self.nextword()
							if(nextword.content == "="):
								attribute.dataValue = self.nextword().content
							else:
								self.backword()
						else:
							attribute.dataType = Const.Packet_Attribute_Type_struct
							attribute.dataName = nextword.content
							attribute.dataStructName = tword.content
							nextword = self.nextword()
							if(nextword.content == "="):
								attribute.dataValue = self.nextword().content
							else:
								self.backword()
					else:
						self.raiseError("message format error, require dataType or \"}\", get \"" + tword.content + "\"")

			else:
				if(tword.type == Const.Word_Type_Comment):
					currItemAttrLen = len(attributeList)
					if(currItemAttrLen > 0):
						attributeList[currItemAttrLen - 1].comment = tword.content

			if(attribute.dataType != Const.Packet_Attribute_Type_invalid):
				attributeList.append(attribute)
			tword = self.nextword()
		
		self.backword()
		return attributeList
		