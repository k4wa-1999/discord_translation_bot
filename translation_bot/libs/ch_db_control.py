import sqlite3

#bot.ini ファイル読み込み
import configparser
config = configparser.ConfigParser()
config.read("config/bot.ini",encoding="utf-8")
db_sql = config["db"]["db_configuration"]
#DBコントロール
def sql_control(db_name,sql,commit):
    sql = f''' {sql}'''
    con = sqlite3.connect(f"data/{db_name}.db")
    cur = con.cursor()
    cur.execute(sql)
    if commit == True:
        con.commit()
    cur = cur.fetchall()
    con.close()
    return cur
#DB作成
def create(db_name):
    sql = f"""
    CREATE table {db_name}(
        {db_sql});
    """
    sql_control(db_name,sql,commit=True)
    
#column追加
def column_add(db_name,column_name):
    sql = f'''ALTER TABLE {db_name} 
            ADD COLUMN "{column_name}";'''
    sql_control(db_name,sql,commit=True)

#DBにデータ追加
def add(db_name,guild,category):
    #sql = f"""insert into server_info(guild_id,category,ch1_jp,ch2_en,ch3_cn,ch4_kr,ch5_th,ch6_id)values({guild},{category},{ch1},{ch2},{ch3},{ch4},{ch5},{ch6});"""
    sql = f"""insert into {db_name}(guild_id,category)values({guild},{category});"""
    sql_control(db_name,sql,commit=True)

#DB内の特定のデータを検索
def search(db_name,guild_id):
    sql = f''' SELECT *
            FROM {db_name}
            WHERE guild_id = {guild_id}'''
    cur = sql_control(db_name,sql,commit=False)
    return cur

#DB内の特定のデータを変更
def change(db_name,guild,ch,ch_id):
    sql = f''' UPDATE {db_name}
                SET {ch} = {ch_id}
                WHERE guild_id = {guild};'''
    sql_control(db_name,sql,commit=True)

def dell(db_name,db_id):
    sql = f"""
            DELETE FROM {db_name} WHERE id="{db_id}";"""
    sql_control(db_name,sql,commit=True)

