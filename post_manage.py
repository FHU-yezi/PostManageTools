import datetime
import os
import time
from random import randint, random

import JianshuResearchTools as jrt
import streamlit as st

import config
from banword import banwords_list
from db_controler import *


def InitDB():
    db = ConnectDatabase("data.db")
    try:
        InitAllDataTable(db, "all_post_data")
    except sqlite3.OperationalError:  # 表已存在
        pass
    return db

@st.cache()
def GetNextSortedID(data):
    return data[-1]["sorted_id"]

@st.cache()
def comapre_time(source_time, time_limit):
    source_timestamp = time.mktime(source_time)
    source_date = datetime.date.fromtimestamp(source_timestamp)
    return source_date < time_limit


def GetData(island_url, db, table_name, time_limit):
    stop_flag = 0
    data_list = jrt.GetIslandPostList(island_url, count=10)  # 首次爬取
    next_sorted_id = GetNextSortedID(data_list)
    AddDataList(db, table_name, data_list)
    while True:
        data_list = jrt.GetIslandPostList(island_url, start_id=next_sorted_id, count=randint(100, 300))
        time.sleep(random())
        new_data_list = []
        for item in data_list:
            if comapre_time(item["create_time"], time_limit):
                new_data_list.append(item)
                stop_flag = 0
            else:
                stop_flag += 1  # 帖子不一定按照时间排序，有新评论会导致排序不同
        if data_list != []:
            next_sorted_id = GetNextSortedID(data_list)  # 用原列表获取 ID，防止序号混乱
            AddDataList(db, table_name, new_data_list)
        else:
            break
        if stop_flag >= 5:
            break
        
def MatchBanWordFromText(text, ban_words_list):
    matched_ban_words = []
    for ban_word in ban_words_list:
        if ban_word in text:
            matched_ban_words.append(ban_word)
    return matched_ban_words

def BanWordMatch(db):
    data = db.execute("SELECT * FROM all_post_data").fetchall()
    InitBanedDataTable(db, "ban_post_data")
    result = []
    for post in data:
        content = post[4]
        matched_ban_words = MatchBanWordFromText(content, banwords_list)
        keys_list = ["sorted_id", "pid", "pslug", "title", "content", "likes_count", "comments_count", 
                        "is_topped", "is_new", "is_hot", "is_most_valuable", "create_time", "pictures", 
                        "nickname", "uid", "uslug", "user_badge", "topic_name", "tid", "tslug"]
        new_post = {}
        zipped = zip(keys_list, post)
        for key, value in zipped:
            new_post[key] = value
        new_post["ban_words"] = " ".join(matched_ban_words)
        result.append(new_post)
    st.write(result)
    AddDataList(db, "ban_post_data", result)
    db.commit()
        

def main():
    if config.ISLAND_URL == None:
        st.error("未设置小岛链接")
        return
    db = InitDB()

    
    st.header("敏感词检测")
    with st.form("敏感词检测"):
        limit_time = st.date_input("时间限制", help="只会对时间在此之后的帖子进行敏感词检测")
        enable_ban_word_match = st.form_submit_button("开始检测")

    if enable_ban_word_match:
        flag = st.warning("正在获取数据，请稍后......")
        GetData(config.ISLAND_URL, db, "all_post_data", limit_time)
        flag = st.success("获取数据成功！")
        BanWordMatch(db)