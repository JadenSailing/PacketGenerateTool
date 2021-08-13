#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PacketGenerator

import os
import configparser
cfg = configparser.ConfigParser()
cfg.read("Config.ini", encoding = "utf8")

print("Version = " + cfg.get("Global", "Version"))
from src import *
outputDir = cfg.get("Global", "OutPutDir")
print("outputDir = " + outputDir)
if(not os.path.exists(outputDir)):
    raise("outputDir not exists!")
Const.Cfg = cfg
exportPacketList()