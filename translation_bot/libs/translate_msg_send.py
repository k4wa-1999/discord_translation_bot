from libs.translation import translation
from libs.ch_db_control import search

lang_list=["ja","en","zh-TW","ko","th","id"]


async def tr_send(db_name,client,Embed,guild,channel,msg):
    guild_list = search(db_name,guild)
    for guild in guild_list:
        for i,ch in enumerate(guild[3:]):
            if ch == None:
                continue
            elif channel == ch:
                continue
            send_channel = client.get_channel(ch)
            if "http" in msg.content:
                try:
                    embed = Embed(title=f"URL",description= f"{msg.content}")
                    embed.set_author(name=msg.author,icon_url= msg.author.avatar.url)
                    await send_channel.send(embed = embed)
                    #await send_channel.send(tr_msg)
                except AttributeError:
                    pass

            elif msg.attachments:
                embed = Embed(title=f"URL",description= f"{msg.content}")
                embed.set_image(url=msg.attachments[0])
                embed.set_author(name=msg.author,icon_url= msg.author.avatar.url)
                await send_channel.send(embed = embed)
                    
            else:
                tr_msg = translation(lang_list[i],msg.content)
                embed = Embed(title=f"{tr_msg}",description= f"{msg.content}")
                embed.set_author(name=msg.author,icon_url= msg.author.display_avatar)
                await send_channel.send(embed = embed)
                #await send_channel.send(tr_msg)
