import streamlit as st
from pathlib import Path
from energy_tracker_core.Visulization.workspace_task import WorkSpace
import time
import pandas as pd

# 页面配置
st.set_page_config(
    page_title="CSV 文件管理",
    page_icon="📂",
    layout="wide"
)


st.title("📂 CSV 文件管理")
st.markdown("### 工作目录")


# 输入并确认 workspace 目录
col1, col2, col3 = st.columns([12, 1, 1], vertical_alignment="bottom")
with col1:
    dir_input = st.text_input(
        "请输入包含 CSV 文件的工作目录绝对路径", value=st.session_state.get("workspace_dirpath", ""),
        help="日志文件默认放在项目根目录的log文件夹下",
        label_visibility='visible'
    )
with col2:
    confirm_click = st.button("确认", help='确认新路径',key="confirm_dir",use_container_width=True)

with col3:
    update_click = st.button("更新", help='重新扫描当前路径',key="rescan_dir",use_container_width=True)

if confirm_click:
    try:
        ws = WorkSpace(dir_input)
        ws.scan()
        st.session_state.workspace = ws
        st.success("Workspace 初始化成功，已扫描目录中的 CSV 文件。")
    except Exception as e:
        st.error(f"初始化失败：{e}")
if update_click:
    if "workspace" in st.session_state:
        ws = st.session_state.workspace
        try:
            ws.scan()
            st.success("Workspace 更新成功，已重新扫描目录中的 CSV 文件。")
        except Exception as e:
            st.error(f"更新失败：{e}")
    else:
        st.warning("请先初始化 Workspace。")
    
# 如果已初始化 workspace，则展示文件列表和基本信息
if "workspace" in st.session_state:
    if st.session_state.current_page_index != 2:
        st.session_state.current_page_index = 2
        st.session_state.workspace.task_showframe = st.session_state.edited_task_showframe.copy()
        st.rerun()
    with st.form(key="file_selection_form"):
        st.session_state.edited_task_showframe = st.data_editor(st.session_state.workspace.task_showframe)
        is_submitted = st.form_submit_button(label="提交",use_container_width=True)
    if is_submitted:
        st.success("已提交选择")
    
    
# 重置激活页
st.session_state.current_page_index = 2