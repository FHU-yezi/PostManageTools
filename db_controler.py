import sqlite3

def InitDatabase(filename: str="data.db"):
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("""CREATE TABLE data
        (sorted_id INT    KEY    NOT NULL,
        pid              TEXT    NOT NULL,
        pslug            TEXT    NOT NULL,
        title            TEXT,
        content          TEXT    NOT NULL,
        likes_count      INT     NOT NULL,
        comments_count   TEXT    NOT NULL,
        is_topped        BOOL    NOT NULL,
        is_new           BOOL    NOT NULL,
        is_hot           BOOL    NOT NULL,
        is_most_valuable BOOL    NOT NULL,
        create_time      INT     NOT NULL,
        pictures         TEXT,
        nickname         TEXT    NOT NULL,
        uid              INT     NOT NULL,
        uslug            TEXT    NOT NULL,
        user_badge       TEXT,
        topic_name       TEXT,
        tid              INT,
        tslug            TEXT)""")
    db.commit()
    return db

def ConnectDatabase(filename: str="data.db"):
    db = sqlite3.connect(filename)
    return db


def AddDataList(db: object, data_list: list):
    for item in data_list:
        item["content"] = item["content"].replace("\n", "")
        item["content"] = item["content"].replace("\"", "'")
        cursor = db.cursor()
        columns_list = ["sorted_id", "pid", "pslug", "title", "content", "likes_count", "comments_count", 
                        "is_topped", "is_new", "is_hot", "is_most_valuable", "create_time", "pictures", 
                        "nickname", "uid", "uslug", "user_badge", "topic_name", "tid", "tslug"]
        sql_text = "INSERT INTO data ("
        for column in columns_list:
            try:
                sql_text += column + ","
            except KeyError:
                pass
        sql_text = sql_text.replace("tslug,", "tslug")
        sql_text += ") VALUES ("
        for column in columns_list:
            try:
                sql_text += "\"" + str(item[column]) + "\","
            except KeyError:
                sql_text += "\"" + "\","
        sql_text_list = list(sql_text)
        sql_text_list[-1] = ")"
        sql_text = "".join(sql_text_list)

        cursor.execute(sql_text)
    db.commit()

def EmptyDatabase(db: object):
    sql = "DELETE FROM data"
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()