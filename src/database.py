import pymysql
from log import logger
from dotenv import load_dotenv
import os


def get_secure_info():
    load_dotenv()
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_NAME = os.environ.get('DB_NAME')
    return DB_USERNAME, DB_PASSWORD, DB_NAME


def db_connection_test():
    logger.info(f"DB connection test")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                    SELECT * from user
                    '''
                cur.execute(sql)
        logger.info("DB connection success")
    except Exception as e:
        logger.error(e)


def set_key(chat_id, key_value):
    logger.info("set key")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO user(id, gptkey) VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chat_id, key_value))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE user SET gptkey=%s WHERE id=%s
                    '''
                    cur.execute(sql, (key_value, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_key(chat_id):
    logger.info("get key")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT gptkey from user WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['gptkey']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def set_weather_job_id(chat_id, key_value):
    logger.info("set weather_job_id")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO user(id, weather_job_id) VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chat_id, key_value))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE user SET weather_job_id=%s WHERE id=%s
                    '''
                    cur.execute(sql, (key_value, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_weather_job_id(chat_id):
    logger.info("get weather_job_id")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT weather_job_id from user WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['weather_job_id']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def set_weather_location(chat_id, weather_nx: str, weather_ny: str):
    logger.info("set weather_job_id")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO user(id, weather_nx, weather_ny) VALUES (%s, %s, %s)
                    '''
                    cur.execute(sql, (chat_id, weather_nx, weather_ny))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE user SET weather_nx=%s, weather_ny=%s WHERE id=%s
                    '''
                    cur.execute(sql, (weather_nx, weather_ny, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_weather_location(chat_id):
    logger.info("get weather_job_id")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT weather_nx, weather_ny from user WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['weather_nx'], results[0]['weather_ny']
                except IndexError:
                    return None, None
    except Exception as e:
        logger.error(e)


def set_weather_noti_time(chat_id, weather_noti_time: str):
    logger.info("set weather_noti_time")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO user(id, weather_noti_time) VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chat_id, weather_noti_time))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE user SET weather_noti_time=%s WHERE id=%s
                    '''
                    cur.execute(sql, (weather_noti_time, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_weather_noti_time(chat_id):
    logger.info("get weather_noti_time")
    DB_USERNAME, DB_PASSWORD, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host='127.0.0.1', user=DB_USERNAME, password=DB_PASSWORD,
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT weather_noti_time from user WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['weather_noti_time']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)