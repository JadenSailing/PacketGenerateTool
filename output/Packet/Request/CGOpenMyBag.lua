--CGOpenMyBag
--Date 2021-08-13 21:51:40
--Author LiuZhen

--扩展背包格子
local CGOpenMyBag = class("CGOpenMyBag", LuaRequestPacket)

function CGOpenMyBag:Init()
	self:SetupGameServerPacket(153)
end

function CGOpenMyBag:WriteStream()
end

return CGOpenMyBag