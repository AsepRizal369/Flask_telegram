
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

class Config:
    # PostgreSQL Configuration
    user_pg = os.environ.get("USER_DB_SECOND_PG")
    pw_pg = os.environ.get("PASS_DB_SECOND_PG")
    host_pg = os.environ.get("HOST_DB_SECOND_PG")
    port_pg = os.environ.get("PORT_DB_SECOND_PG")
    db_pg = os.environ.get("SERVICE_NAME_DB_SECOND_PG")

    SQLALCHEMY_DATABASE_URI_PG = f'postgresql://{user_pg}:{pw_pg}@{host_pg}:{port_pg}/{db_pg}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Oracle Configuration
    user_oracle = os.environ.get("USER_DB_SECOND_ORC")
    pw_oracle = os.environ.get("PASS_DB_SECOND_ORC")
    host_oracle = os.environ.get("HOST_DB_SECOND_ORC")
    port_oracle = os.environ.get("PORT_DB_SECOND_ORC")
    db_oracle = os.environ.get("SERVICE_NAME_DB_SECOND_ORC")

    # Note: For Oracle, use the 'cx_oracle' dialect and specify the 'service_name' in the connection string
    SQLALCHEMY_DATABASE_URI_ORACLE = f'oracle+cx_oracle://{user_oracle}:{pw_oracle}@{host_oracle}:{port_oracle}/?service_name={db_oracle}'

    # Create the PostgreSQL and Oracle engines
    engine_pg = create_engine(SQLALCHEMY_DATABASE_URI_PG)
    engine_oracle = create_engine(SQLALCHEMY_DATABASE_URI_ORACLE)


# get env bot tele
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
GROUP_ID_TELEGRAM = os.environ.get('GROUP_ID_TELEGRAM')