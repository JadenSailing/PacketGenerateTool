--CGTest
--Date 2021-08-13 21:51:40
--Author 

--测试发送消息
local CGTest = class("CGTest", LuaRequestPacket)

function CGTest:Init()
	self:SetupGameServerPacket(2001)
	self.index = 100

	self.name = "hello"
	self.playerLen = 3
	self.playerList2 = {}
end

function CGTest:WriteStream()
	--int
	self:WriteInt32(self.index)
	--定长int数组
	for i = 1, 10 do
		self:WriteInt32(self.indexArray[i])
	end
	--定长字符串
	self:WriteCharArray(self.name, 30, true, true)
	self:WriteInt32(self.playerLen)
	--不定长player数组
	for i = 1, self.playerLen do
		self:WriteInt32(self.playerList2[i].mainEquip.equipId)
		self:WriteInt32(self.playerList2[i].mainEquip.itemLen)
		for j = 1, self.itemLen do
			self:WriteInt32(self.playerList2[i].mainEquip.equipItem[j].id)
			self:WriteCharArray(self.playerList2[i].mainEquip.equipItem[j].name, 10, true, true)
		end
		for j = 1, 4 do
			self:WriteInt32(self.playerList2[i].objIds[j])
		end
		self:WriteInt32(self.playerList2[i].equipLen)
		for j = 1, self.equipLen do
			self:WriteInt32(self.playerList2[i].equipList[j].equipId)
			self:WriteInt32(self.playerList2[i].equipList[j].itemLen)
			for k = 1, self.itemLen do
				self:WriteInt32(self.playerList2[i].equipList[j].equipItem[k].id)
				self:WriteCharArray(self.playerList2[i].equipList[j].equipItem[k].name, 10, true, true)
			end
		end
	end
end

return CGTest