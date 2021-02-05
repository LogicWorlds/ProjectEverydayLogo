import discord
from discord.ext import tasks, commands
import config as conf
import MakePerfect as mpi

class MyClient(discord.Client):
	async def on_ready(self):
		print('Logged on as', self.user)

	async def on_message(self, message):
        # don't respond to ourselves
		if message.author == self.user:
			return

		if message.content == 'кек':
			await message.channel.send('кек!')
				
		if message.content == 'Смени аву плз':
			await message.channel.send('Окей..')
			mpi.generateIcon()
			server = discord.Client.get_guild(self, id=message.guild.id)
			
			with open('out\out.png', 'rb') as f:
				icon = f.read()
			await server.edit(icon=icon)
			await message.channel.send('Нати.')
			

client = MyClient()
client.run(conf.bot_token)