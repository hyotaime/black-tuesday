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


def set_gpt_key(chat_id, key_value):
    logger.info("set key")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO gpt(id, gptkey)
                    VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chat_id, key_value))
                    logger.info("INSERT gptkey success")
                except Exception:
                    sql = '''
                    UPDATE gpt 
                    SET gptkey=%s 
                    WHERE id=%s
                    '''
                    cur.execute(sql, (key_value, chat_id))
                    logger.info("UPDATE gptkey success")
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_gpt_key(chat_id):
    logger.info("get key")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT gptkey 
                    FROM gpt 
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
                try:
                    sql = '''
                    INSERT INTO weather(id, nx, ny)
                    VALUES (%s, %s, %s)
                    '''
                    cur.execute(sql, (chat_id, weather_nx, weather_ny))
                    logger.info("INSERT location success")
                except Exception:
                    sql = '''
                    UPDATE weather
                    SET nx=%s, ny=%s
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
                    SELECT nx, ny 
                    FROM weather 
                    WHERE id=%s
                    '''
                    cur.execute(sql, chat_id)
                    results = cur.fetchall()
                    return results[0]['nx'], results[0]['ny']
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
                    FROM weather 
                    WHERE noti_time=%s
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
                UPDATE weather 
                SET noti_time=%s 
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


def set_boj_handle(chatid, handle):
    logger.info(f"set boj handle {chatid}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO boj(id, handle)
                    VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chatid, handle))
                except Exception:
                    sql = '''
                    UPDATE boj 
                    SET handle=%s 
                    WHERE id=%s
                    '''
                    cur.execute(sql, (handle, chatid))
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_boj_handle(chatid):
    logger.info(f"set boj handle {chatid}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT handle
                    FROM boj
                    WHERE id=%s
                    '''
                    cur.execute(sql, chatid)
                    results = cur.fetchall()
                    return results[0]['handle']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def set_boj_noti_time(chatid, noti_time):
    logger.info(f"set boj noti time {chatid} {noti_time}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                             db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    INSERT INTO boj(id, noti_time)
                    VALUES (%s, %s)
                    '''
                    cur.execute(sql, (chatid, noti_time))
                except Exception:
                    sql = '''
                    UPDATE boj 
                    SET noti_time=%s 
                    WHERE id=%s
                    '''
                    cur.execute(sql, (noti_time, chatid))
                conn.commit()
    except Exception as e:
        logger.error(e)


def get_boj_noti_time(chatid):
    logger.info(f"get boj noti time {chatid}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT), db=DB_NAME,
                             charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT noti_time
                    FROM boj
                    WHERE id=%s
                    '''
                    cur.execute(sql, chatid)
                    results = cur.fetchall()
                    return results[0]['noti_time']
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)


def get_boj_noti_id(time):
    logger.info(f"get boj noti id {time}")
    DB_HOST, DB_USERNAME, DB_PASSWORD, DB_PORT, DB_NAME = get_secure_info()
    try:
        with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT), db=DB_NAME,
                             charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
            with conn.cursor() as cur:
                try:
                    sql = '''
                    SELECT id
                    FROM boj
                    WHERE noti_time=%s
                    '''
                    cur.execute(sql, time)
                    results = cur.fetchall()
                    return results
                except IndexError:
                    return None
    except Exception as e:
        logger.error(e)
