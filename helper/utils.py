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
def is_user(user_id, channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT exists(SELECT 1 FROM line_user WHERE id = '{user_id}' AND channel_id = '{channel_id}' )"
    sql = sql.format(channel_id = channel_id, user_id = user_id)
    app.logger.info("Start check user: " + sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    result = result[0]
    app.logger.info("Result: " + str(result))
    cursor.close()
    conn.close()
    return result


# Get user info
def get_user(user_id, channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()

    sql = "SELECT channel_id, id, name, gender, birth_day, birth_time, status \
    FROM line_user WHERE id = '{user_id}' \
    AND channel_id = '{channel_id}'"

    sql = sql.format(channel_id = channel_id,
                     user_id = user_id)

    app.logger.info("Start query user: " + sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    app.logger.info("Result: " + str(result))
    cursor.close()
    conn.close()
    return result


# Store user info after complete the first stage info collection
def store_user_info(channel_id, user_id, user_name, user_gender, user_birth_day, user_birth_time, user_status):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()

    # sql = "INSERT INTO line_user \
    # VALUES  ('{channel_id}','{user_id}','{user_name}','{user_gender}','{user_birth_day}','{user_birth_time}','{user_status}') \
    # ON CONFLICT (id) DO UPDATE \
    # SET channel_id = '{channel_id}', name = '{user_name}', \
    # gender = '{user_gender}', birth_day = '{user_birth_day}', \
    # birth_time = '{user_birth_time}', status = '{user_status}' \
    # WHERE line_user.id = '{user_id}' "

    sql = "INSERT INTO line_user \
    VALUES  ('{channel_id}','{user_id}','{user_name}','{user_gender}','{user_birth_day}','{user_birth_time}','{user_status}')"

    sql = sql.format(channel_id = channel_id,
                     user_id = user_id,
                     user_name = user_name,
                     user_gender = user_gender,
                     user_birth_day = user_birth_day,
                     user_birth_time = user_birth_time,
                     user_status = user_status)
    app.logger.info("Insert user info: " + sql)

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()
