import os

import streamlit as st

import config


def main():
    island_url = st.text_input("小岛链接")

    if "/g/" in island_url:
        st.success("小岛链接已保存")
        config.ISLAND_URL = island_url
    elif island_url == "":
        pass
    else:
        st.error("小岛链接无效")
        
    config.DEBUG_MODE = st.checkbox("开启调试模式", help="仅限开发人员调试使用")
    
    if config.DEBUG_MODE == True:
        delete_database = st.button("重置数据库")
        if delete_database == True:
            try:
                os.remove("data.db")
            except FileNotFoundError:
                st.warning("数据库文件不存在")
            else:
                st.success("已重置数据库")