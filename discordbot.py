import discord
from discord import app_commands
import os
from dotenv import load_dotenv

"""
discordbot初期設定
"""
#bot Tokenを環境ファイルから読み込み
load_dotenv()
TOKEN=os.environ["TOKEN"]

#channelid
channelid="entry channelid"

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