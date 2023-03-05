local discordia = require('discordia')
local json = require('json')
local config = dofile('config.lua')

local client = discordia.Client()

local data = {}
local function loadData()

	print('Loading data...')

	local fp = io.open(config.data, "r")

	if fp then 
		local txt = fp:read("a")
		data = json.decode(txt)

		if not data then
			error("Invalid data.json")
		end
	else
		data = {}
	end

	print('Done.')
end

local function saveData()
	local fp = io.open(config.data, "w")
	fp:write(json.encode(data))

	print("Wrote data to " .. config.data)
end

local function isPrivate(message)
	return message.channel.type == discordia.enums.channelType.private
end

client:on('ready', function()
	print('Logged in as '.. client.user.username)
	loadData()
end)

local commands = {

	ping = function(message)
		message.channel:send("Pong!")
	end

}

client:on('messageCreate', function(message)
	
	for com, func in pairs(commands) do
		if message.content:lower():match("^" .. config.prefix .. com) then
			func(message)
		end
	end
end)

client:run('Bot ' .. config.token)
