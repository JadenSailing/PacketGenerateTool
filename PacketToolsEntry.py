#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PacketGenerator

import os
import configparser
cfg = configparser.ConfigParser()
cfg.read("Config.ini", encoding = "utf8")
print("PS Packet Tool Version " + cfg.get("Global", "Version"))
from src import *
Const.Cfg = cfg
exportPacketList()