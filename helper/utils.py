import os
import json
import redis
import psycopg2
from flask import Flask
from dotenv import load_dotenv

# start app
app = Flask(__name__)
load_dotenv(os.path.join(os.getcwd(), '.env'))

# Init Redis
redis_url = os.getenv('REDIS_URL')
r = redis.from_url(redis_url, decode_responses = True, charset = 'UTF-8')


# Query channel information using channel_id
def get_channel(channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT secret, access_token FROM line_channel WHERE line_channel.channel_id = '%s' " % channel_id
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
    sql = "SELECT exists(SELECT 1 FROM line_user WHERE user_id = '{user_id}' AND channel_id = '{channel_id}' )"
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

    sql = "SELECT channel_id, user_id, name, gender, birth_day, birth_time, status \
    FROM line_user WHERE user_id = '{user_id}' \
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

    if not is_user(user_id, channel_id):
        sql = "INSERT INTO line_user \
                ( channel_id, user_id, name, gender, birth_day, birth_time, status ) \
                VALUES  ('{channel_id}','{user_id}','{user_name}','{user_gender}','{user_birth_day}','{user_birth_time}','{user_status}')"

    else:
        sql = "UPDATE line_user \
        SET name = '{user_name}', \
            gender = '{user_gender}', \
            birth_day = '{user_birth_day}', \
            birth_time = '{user_birth_time}', \
            status = '{user_status}' \
        WHERE user_id = '{user_id}' \
        AND channel_id = '{channel_id}'"

    sql = sql.format(channel_id = channel_id,
                     user_id = user_id,
                     user_name = user_name,
                     user_gender = user_gender,
                     user_birth_day = user_birth_day,
                     user_birth_time = user_birth_time,
                     user_status = user_status)

    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    app.logger.info("Insert user info: " + sql)
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()


# Get line message
# If find the message in redis, then simply return the message.
# But if not, query from DB and set them in redis. Then return the message.
def get_line_message(channel_id, context_id):

    message_id = channel_id + context_id

    if r.exists(channel_id+context_id):
        return r.get(message_id)
    else:
        refresh_line_message(channel_id)
        return r.get(message_id)


def refresh_line_message(channel_id):
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    sql = "SELECT context_id, message FROM line_message WHERE channel_id = '{channel_id}'"
    sql = sql.format(channel_id = channel_id)
    app.logger.warning("No message in Redis, start query: " + sql)
    cursor.execute(sql)
    results = cursor.fetchall()
    for result in results:
        context_id = result[0]
        message = result[1]
        r.set(channel_id + context_id, message)
    app.logger.info("Results: " + str(results))
    cursor.close()
    conn.close()