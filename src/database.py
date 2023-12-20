import pymysql
from functools import wraps
from log import logger
from dotenv import load_dotenv
import os


def db_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        load_dotenv()
        DB_HOST = os.environ.get('DB_HOST')
        DB_USERNAME = os.environ.get('DB_USERNAME')
        DB_PASSWORD = os.environ.get('DB_PASSWORD')
        DB_PORT = os.environ.get('DB_PORT')
        DB_NAME = os.environ.get('DB_NAME')
        try:
            with pymysql.connect(host=DB_HOST, user=DB_USERNAME, password=DB_PASSWORD, port=int(DB_PORT),
                                 db=DB_NAME, charset="utf8", cursorclass=pymysql.cursors.DictCursor) as conn:
                with conn.cursor() as cur:
                    return func(cur, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return None

    return wrapper


@db_connection
def db_test(cur):
    logger.info(f"DB connection test")
    sql = '''
        SELECT * 
        FROM user
        '''
    cur.execute(sql)
    logger.info("DB connection success")


@db_connection
def start_chat(cur, chat_id):
    logger.info("start chat")
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
        cur.connection.commit()
        logger.info(f"{chat_id} INSERT success")
    else:
        logger.info(f"{chat_id} Already exist")


@db_connection
def set_gpt_key(cur, chat_id, key_value):
    logger.info("set key")
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
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_gpt_key(cur, chat_id):
    logger.info("get key")
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


@db_connection
def set_weather_location(cur, chat_id, weather_nx: int, weather_ny: int):
    logger.info("set weather_job_id")
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
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_weather_location(cur, chat_id):
    logger.info("get weather_location")
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


@db_connection
def get_weather_noti_id(cur, time):
    logger.info("get weather time")
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


@db_connection
def set_weather_noti_time(cur, chatid, time):
    logger.info("set wtime")
    sql = '''
    UPDATE weather 
    SET noti_time=%s 
    WHERE id=%s
    '''
    cur.execute(sql, (time, chatid))
    cur.connection.commit()
    logger.info("UPDATE weather noti time success")


@db_connection
def set_alarm(cur, chatid, time):
    logger.info("set alarm")
    sql = '''
    INSERT INTO alarm(id, atime, chatid) 
    VALUES (%s, %s, %s)
    '''
    cur.execute(sql, (f"A{chatid}{time.replace(':', '')}", time, chatid))
    cur.connection.commit()
    logger.info("INSERT success")


@db_connection
def get_alarm(cur, chatid):
    logger.info("get alarm")
    sql = '''
    SELECT id, atime 
    FROM alarm 
    WHERE chatid=%s
    '''
    cur.execute(sql, chatid)
    results = cur.fetchall()
    return results


@db_connection
def get_alarm_by_time(cur, time):
    logger.info("get alarm")
    sql = '''
    SELECT chatid 
    FROM alarm 
    WHERE atime=%s
    '''
    cur.execute(sql, time)
    results = cur.fetchall()
    return results


@db_connection
def remove_alarm(cur, id):
    logger.info(f"delete alarm {id}")
    sql = '''
    DELETE 
    FROM alarm 
    WHERE id=%s
    '''
    cur.execute(sql, id)
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def remove_all_alarm(cur, chatid):
    logger.info(f"delete alarm {chatid}")
    sql = '''
    DELETE 
    FROM alarm 
    WHERE chatid=%s
    '''
    cur.execute(sql, chatid)
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def set_boj_handle(cur, chatid, handle):
    logger.info(f"set boj handle {chatid}")
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
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_boj_handle(cur, chatid):
    logger.info(f"get boj handle {chatid}")
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


@db_connection
def set_boj_noti_time(cur, chatid, noti_time):
    logger.info(f"set boj noti time {chatid} {noti_time}")
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
    cur.connection.commit()
    logger.info("commit success")


@db_connection
def get_boj_noti_time(cur, chatid):
    logger.info(f"get boj noti time {chatid}")
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


@db_connection
def get_boj_noti_id(cur, time):
    logger.info(f"get boj noti id {time}")
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
