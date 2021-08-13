#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PacketGenerator

import os
from .Parser import *
from .Const import *
from .LuaPacketoutput import *

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
	pNum = 0
	for filePath in validFiles:
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
			output = pLua.generateOutput()
			print("\tmessage " + item.name)
			outDir = ""
			if(len(item.dir) > 0):
				outDir = os.path.join(outputDir, item.dir)
				#需要逐层添加路径
				Util.CreateDirRecusive(outDir)
			else:
				outDir = os.path.join(outputDir)

			if(not os.path.exists(outDir)):
				os.mkdir(outDir)
			with open(os.path.join(outDir, item.name + Const.LuaFileExtention), "w", encoding = "utf-8") as file:
				file.write(output)

	print("complete! file num = %s, message num = %s" % (len(validFiles), pNum))
