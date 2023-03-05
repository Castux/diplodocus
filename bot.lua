local discordia = require('discordia')
local json = require('json')
local config = dofile('config.lua')

--[[ Setup ]]

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
	fp:close()
end

local function isPrivate(message)
	return message.channel.type == discordia.enums.channelType.private
end

local function reply(message, text)
	message.channel:send(text)
end

local function replyf(message, ...)
	message.channel:send(string.format(...))
end

--[[ Commands ]]

local commands = {}

function commands.ping(message, payload)
	reply(message, "Pong! " .. payload)
end

function commands.status(message)

	if data.phase then

		local count = 0
		for k,v in pairs(data[data.phase]) do
			count = count + 1
		end

		local plural =
			count == 0 and "No users have" or
			count == 1 and "One user has" or
			(count .. " users have")

		replyf(message, "Accepting orders for **%s**. %s submitted their orders.",
			data.phase,
			plural
		)
	else
		reply(message, "Not accepting orders at the moment")
	end
	
end

function commands.startphase(message, payload)

	if not payload or #payload == 0 then
		reply(message, "Invalid phase")
		return
	end

	data.phase = payload
	data[payload] = {}
	reply(message, "Starting phase **" .. payload .. "**")
end

function commands.stopphase(message, payload)

	if not data.phase then
		reply(message, "No current phase.")
		return
	end

	local all = {}

	for player, orders in pairs(data[data.phase]) do
		table.insert(all, "=========")
		table.insert(all, player)
		table.insert(all, orders)
	end

	table.insert(all, "=========")

	replyf(message, "Stopped phase **%s**.", data.phase)
	reply(message, table.concat(all, "\n"))

	data.phase = nil
end

function commands.send(message, payload, user)

	if not data.phase then
		reply(message, "Not currently accepting orders.")
		return
	end

	data[data.phase][user] = payload

	replyf(message, "Got it! Orders for **%s** in **%s**:\n%s",
		user,
		data.phase,
		payload
	)
end


function commands.check(message, payload, user)

	if not data.phase then
		reply(message, "Not currently accepting orders.")
		return
	end

	local orders = data[data.phase][user]

	if not orders then
		replyf(message, "You have not submitted orders yet for **%s**.", data.phase)
	else
		replyf(message, "Your orders for **%s**:\n%s",
			data.phase,
			orders
		)
	end
end

--[[ Bot start ]]

client:on('ready', function()

	print('Logged in as '.. client.user.username)
	loadData()
end)

client:on('messageCreate', function(message)

	for com, func in pairs(commands) do
		local user = message.author.username
		local trigger,payload = message.content:match("^(" .. config.prefix .. com .. ")%s*(.*)")
		if trigger then
			print(message.timestamp, user, com, payload)
			func(message, payload, user)
			saveData()
		end
	end

end)

client:run('Bot ' .. config.token)
