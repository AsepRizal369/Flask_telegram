import requests
import settings
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from settings import Config
from sqlalchemy import text


TOKEN = settings.TELEGRAM_BOT_TOKEN
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def send_message(text, chat_id, parse_mode=None):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"  
    params = {
        'text': text,
        'chat_id': chat_id,
        'parse_mode': parse_mode  # 'html' untuk HTML, 'markdown' untuk Markdown, atau kosong untuk teks biasa
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    result = requests.post(url, params=params, headers=headers)
    return result

def getSysdateHour(interval=None, intervaltanggal=None, jam=None):
    connection = Config.engine_oracle.connect()
    if interval:
        with current_app.app_context():
            result = connection.execute(
                text(f"SELECT TO_CHAR(TO_TIMESTAMP(to_char(sysdate-interval '{interval}' hour,'YYYY-MM-DD HH24'),'YYYY-MM-DD HH24'),'HH24') FROM dual")
            )
            data = [row[0] for row in result.fetchall()]
        return data
    elif intervaltanggal and jam:
        with current_app.app_context():
            result = connection.execute(
                text(f"SELECT TO_CHAR(TO_TIMESTAMP('{intervaltanggal} {jam}' ,'YYYY-MM-DD HH24')- interval '3' hour,'YYYY-MM-DD HH24') FROM dual")
            )
            data = [row[0] for row in result.fetchall()]

        return data
    else:
        with current_app.app_context():
            result = connection.execute(
                text("SELECT TO_CHAR(TO_TIMESTAMP(to_char(sysdate,'YYYY-MM-DD HH24'),'YYYY-MM-DD HH24'),'HH24') FROM dual")
            )
            data = [row[0] for row in result.fetchall()]
        return data
