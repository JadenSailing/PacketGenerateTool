--GCOpenMyBag
--Date 2020-11-26 17:01:52
--Author LiuZhen

--扩展背包格子返回
local GCOpenMyBag = class("GCOpenMyBag", LuaResponsePacket)

function GCOpenMyBag:ReadStream()
	--当前开放的格子数
	self.curOpenNum = self:ReadByte()
	--最大开放的格子数
	self.maxOpenNum = self:ReadByte()
end

function GCOpenMyBag:Handler()
	Log.Info("GCOpenMyBag:Handler...")
end

return GCOpenMyBag