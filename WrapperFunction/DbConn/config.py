import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    snowflake_url = os.getenv("SNOWFLAKE_URL")
    username = os.getenv("SNOWFLAKE_USERNAME")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    snow_db = os.getenv("SNOWFLAKE_DATABASE")
    
    DB_CONFIG = snowflake_url = 'snowflake://{user}:{password}@{account_identifier}/{snow_db}'.format(
        user=username,
        password=password,
        account_identifier=snowflake_url,
        snow_db=snow_db
    )

config = Config