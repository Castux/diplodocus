local discordia = require('discordia')
local json = require('json')
local config = dofile('config.lua')

--[[ Setup ]]

local client = discordia.Client {
	logFile = 'diplodocus.log'
}

local data = {}
local function loadData()

	client:info('Loading data...')

	local fp = io.open(config.data, "r")

	if fp then
		local txt = fp:read("a")
		data = json.decode(txt)

		if not data then
			client:error("Invalid data.json")
			client:stop()
			return
		end
	else
		data = {}
	end

	client:info('Done.')
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
			count == 0 and "No player has" or
			count == 1 and "One player has" or
			(count .. " players have")

		replyf(message, "Accepting orders for **%s**. %s submitted their orders.",
			data.phase,
			plural
		)
	else
		reply(message, "Not accepting orders at the moment.")
	end
end

function commands.startphase(message, payload)

	if isPrivate(message) then
		reply(message, "GM actions only valid in public channels")
		return
	end

	if not payload or #payload == 0 then
		reply(message, "Invalid phase")
		return
	end

	data.phase = payload
	data[payload] = {}
	reply(message, "Starting phase **" .. payload .. "**")
end

function commands.stopphase(message, payload)

	if isPrivate(message) then
		reply(message, "GM actions only valid in public channels")
		return
	end

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

function commands.remove(message, payload, user)

	if not data.phase then
		reply(message, "Not currently accepting orders.")
		return
	end

	if data[data.phase][user] then
		data[data.phase][user] = nil
		replyf(message, "Removed your orders for **%s**.", data.phase)
	else
		replyf(message, "You have not submitted orders yet for **%s**.", data.phase)
	end
end

function commands.kill(message)
	
	reply("Ok. Signing off.")
	client:close()
	os.exit()
end

local helpMessage = string.format([[
Sorry, I didn't quite get that. Try these:
**%ssend <orders>**: send your orders for the current phase. They can be on multiple lines. That will overwrite previously sent orders if any.
**%scheck**: check what are your current orders for the phase.
**%sremove**: delete your current orders.
**%sstatus**: see what the current phase is and how many have submitted orders so far.
]], config.prefix, config.prefix, config.prefix, config.prefix)

--[[ Bot start ]]

client:on('ready', function()

	client:info('Logged in as '.. client.user.username)
	loadData()
end)

client:on('messageCreate', function(message)

	for com, func in pairs(commands) do
		local user = message.author.username
		local trigger,payload = message.content:match("^(" .. config.prefix .. com .. ")%s*(.*)")
		if trigger then
			client:info("Command received: %s, %s, %s", user, com, payload or "")
			func(message, payload, user)
			saveData()

			return
		end
	end

	-- No match

	if isPrivate(message) and message.author ~= client.user then
		reply(message, helpMessage)
	end

end)

client:run('Bot ' .. config.token)
