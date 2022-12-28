from discord import Embed

#bot.ini ファイル読み込み
import configparser
config = configparser.ConfigParser()
config.read("config/bot.ini",encoding="utf-8")

#対象の言語リスト , リアクション用絵文字リスト
lang_list = [config["embed_lang_list"][embed_info] for embed_info in config["embed_lang_list"]]
emoji_data = [config["emoji_data"][emoji] for emoji in config["emoji_data"]]

#チャンネル作成時に実行される関数
async def ch_creation_msg(client,msg_send_ch):
    embed = Embed(title=f"使用する翻訳言語",color=0xCCFFFF)
    #embedに言語一覧を追加する
    for i in range(0,len(lang_list),2):
        embed.add_field(name=f"{lang_list[i]}",value=f"{lang_list[i+1]}",inline=False)
    #指定のチャンネルに送信する
    message_send_channel = client.get_channel(msg_send_ch)
    reaction_message = await message_send_channel.send(embed=embed)
    #リアクションを追加
    for reaction in emoji_data:
        await reaction_message.add_reaction(reaction)
    return reaction_message