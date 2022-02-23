"""

Это переписанный код с видео-уроков по написаню бота для сервера дискорд. Автор кода: Fsoky (Fsoky Community)
Здесь вы найдете весь функционал, кроме:
карточки пользователя, проигрывание музыки в голосовом канале

Также некоторые части кода были переписаны более верно и удобно, например команда help и ивент on_message

Некоторые функции или строчки кода буду содержать в себе комментарий для описания того или иного действия.

P.S если что-то не будет работать или возникнет какая-либо "заводская" ошибка, прошу отписать - https://vk.com/fsoky


Links:
https://t.me/officialfsokycommchat​​​ - телеграм чат
https://vk.com/fsoky - группа в вк (присутствует беседа)
https://pastebin.com/u/Fsoky​ - Pastebin автора
https://github.com/Fsoky - GitHub автора



01.04.2021 Fsoky Community

"""

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None, intents=discord.Intents.all())


@bot.event
async def on_ready():
	print("Bot was connected to the server")

	await bot.change_presence(status=discord.Status.online, activity=discord.Game("help")) # Изменяем статус боту

	"""Статус

	Также можно установить не только Game, но и Watching или Streaming..
	Точные классы посмотрите в документации по discord.py

	https://discordpy.readthedocs.io/en/latest/api.html

	"""


@bot.event
async def on_message(message):
	await bot.process_commands(message)

	msg = message.content.lower()
	greeting_words = ["hello", "hi", "привет"]
	censored_words = ["дурак", "дура", "придурок"]

	if msg in greeting_words:
		await message.channel.send(f"{message.author.name}, приветствую тебя!")

	# Filter censored words
	for bad_content in msg.split(" "):
		if bad_content in censored_words:
			await message.channel.send(f"{message.author.mention}, ай-ай-ай... Плохо, плохо, так нельзя!")


@bot.event
async def on_member_join(member):
	channel = bot.get_channel() # Передайте ID канала
	role = discord.utils.get(member.guild.roles, id=role_id) # Передайте ID роли

	await member.add_roles(role)


@bot.event
async def on_command_error(ctx, error):
	"""Работа с ошибками
	
	Работать с ошибками можно с двумя способами, как в видео (11 серия "Работа с ошибками")
	или же в данной функции. Легче всего использовать второй вариант.. 

	"""

	print(error)

	if isinstance(error, commands.MissingPermissions):
		await ctx.send(f"{ctx.author}, у вас недостаточно прав для выполнения данной команды!")
	elif isinstance(error, commands.UserInputError):
		await ctx.send(embed=discord.Embed(
			description=f"Правильное использование команды: `{ctx.prefix}{ctx.command.name}` ({ctx.command.brief})\nExample: {ctx.prefix}{ctx.command.usage}"
		))


@bot.command(name="очистить", brief="Очистить чат от сообщений, по умолчанию 10 сообщений", usage="clear <amount=10>")
async def clear(ctx, amount: int=10):
	await ctx.channel.purge(limit=amount)
	await ctx.send(f"Was deleted {amount} messages...")


@bot.command(name="кик", brief="Выгнать пользователя с сервера", usage="kick <@user> <reason=None>")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
	await ctx.message.delete(delay=1) # Если желаете удалять сообщение после отправки с задержкой

	await member.send(f"You was kicked from server") # Отправить личное сообщение пользователю
	await ctx.send(f"Member {member.mention} was kicked from this server!")
	await member.kick(reason=reason)


@bot.command(name="бан", brief="Забанить пользователя на сервере", usage="ban <@user> <reason=None>")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
	await member.send(f"You was banned on server") # Отправить личное сообщение пользователю
	await ctx.send(f"Member {member.mention} was banned on this server")
	await member.ban(reason=reason)


@bot.command(name="разбанить", brief="Разбанить пользователя на сервере", usage="unban <user_id>")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
	user = await bot.fetch_user(user_id)
	await ctx.guild.unban(user)


@bot.command()
async def help(ctx):
	"""Команда help

	Чтобы не писать тысячу строк одинакового кода, лучше занесем название и описание команд в списки,
	и переберм в цикле.

	"""

	embed = discord.Embed(
		title="Help menu",
		description="Here you can find the necessary command"
	)
	commands_list = ["clear", "kick", "ban", "unban"]
	descriptions_for_commands = ["Clear chat", "Kick user", "Ban user", "Unban user"]

	for command_name, description_command in zip(commands_list, descriptions_for_commands):
		embed.add_field(
			name=command_name,
			value=description_command,
			inline=False # Будет выводиться в столбик, если True - в строчку
		)

	await ctx.send(embed=embed)


@bot.command(name="мут", brief="Запретить пользователю писать (настройте роль и канал)", usage="mute <member>")
async def mute_user(ctx, member: discord.Member):
	mute_role = discord.utils.get(ctx.message.guild.roles, name="role name")

	await member.add_roles(mute_role)
	await ctx.send(f"{ctx.author} gave role mute to {member}")

	"""Временный мут

	Также вы можете сделать временный мут, для этого используйте модуль asyncio и метод sleep (asyncio.sleep).
	Пусть функция принимает параметр time_mute. Поставьте условие if "h" in time_mute:
	То есть, если вы пишите: !mute @user 1h, и в переменной time_mute находит букву "h" значит asyncio.sleep(time_mute[:1] * 3600)
	
	"""


@bot.command(name="join", brief="Подключение к голосовому каналу", usage="join")
async def join_to_channel(ctx):
	global voice
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	channel = ctx.message.author.voice.channel

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else:
		voice = await channel.connect()
		await ctx.send(f"Bot was connected to the voice channel")


@bot.command(name="leave", brief="Отключение от голосового канала", usage="leave")
async def leave_from_channel(ctx):
	global voice
	voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
	channel = ctx.message.author.voice.channel

	if voice and voice.is_connected():
		await voice.disconnect()
	else:
		voice = await channel.disconnect()
		await ctx.send(f"Bot was connected to the voice channel")


bot.run("TOKEN")
