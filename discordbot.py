import discord
from discord import app_commands
from apikey import TOKEN,channelid

"""
discordbot初期設定
"""
#初期設定
intents=discord.Intents.default()
intents.messages=True
intents.message_content=True
client =discord.Client(intents=intents)
bot = app_commands.CommandTree(client)

"""
botコマンドプログラム
"""


"""
起動
"""
client.run(TOKEN)