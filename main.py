import streamlit as st

import settings
import welcome
import config
import post_manage

st.set_page_config(page_title="简书小岛管理平台", layout="wide")

SubPageList = ["欢迎", "仪表盘", "帖子管理", "用户管理", "舆情监测", "设置"]

st.title("简书小岛管理平台")

active_page = st.sidebar.selectbox("页面", SubPageList)

def DebugModeWarning():
    if config.DEBUG_MODE == True:
        debug_warning = st.warning("调试模式已启用")

if active_page == "欢迎":
    DebugModeWarning()
    welcome.main()
elif active_page =="仪表盘":
    DebugModeWarning()
    pass
elif active_page =="帖子管理":
    DebugModeWarning()
    post_manage.main()
elif active_page =="用户管理":
    DebugModeWarning()
    pass
elif active_page =="舆情监测":
    DebugModeWarning()
    pass
elif active_page =="设置":
    settings.main()