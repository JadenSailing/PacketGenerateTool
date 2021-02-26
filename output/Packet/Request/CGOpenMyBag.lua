--CGOpenMyBag
--Date 2020-11-26 17:01:52
--Author LiuZhen

--扩展背包格子
local CGOpenMyBag = class("CGOpenMyBag", LuaRequestPacket)

function CGOpenMyBag:Init()
	self:SetupGameServerPacket(153)
end

function CGOpenMyBag:WriteStream()
end

return CGOpenMyBag