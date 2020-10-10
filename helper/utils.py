from flask import Flask
import json
import os
import psycopg2
app = Flask(__name__)


# Query channel information using channel_id
def get_channel(channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT secret, access_token FROM channel WHERE channel.id = '%s' " % channel_id
    app.logger.info("Start query channel: " + sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    app.logger.info("Result: " + json.dumps(result))
    cursor.close()
    conn.close()
    return result


# Check user exist
def is_user(user_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT exists(SELECT 1 FROM line_user WHERE id = '%s' )" % user_id
    app.logger.info("Start check user: " + sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    app.logger.info("Result: " + str(result))
    cursor.close()
    conn.close()
    return result
