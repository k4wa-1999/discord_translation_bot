import sqlite3

#bot.ini ファイル読み込み
import configparser
config = configparser.ConfigParser()
config.read("../config/bot.ini",encoding="utf-8")

#DBコントロール
def sql_control(db_name,sql,commit):
    sql = f''' {sql}'''
    con = sqlite3.connect(f"../data/{db_name}.db")
    cur = con.cursor()
    cur.execute(sql)
    if commit == True:
        con.commit()
    cur = cur.fetchall()
    con.close()
    return cur

#DB作成
def create(db_name):
    db_sql = config["db"]["role_db_configuration"]
    sql = f"""
    CREATE table {db_name}(
        {db_sql});
    """
    sql_control(db_name,sql,commit=True)

#DBにデータ追加
def add(db_name,guild):
    sql = f"""insert into {db_name}(guild_id)values({guild});"""
    sql_control(db_name,sql,commit=True)

#DB内の特定のデータを検索
def search(db_name,guild_id):
    sql = f''' SELECT *
            FROM {db_name}
            WHERE guild_id = {guild_id}'''
    cur = sql_control(db_name,sql,commit=False)
    return cur

#DB内の特定のデータを変更
def change(db_name,guild,role,role_id):
    sql = f''' UPDATE {db_name}
                SET {role} = {role_id}
                WHERE guild_id = {guild};'''
    sql_control(db_name,sql,commit=True)

def dell(db_name,db_id):
    sql = f"""
            DELETE FROM {db_name} WHERE id="{db_id}";"""
    sql_control(db_name,sql,commit=True)
