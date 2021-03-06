--GCTest
--Date 2020-11-26 17:01:52
--Author 

--测试返回消息
local GCTest = class("GCTest", LuaResponsePacket)

function GCTest:ReadStream()
	--int
	self.index = self:ReadInt32()
	--定长int数组
	self.indexArray = {}
	for i = 1, 10 do
		self.indexArray[i] = self.ReadInt32()
	end
	self.indexLen = self:ReadInt32()
	--不定长int数组
	self.indexArray2 = {}
	for i = 1, self.indexLen do
		self.indexArray2[i] = self.ReadInt32()
	end
	self.shortData = self:ReadInt16()
	self.ushortData = self:ReadUInt16()
	self.int64Data = self:ReadInt32()
	self.uint64Data = self:ReadUInt32()
	self.byteData = self:ReadByte()
	self.floatData = self:ReadSingle()
	self.doubleData = self:ReadDouble()
	self.boolData = self:ReadBool()
	self.shortData = {}
	for i = 1, 1 do
		self.shortData[i] = self.ReadInt16()
	end
	self.ushortData = {}
	for i = 1, 2 do
		self.ushortData[i] = self.ReadUInt16()
	end
	self.int64Data = {}
	for i = 1, 3 do
		self.int64Data[i] = self.ReadInt32()
	end
	self.uint64Data = {}
	for i = 1, 4 do
		self.uint64Data[i] = self.ReadUInt32()
	end
	self.byteLen = self:ReadInt32()
	self.byteData = {}
	for i = 1, self.byteLen do
		self.byteData[i] = self.ReadByte()
	end
	self.floatLen = self:ReadInt32()
	self.floatData = {}
	for i = 1, self.floatLen do
		self.floatData[i] = self.ReadSingle()
	end
	self.doubleLen = self:ReadInt32()
	self.doubleData = {}
	for i = 1, self.doubleLen do
		self.doubleData[i] = self.ReadDouble()
	end
	self.boolLen = self:ReadInt32()
	self.boolData = {}
	for i = 1, self.boolLen do
		self.boolData[i] = self.ReadBool()
	end
	--定长字符串
	self.name = self:ReadString(30)
	self.nameLen = self:ReadInt32()
	--不定长字符串
	self.name2 = self:ReadString(self.nameLen)
	--单一item
	self.oneItem = {}
	self.oneItem.id = self.ReadInt32()
	self.oneItem.name = self.ReadString(10)
	self.oneItem.isBind = self.ReadBool()
	--单一equip
	self.oneEquip = {}
	self.oneEquip.equipId = self.ReadInt32()
	self.oneEquip.itemLen = self.ReadInt32()
	for i = 1, self.oneEquip.itemLen do
		self.oneEquip.equipItem[i] = {}
		self.oneEquip.equipItem[i].id = self.ReadInt32()
		self.oneEquip.equipItem[i].name = self.ReadString(10)
		self.oneEquip.equipItem[i].isBind = self.ReadBool()
	end
	--单一player
	self.onePlayer = {}
	self.onePlayer.mainEquip = {}
	self.onePlayer.mainEquip.equipId = self.ReadInt32()
	self.onePlayer.mainEquip.itemLen = self.ReadInt32()
	for i = 1, self.onePlayer.mainEquip.itemLen do
		self.onePlayer.mainEquip.equipItem[i] = {}
		self.onePlayer.mainEquip.equipItem[i].id = self.ReadInt32()
		self.onePlayer.mainEquip.equipItem[i].name = self.ReadString(10)
		self.onePlayer.mainEquip.equipItem[i].isBind = self.ReadBool()
	end
	for i = 1, 4 do
		self.onePlayer.objIds[i] = self.ReadInt32()
	end
	self.onePlayer.equipLen = self.ReadInt32()
	for i = 1, self.onePlayer.equipLen do
		self.onePlayer.equipList[i] = {}
		self.onePlayer.equipList[i].equipId = self.ReadInt32()
		self.onePlayer.equipList[i].itemLen = self.ReadInt32()
		for j = 1, self.onePlayer.equipList[i].itemLen do
			self.onePlayer.equipList[i].equipItem[j] = {}
			self.onePlayer.equipList[i].equipItem[j].id = self.ReadInt32()
			self.onePlayer.equipList[i].equipItem[j].name = self.ReadString(10)
			self.onePlayer.equipList[i].equipItem[j].isBind = self.ReadBool()
		end
	end
	--定长item数组
	self.itemList1 = {}
	for i = 1, 5 do
		self.itemList1[i] = {}
		self.itemList1[i].id = self.ReadInt32()
		self.itemList1[i].name = self.ReadString(10)
		self.itemList1[i].isBind = self.ReadBool()
	end
	self.itemLen = self:ReadInt32()
	--不定长item数组
	self.itemList2 = {}
	for i = 1, self.itemLen do
		self.itemList2[i] = {}
		self.itemList2[i].id = self.ReadInt32()
		self.itemList2[i].name = self.ReadString(10)
		self.itemList2[i].isBind = self.ReadBool()
	end
	--定长equip数组
	self.equipList1 = {}
	for i = 1, 6 do
		self.equipList1[i] = {}
		self.equipList1[i].equipId = self.ReadInt32()
		self.equipList1[i].itemLen = self.ReadInt32()
		for j = 1, self.equipList1[i].itemLen do
			self.equipList1[i].equipItem[j] = {}
			self.equipList1[i].equipItem[j].id = self.ReadInt32()
			self.equipList1[i].equipItem[j].name = self.ReadString(10)
			self.equipList1[i].equipItem[j].isBind = self.ReadBool()
		end
	end
	self.equipLen = self:ReadInt32()
	--不定长equip数组
	self.equipList2 = {}
	for i = 1, self.equipLen do
		self.equipList2[i] = {}
		self.equipList2[i].equipId = self.ReadInt32()
		self.equipList2[i].itemLen = self.ReadInt32()
		for j = 1, self.equipList2[i].itemLen do
			self.equipList2[i].equipItem[j] = {}
			self.equipList2[i].equipItem[j].id = self.ReadInt32()
			self.equipList2[i].equipItem[j].name = self.ReadString(10)
			self.equipList2[i].equipItem[j].isBind = self.ReadBool()
		end
	end
	--定长player数组
	self.playerList1 = {}
	for i = 1, 7 do
		self.playerList1[i] = {}
		self.playerList1[i].mainEquip = {}
		self.playerList1[i].mainEquip.equipId = self.ReadInt32()
		self.playerList1[i].mainEquip.itemLen = self.ReadInt32()
		for j = 1, self.playerList1[i].mainEquip.itemLen do
			self.playerList1[i].mainEquip.equipItem[j] = {}
			self.playerList1[i].mainEquip.equipItem[j].id = self.ReadInt32()
			self.playerList1[i].mainEquip.equipItem[j].name = self.ReadString(10)
			self.playerList1[i].mainEquip.equipItem[j].isBind = self.ReadBool()
		end
		for j = 1, 4 do
			self.playerList1[i].objIds[j] = self.ReadInt32()
		end
		self.playerList1[i].equipLen = self.ReadInt32()
		for j = 1, self.playerList1[i].equipLen do
			self.playerList1[i].equipList[j] = {}
			self.playerList1[i].equipList[j].equipId = self.ReadInt32()
			self.playerList1[i].equipList[j].itemLen = self.ReadInt32()
			for k = 1, self.playerList1[i].equipList[j].itemLen do
				self.playerList1[i].equipList[j].equipItem[k] = {}
				self.playerList1[i].equipList[j].equipItem[k].id = self.ReadInt32()
				self.playerList1[i].equipList[j].equipItem[k].name = self.ReadString(10)
				self.playerList1[i].equipList[j].equipItem[k].isBind = self.ReadBool()
			end
		end
	end
	self.playerLen = self:ReadInt32()
	--不定长player数组
	self.playerList2 = {}
	for i = 1, self.playerLen do
		self.playerList2[i] = {}
		self.playerList2[i].mainEquip = {}
		self.playerList2[i].mainEquip.equipId = self.ReadInt32()
		self.playerList2[i].mainEquip.itemLen = self.ReadInt32()
		for j = 1, self.playerList2[i].mainEquip.itemLen do
			self.playerList2[i].mainEquip.equipItem[j] = {}
			self.playerList2[i].mainEquip.equipItem[j].id = self.ReadInt32()
			self.playerList2[i].mainEquip.equipItem[j].name = self.ReadString(10)
			self.playerList2[i].mainEquip.equipItem[j].isBind = self.ReadBool()
		end
		for j = 1, 4 do
			self.playerList2[i].objIds[j] = self.ReadInt32()
		end
		self.playerList2[i].equipLen = self.ReadInt32()
		for j = 1, self.playerList2[i].equipLen do
			self.playerList2[i].equipList[j] = {}
			self.playerList2[i].equipList[j].equipId = self.ReadInt32()
			self.playerList2[i].equipList[j].itemLen = self.ReadInt32()
			for k = 1, self.playerList2[i].equipList[j].itemLen do
				self.playerList2[i].equipList[j].equipItem[k] = {}
				self.playerList2[i].equipList[j].equipItem[k].id = self.ReadInt32()
				self.playerList2[i].equipList[j].equipItem[k].name = self.ReadString(10)
				self.playerList2[i].equipList[j].equipItem[k].isBind = self.ReadBool()
			end
		end
	end
end

function GCTest:Handler()
	Log.Info("GCTest:Handler...")
end

return GCTest