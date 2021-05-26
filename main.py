import streamlit as st

import settings
import welcome
import config

SubPageList = ["欢迎", "仪表盘", "帖子管理", "用户管理", "舆情监测", "设置"]

st.title("简书小岛管理平台")

active_page = st.sidebar.selectbox("页面", SubPageList)

if active_page == "欢迎":
    welcome.main()
elif active_page =="仪表盘":
    pass
elif active_page =="帖子管理":
    pass
elif active_page =="用户管理":
    pass
elif active_page =="舆情监测":
    pass
elif active_page =="设置":
    settings.main()