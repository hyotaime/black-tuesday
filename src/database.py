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
                    SELECT * 
                    FROM user
                    '''
                cur.execute(sql)
        logger.info("DB connection success")
    except Exception as e:
        logger.error(e)


def start_chat(chat_id):
    logger.info("start chat")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                    SELECT id
                    FROM user
                    WHERE id=%s
                    '''
                cur.execute(sql, chat_id)
                results = cur.fetchall()
                if len(results) == 0:
                    sql = '''
                        INSERT INTO user(id)
                        VALUES (%s)
                        '''
                    cur.execute(sql, chat_id)
                    conn.commit()
                    logger.info(f"{chat_id} INSERT success")
                else:
                    logger.info(f"{chat_id} Already exist")
    except Exception as e:
        logger.error(e)


def set_key(chat_id, key_value):
    logger.info("set key")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                sql = '''
                UPDATE user 
                SET gptkey=%s 
                WHERE id=%s
                '''
                cur.execute(sql, (key_value, chat_id))
                logger.info("UPDATE gptkey success")
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
                    SELECT gptkey 
                    FROM user 
                    WHERE id=%s
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
                sql = '''
                UPDATE user 
                SET w_nx=%s, w_ny=%s 
                WHERE id=%s
                '''
                cur.execute(sql, (weather_nx, weather_ny, chat_id))
                logger.info("UPDATE location success")
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
                    SELECT w_nx, w_ny 
                    FROM user 
                    WHERE id=%s
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
                    SELECT id 
                    FROM user 
                    WHERE w_time=%s
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
                sql = '''
                UPDATE user 
                SET w_time=%s 
                WHERE id=%s
                '''
                cur.execute(sql, (time, chatid))
                logger.info("UPDATE weather noti time success")
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
                INSERT INTO alarm(id, atime, chatid) 
                VALUES (%s, %s, %s)
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
                SELECT id, atime 
                FROM alarm 
                WHERE chatid=%s
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
                SELECT chatid 
                FROM alarm 
                WHERE atime=%s
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
                DELETE 
                FROM alarm 
                WHERE id=%s
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
                DELETE 
                FROM alarm 
                WHERE chatid=%s
                '''
                cur.execute(sql, chatid)
            conn.commit()
    except Exception as e:
        logger.error(e)
