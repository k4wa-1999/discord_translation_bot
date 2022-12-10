import discord
from discord.ext import commands
import datetime
from libs.ch_db_control import search,change,dell,create
import libs.role_db_control as db_role
from libs.ch_creation_embed import ch_creation_msg
from libs.ch_creation import cg_ch_creation
from libs.translate_msg_send import tr_send

#bot.ini ファイル読み込み
import configparser
config = configparser.ConfigParser()
config.read("../config/bot.ini",encoding="utf-8")

#botにスラッシュコマンドを追加
class MyBot(commands.Bot):
    async def setup_hook(self):
        await self.tree.sync(guild=None)

#intent有効化
intents = discord.Intents.default()
intents.message_content = True
intents.reactions= True
intents.members = True
bot = MyBot(command_prefix="!", intents=intents,case_insensitive=True)

#データベース情報
db_name = config["db"]["name"]
role_db_name = config["db"]["neme_role"]
db_column = [config["db_column"][column_name] for column_name in config["db_column"]]
role_db_column = [config["db_column_role"][column_name] for column_name in config["db_column_role"]]
#DBファイルの存在確認(無い場合は作成されます。)
def dbfile_search():
    import glob
    ch_db_file_search = glob.glob(f"../data/{db_name}.db")
    role_db_file_search = glob.glob(f"../data/{role_db_name}.db")
    if not ch_db_file_search:
        create(db_name)
        print("チャンネル用DBファイルが作成されました。")
    else:
        print("DBファイルが読み込まれました。")
    
    if not role_db_file_search:
        db_role.create(role_db_name)
        print("ロール用DBファイルが作成されました。")
    else:
        print("DBファイルが読み込まれました。")
    
dbfile_search()

#コマンド実行中サーバー  選択したチャンネルリスト
com_executing_server = []
#DMからのメッセージの処理
@bot.check
async def globally_block_dms(ctx):
    return ctx.guild is not None

@bot.event
async def on_message(ctx):
    if ctx.author.bot:
        return
    Embed = discord.Embed
    guild = ctx.guild.id
    channel = ctx.channel.id
    if search(db_name,guild):
        guild_info = search(db_name,guild)
        if channel in guild_info[0]:
            await tr_send(db_name,bot,Embed,guild,channel,ctx)



#チャンネル作成コマンド実行
@bot.hybrid_command(description="翻訳チャンネルを作成します。",with_app_command=True)
@commands.has_permissions(administrator=True)
async def ch_creation(ctx):
    global creation_msg
    global added_language_msg
    #既にコマンド実行中の場合returnする。
    executing_guild_list = [guild_id[0] for guild_id in com_executing_server]
    if ctx.guild.id in executing_guild_list:
        await ctx.send(content="コマンドは既に実行されています。",delete_after=3.0)
        now_time = datetime.datetime.now()
        print(f"{now_time.strftime('%Y-%m-%d %H:%M:%S')} (error)コマンド実行中の為キャンセルされました。 サーバー: {ctx.guild.name} ユーザー: {ctx.author.name}")
        return
    #データベースに既にサーバーが追加されていないかをチェックする。
    elif len(search(db_name,ctx.guild.id)) == 0:
        creation_msg = await ctx.send("チャネルを作成します。")
        now_time = datetime.datetime.now()
        print(f"{now_time.strftime('%Y-%m-%d %H:%M:%S')} (execution)チャンネル作成コマンドが実行されました。サーバー: {ctx.guild.name} ユーザー: {ctx.author.name}")
        #コマンドを実行したサーバー情報をリストに追加
        com_executing_server.append([ctx.guild.id,None,None,None,None,None,None,None,ctx.author.id])
        #embedを送信する&チャンネルを選択するためのリアクションを追加する
        reaction_msg = await ch_creation_msg(bot,ctx.channel.id)
        #追加された言語の表示
        added_language_msg = await ctx.send(f"追加された言語:")
        #embedのIDを対象のguildリストに追加する
        for i,guild_info in enumerate(com_executing_server):
            if guild_info[0] == ctx.guild.id:
                com_executing_server[i][1] = reaction_msg.id
                return
    #データベースに登録されている場合の処理
    else:
        await ctx.send("チャンネルが既に存在します。")

#チャンネル削除コマンド実行
@bot.hybrid_command(description="翻訳チャンネルを削除します。",with_app_command=True)
@commands.has_permissions(administrator=True)
async def ch_delete(ctx):
    #同じuserか
    def check(msg):
        return msg.author == ctx.author

    delete_msg = await ctx.send("チャンネルを削除しまか？　y/n")
    msg = await bot.wait_for('message', check=check, timeout=30)
    if msg.content == "n" or msg.content == "no":
        await delete_msg.delete()
        await ctx.send("チャンネルを削除を中断します。",delete_after=3.0)
        return
    elif msg.content == "y" or msg.content == "yes":
        now_time = datetime.datetime.now()
        print(f"{now_time.strftime('%Y-%m-%d %H:%M:%S')} (execution)チャンネル削除コマンドが実行されました。サーバー: {ctx.guild.name} ユーザー: {ctx.author.name}")
        await delete_msg.delete()
        delete_msg = await ctx.send("チャンネルを削除します。")
        #削除するチャンネルがDBファイルに存在しなかった場合
        if len(search(db_name,ctx.guild.id)) == 0:
            await ctx.send("チャンネルがありません。")
        else:
            #DBファイルのチャンネルID情報からチャンネル削除を行います
            db_ch_id = search(db_name,ctx.guild.id)
            db_role_id = search(role_db_name,ctx.guild.id)

            for i,role_id in enumerate(db_role_id[0][2:]):
                if role_id == None:
                    continue
                try:
                    role = discord.utils.get(ctx.guild.roles, id=role_id)
                    await role.delete()
                    db_role.change(role_db_name,ctx.guild.id,role_db_column[i],"NULL")
                except AttributeError:
                    pass
            db_role.dell(role_db_name,db_role_id[0][0])

            for i,ch_id in enumerate(db_ch_id[0][2:]):
                if ch_id == None:
                    continue
                delete_ch = bot.get_channel(ch_id)
                try:
                    await delete_ch.delete()
                except AttributeError:
                    pass
                change(db_name,ctx.guild.id,db_column[i],"NULL")
            dell(db_name,db_ch_id[0][0])
            await delete_msg.delete()
            await ctx.send("チャンネルを削除しました！！")
    else:
        await delete_msg.delete()
        await ctx.send("y(yes) か n(no) でお答えください。")

#スライスコマンド追加
async def setup(bot):
    bot.add_command(ch_creation,ch_delete)

#コマンド実行で送信したメッセージに対するリアクションが押された時
@bot.event
async def on_reaction_add(reaction,user):
    if user.bot:
        return
    guild_id = [msg_id[0] for msg_id in com_executing_server]
    #com_executing_serverリストでのサーバーIDのインデックス取得
    guild_id_index = guild_id.index(user.guild.id)
    msg_id = com_executing_server[guild_id_index][1]
    user_id = com_executing_server[guild_id_index][len(com_executing_server[guild_id_index])-1]
    #リアクションの絵文字リスト
    emoji_data = [config["emoji_data"][emoji] for emoji in config["emoji_data"]]
    #リアクションしたい人が管理者じゃない場合return
    if not user.guild_permissions.administrator:
        return
    #リアクションしたい人がメッセージID and ユーザーIDが違うとreturn
    if not reaction.message.id == msg_id and user.id == user_id:
        return
    if str(reaction) == "🆗":
        #コマンド実行で作成されたメッセージをすべて削除
        await creation_msg.delete()
        await reaction.message.delete()
        await added_language_msg.delete()
        emoji_data_index = emoji_data.index(str(reaction))
        com_executing_server[guild_id_index][emoji_data_index+2] = str(reaction)
        added_language = [add_lang for add_lang in com_executing_server[guild_id_index]if add_lang in emoji_data]
        await cg_ch_creation(user.guild,reaction,added_language)
        com_executing_server.pop(guild_id_index)
        return
    if str(reaction) in emoji_data:
        emoji_data_index = emoji_data.index(str(reaction))
        com_executing_server[guild_id_index][emoji_data_index+2] = str(reaction)
        added_language = [add_lang for add_lang in com_executing_server[guild_id_index]if add_lang in emoji_data]
        await added_language_msg.edit(content=f"追加された言語:{' '.join(added_language)}")

#コマンド実行で送信したメッセージに対するリアクションが外された時
@bot.event
async def on_reaction_remove(reaction,user):
    guild_id = [msg_id[0] for msg_id in com_executing_server]
    #com_executing_serverリストでのサーバーIDのインデックス取得
    guild_id_index = guild_id.index(user.guild.id)
    msg_id = com_executing_server[guild_id_index][1]
    user_id = com_executing_server[guild_id_index][len(com_executing_server[guild_id_index])-1]
    #リアクションの絵文字リスト
    emoji_data = [config["emoji_data"][emoji] for emoji in config["emoji_data"]]
    #リアクションしたい人が管理者じゃない場合return
    if not user.guild_permissions.administrator:
        return
    #リアクションしたい人がメッセージID and ユーザーIDが違うとreturn
    if not reaction.message.id == msg_id and user.id == user_id:
        return
    if str(reaction) in emoji_data:
        emoji_data_index = emoji_data.index(str(reaction))
        com_executing_server[guild_id_index][emoji_data_index+2] = None
        added_language = [add_lang for add_lang in com_executing_server[guild_id_index]if add_lang in emoji_data]
        await added_language_msg.edit(content=f"追加された言語:{' '.join(added_language)}")



#コマンドエラー処理
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.MissingPermissions):
        await ctx.send("権限がありません。")
    print(error)

bot.run(config["bot"]["bot_token"])