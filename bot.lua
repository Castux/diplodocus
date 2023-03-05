local discordia = require('discordia')
local json = require('json')

local client = discordia.Client{
	logFile = 'diplodocus.log',
	logLevel = discordia.enums.logLevel.debug
}

client:on('ready', function()
	-- client.user is the path for your bot
	print('Logged in as '.. client.user.username)
end)

client:on('messageCreate', function(message)
	for k,v in pairs(message) do
		print(k,v)
	end
	if message.content == '!ping' then
		message.channel:send('Pong!')
	end
end)

client:run('Bot MjUxMzQwMjg5NDI2MzI1NTA0.G7h84S.26vA4eobx01JTBnUVHOA3LnXPVBah7UdofNTfg')
