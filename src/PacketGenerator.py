#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PacketGenerator

import os
from .PacketParser import *
from .Const import *
from .LuaPacketoutput import *
from .PacketDefineParser import *
from .LuaAutoIDListoutput import *

def exportPacketList():
	cfg = Const.Cfg
	outputDir = cfg.get("Global", "OutPutDir")
	packetDirPath = os.path.join(Const.ParentDir, Const.PacketPath)
	if(not os.path.exists(packetDirPath)):
		print("packet config dir not exist!")
		return
	files = os.listdir(packetDirPath)
	validFiles = []
	for filePath in files:
		if(filePath.endswith(Const.PacketFileExtention)):
			validFiles.append(os.path.join(packetDirPath, filePath))
	fileList = []
	
	print("start generating ...")
	#处理PacketDefine
	Const.PacketDefine = PacketDefine()
	content = ""
	filePath = os.path.join(Const.ParentDir, Const.PacketPath, Const.PacketDefinePath)
	with open(filePath, "r", encoding="utf-8") as file:
		content = file.read()
	Const.PacketDefine.Parse(content)
	output = LuaPacketDefineOutput(Const.PacketDefine).generateOutput()
	with open(os.path.join(outputDir, "PacketIDAutoList" + Const.LuaFileExtention), "w", encoding = "utf-8") as file:
		file.write(output)
	#print("cg chonglou id = " + Const.PacketDefine.getPacketID("CGChongLou"))

	outputDir = os.path.join(outputDir, "AutoGenerate")
	fNum = 0
	pNum = 0
	for filePath in validFiles:
		if(Const.PacketDefinePath in filePath):
			continue
		fNum = fNum + 1
		slashIndex = filePath.rfind("\\")
		fileName = filePath[slashIndex + 1 :]
		commentName = fileName[:-4]
		content = ""
		with open(filePath, "r", encoding = "utf-8") as file:
			content = file.read()
		jpacket = JPacket(commentName, content)
		print(fileName)
		jpacket.parse()
		pList = jpacket.packetList

		for item in pList:
			pNum = pNum + 1
			pLua = LuaPacketOutput(item)
			outputLua = pLua.generateOutput()
			print("\tmessage " + item.name)
			outDirLua = ""
			if(len(item.dir) > 0):
				outDirLua = os.path.join(outputDir, item.dir)
				#需要逐层添加路径
				Util.CreateDirRecursive(outDirLua)
			else:
				outDirLua = os.path.join(outputDir)

			if(not os.path.exists(outDirLua)):
				os.mkdir(outDirLua)
			with open(os.path.join(outDirLua, item.name + Const.LuaFileExtention), "w", encoding = "utf-8") as file:
				file.write(outputLua)

	print("complete! file num = %s, message num = %s" % (fNum, pNum))
