import sqlite3


def ConnectDatabase(filename: str="data.db"):
    db = sqlite3.connect(filename)
    return db


def InitTable(db: object, table_name: str="data"):
    cursor = db.cursor()
    sql_text = "CREATE TABLE " + table_name + """
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
        tslug            TEXT)"""
    cursor.execute(sql_text)
    db.commit()


def EmptyTable(db: object, table_name: str):
    sql_text = "DELETE FROM " + table_name
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()


def DeleteTable(db: object, table_name: str):
    sql_text = "DROP TABLE " + table_name
    cursor = db.cursor()
    cursor.execute(sql_text)
    db.commit()


def AddDataList(db: object, table_name: str, data_list: list):
    for item in data_list:
        item["content"] = item["content"].replace("\n", "")
        item["content"] = item["content"].replace("'", "\"")
        # item["content"] = item["content"].replace("“", "'")
        # item["content"] = item["content"].replace("”", "'")
        item["pictures"] = ",".join(item["pictures"])
        cursor = db.cursor()
        columns_list = ["sorted_id", "pid", "pslug", "title", "content", "likes_count", "comments_count", 
                        "is_topped", "is_new", "is_hot", "is_most_valuable", "create_time", "pictures", 
                        "nickname", "uid", "uslug", "user_badge", "topic_name", "tid", "tslug"]
        sql_text = "INSERT INTO "+ table_name + " ("
        for column in columns_list:
            try:
                sql_text += column + ","
            except KeyError:
                pass
        sql_text = sql_text.replace("tslug,", "tslug")
        sql_text += ") VALUES ("
        for column in columns_list:
            try:
                sql_text += "\'" + str(item[column]) + "\',"
            except KeyError:
                sql_text += "\'" + "\',"
        sql_text_list = list(sql_text)
        sql_text_list[-1] = ")"
        sql_text = "".join(sql_text_list)
        cursor.execute(sql_text)
    db.commit()