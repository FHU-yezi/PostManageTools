import sqlite3


def ConnectDatabase(filename: str="data.db"):
    db = sqlite3.connect(filename)
    return db


def InitAllDataTable(db: object, table_name: str="data"):
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


def InitBanedDataTable(db: object, table_name: str="data"):
    cursor = db.cursor()
    sql_text = "CREATE TABLE " + table_name + """
        (sorted_id INT    KEY    NOT NULL,
        pid              TEXT    NOT NULL,
        pslug            TEXT    NOT NULL,
        ban_words        TEXT,
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
        item["pictures"] = ",".join(item["pictures"])
        
        keys_text = ""
        values_text = ""
        for key, value in item.items():
            keys_text += key + ","
            values_text += "\'" + str(value) + "\',"
        keys_text = keys_text.strip(",")
        values_text = values_text.strip(",")
        sql_text = "INSERT INTO " + table_name + " (" + keys_text \
                    + ") VALUES (" + values_text + ")"
        db.execute(sql_text)
    db.commit()