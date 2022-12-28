from libs.ch_db_control import create

#bot.ini ファイル読み込み
import configparser
config = configparser.ConfigParser()
config.read("config/bot.ini",encoding="utf-8")
print(config)
db_name = config["db"]["name"]
create(db_name)

