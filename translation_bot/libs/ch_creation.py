from asyncio.windows_events import NULL
from libs.ch_db_control import add,change,search
import libs.role_db_control as db_role
import discord

import configparser
config = configparser.ConfigParser()
config.read("../config/bot.ini",encoding="utf-8")

emoji_data = [config["emoji_data"][emoji] for emoji in config["emoji_data"]]
db_name = config["db"]["name"]
role_db_name = config["db"]["neme_role"]
db_column = [config["db_column"][column_name] for column_name in config["db_column"]]
role_db_column = [config["db_column_role"][column_name] for column_name in config["db_column_role"]]
async def cg_ch_creation(guild,reaction,com_executing):
    guild_id = guild.id
    if len(search(db_name,guild_id)) == 0:
        Category = await guild.create_category("translation_ch")
        await Category.set_permissions(guild.default_role, read_messages=False,send_messages=False)
        add(db_name,guild.id,Category.id)
        db_role.add(role_db_name,guild.id)
        for i,lang in enumerate(com_executing):
            if lang == NULL:
                continue
            if lang == "🆗":
                continue
            else:
                p_roll = await guild.create_role(name=f'{emoji_data[i]}', permissions=discord.Permissions(permissions=0), colour=0xffffff)
                db_role.change(role_db_name,guild.id,role_db_column[i],p_roll.id)
                ch = await guild.create_text_channel(f"{emoji_data[i]}", category = Category)
                await ch.set_permissions(p_roll, read_messages=True,send_messages=True)
                change(db_name,guild.id,db_column[i+1],ch.id)
        await reaction.message.channel.send("チャンネルを作成しました！！")