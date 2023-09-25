import pymysql
from log import logger
from dotenv import load_dotenv
import os


def get_secure_info():
    load_dotenv()
    DB_HOST = os.environ.get('DB_HOST')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_PORT = os.environ.get('DB_PORT')
    DB_NAME = os.environ.get('DB_NAME')
    return DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME


def db_connection_test():
    logger.info(f"DB connection test")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                    SELECT * from botuser
                    '''
                cur.execute(sql)
        logger.info("DB connection success")
    except Exception as e:
        logger.error(e)


def set_key(chat_id, key_value):
    logger.info("set key")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO botuser(id, gptkey) VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chat_id, key_value))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE botuser SET gptkey=%s WHERE id=%s
                    '''
                    cur.execute(sql, (key_value, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_key(chat_id):
    logger.info("get key")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT gptkey from botuser WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['gptkey']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def set_weather_location(chat_id, weather_nx: str, weather_ny: str):
    logger.info("set weather_job_id")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO botuser(id, w_nx, w_ny) VALUES (%s, %s, %s)
                    '''
                    cur.execute(sql, (chat_id, weather_nx, weather_ny))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE botuser SET w_nx=%s, w_ny=%s WHERE id=%s
                    '''
                    cur.execute(sql, (weather_nx, weather_ny, chat_id))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_weather_location(chat_id):
    logger.info("get weather_location")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT w_nx, w_ny from botuser WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['w_nx'], results[0]['w_ny']
                except IndexError:
                    return None, None
    except Exception as e:
        logger.error(e)


def get_weather_noti_id(time):
    logger.info("get weather time")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT id from botuser WHERE w_time=%s
                    '''
                    cur.execute(sql, time)
                    results = cur.fetchall()
                    return results
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def set_weather_noti_time(chatid, time):
    logger.info("set wtime")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO botuser(id, w_time) VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chatid, time))
                    logger.info("INSERT success")
                except pymysql.err.MySQLError:
                    sql = '''
                    UPDATE botuser SET w_time=%s WHERE id=%s
                    '''
                    cur.execute(sql, (time, chatid))
                    logger.info("UPDATE success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def set_alarm(chatid, time):
    logger.info("set alarm")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                INSERT INTO btalarm(id, time, chatid) VALUES (%s, %s, %s)
                '''
                cur.execute(sql, (f"A{chatid}{time.replace(':', '')}", time, chatid))
                logger.info("INSERT success")
            conn.commit()
    except Exception as e:
        logger.error(e)


def get_alarm(chatid):
    logger.info("get alarm")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                SELECT id, time from btalarm WHERE chatid=%s
                '''
                cur.execute(sql, chatid)
                results = cur.fetchall()
                return results
    except Exception as e:
        logger.error(e)


def get_alarm_by_time(time):
    logger.info("get alarm")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                SELECT chatid from btalarm WHERE time=%s
                '''
                cur.execute(sql, time)
                results = cur.fetchall()
                return results
    except Exception as e:
        logger.error(e)


def remove_alarm(id):
    logger.info(f"delete alarm {id}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                DELETE FROM btalarm WHERE id=%s
                '''
                cur.execute(sql, id)
            conn.commit()
    except Exception as e:
        logger.error(e)


def remove_all_alarm(chatid):
    logger.info(f"delete alarm {chatid}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                DELETE FROM btalarm WHERE chatid=%s
                '''
                cur.execute(sql, chatid)
            conn.commit()
    except Exception as e:
        logger.error(e)
