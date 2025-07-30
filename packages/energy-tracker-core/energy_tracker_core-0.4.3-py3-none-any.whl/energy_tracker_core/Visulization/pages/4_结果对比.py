import streamlit as st
import pandas as pd
import numpy as np
from energy_tracker_core.Visulization.workspace_task import WorkSpace, Task
from scipy import interpolate

# 页面配置
st.set_page_config(
    page_title="结果对比",
    page_icon="📊",
    layout="wide"
)

st.title("📊 任务结果对比")
ws: WorkSpace = None
ws = st.session_state.get("workspace", None)

# 辅助函数：对数据进行插值处理
def interpolate_data(data_series, target_length):
    """
    对数据序列进行插值，使其长度达到目标长度
    """
    # 原始数据的索引
    orig_indices = np.arange(len(data_series))
    # 目标索引
    target_indices = np.linspace(0, len(data_series) - 1, target_length)
    # 创建插值函数
    if len(data_series) > 1:
        f = interpolate.interp1d(orig_indices, data_series, kind='linear')
        # 执行插值
        interpolated_data = f(target_indices)
        return interpolated_data
    else:
        # 如果只有一个数据点，无法进行插值，则复制该值
        return np.full(target_length, data_series.iloc[0])

# 检查前序工作
if 'workspace' not in st.session_state:
    st.warning("请先在 CSV 管理页面初始化工作目录。")
else:
    if 'edited_task_showframe' not in st.session_state:
        st.warning("请先在 CSV 管理页面至少选择两个要对比的csv文件。")
    else:
        # 获取所有选中的任务名称
        selected_mask = st.session_state.edited_task_showframe['is_selected'] == True
        selected_names = st.session_state.edited_task_showframe[selected_mask]['name'].tolist()
        
        if len(selected_names) < 2:
            st.warning("请至少选择两个任务进行对比。")
        else:
            # 获取对应的任务对象
            selected_tasks = [ws.get_task_by_name(name) for name in selected_names]
            
            # 确保所有任务都分析过
            for task in selected_tasks:
                if not hasattr(task, 'statistics') or not task.statistics:
                    task.analyse()
            
            # 创建对比数据
            comparison_data = {}
            for task in selected_tasks:
                task_name = task.basic_info['name']
                
                # 收集基本统计数据用于对比
                comparison_data[task_name] = {
                    '问答总数': task.statistics['问答总数'],
                    '总持续时间(秒)': task.statistics['总持续时间(秒)'],
                    '正确率': task.statistics['正确率'],
                    '平均每次问答时间(秒)': task.statistics['平均每次问答时间(秒)'],
                    'CPU总能耗(Wh)': task.statistics['CPU总能耗(Wh)'],
                    'GPU总能耗(Wh)': task.statistics['GPU总能耗(Wh)'],
                    '总能耗(Wh)': task.statistics['总能耗(Wh)'],
                    'CPU平均每次问答能耗(Wh)': task.statistics['CPU平均每次问答能耗(Wh)'],
                    'GPU平均每次问答能耗(Wh)': task.statistics['GPU平均每次问答能耗(Wh)'],
                    '平均每次问答总能耗(Wh)': task.statistics['平均每次问答总能耗(Wh)'],
                    'CPU平均功率(W)': task.statistics['CPU平均功率(W)'],
                    'GPU平均功率(W)': task.statistics['GPU平均功率(W)'],
                    '总平均功率(W)': task.statistics['总平均功率(W)'],
                }

            # 转换为DataFrame便于绘图
            comparison_df = pd.DataFrame(comparison_data).T
            
            # 提供不同对比维度的选择
            st.markdown("### 选择对比维度")
            comparison_tabs = st.tabs(["基本指标", "能耗对比", "功率对比", "组合对比"])
            
            with comparison_tabs[0]:
                st.markdown("#### 基本指标对比")
                basic_metrics = ['问答总数', '总持续时间(秒)', '正确率', '平均每次问答时间(秒)']
                selected_basic_metrics = st.multiselect(
                    "选择要对比的基本指标", 
                    basic_metrics,
                    default=['问答总数', '正确率']
                )
                
                if selected_basic_metrics:
                    st.bar_chart(comparison_df[selected_basic_metrics])
            
            with comparison_tabs[1]:
                st.markdown("#### 能耗对比")
                energy_metrics = ['CPU总能耗(Wh)', 'GPU总能耗(Wh)', '总能耗(Wh)', 
                               'CPU平均每次问答能耗(Wh)', 'GPU平均每次问答能耗(Wh)', '平均每次问答总能耗(Wh)']
                selected_energy_metrics = st.multiselect(
                    "选择要对比的能耗指标", 
                    energy_metrics,
                    default=['总能耗(Wh)', 'CPU总能耗(Wh)', 'GPU总能耗(Wh)']
                )
                
                if selected_energy_metrics:
                    # 绘制能耗对比图
                    st.bar_chart(comparison_df[selected_energy_metrics])
                    
                    # 提供数据表格查看
                    with st.expander("查看详细数据"):
                        st.dataframe(comparison_df[selected_energy_metrics])
            
            with comparison_tabs[2]:
                st.markdown("#### 功率对比")
                power_metrics = ['CPU平均功率(W)', 'GPU平均功率(W)', '总平均功率(W)']
                selected_power_metrics = st.multiselect(
                    "选择要对比的功率指标", 
                    power_metrics,
                    default=power_metrics
                )
                
                if selected_power_metrics:
                    # 绘制功率对比图
                    st.bar_chart(comparison_df[selected_power_metrics])
                    
                    # 提供数据表格查看
                    with st.expander("查看详细数据"):
                        st.dataframe(comparison_df[selected_power_metrics])
            
            with comparison_tabs[3]:
                st.markdown("#### 自定义组合对比")
                all_metrics = basic_metrics + energy_metrics + power_metrics
                custom_metrics = st.multiselect(
                    "选择要对比的指标", 
                    all_metrics,
                    default=['总能耗(Wh)', '总平均功率(W)', '正确率']
                )
                
                chart_type = st.radio("选择图表类型", ["柱状图", "折线图"], horizontal=True)
                
                if custom_metrics:
                    if chart_type == "柱状图":
                        st.bar_chart(comparison_df[custom_metrics])
                    else:
                        st.line_chart(comparison_df[custom_metrics])
                    
                    # 提供数据表格查看
                    with st.expander("查看详细数据"):
                        st.dataframe(comparison_df[custom_metrics])
            
            # 高级对比：时间序列叠加对比
            st.markdown("### 能耗趋势对比")
            trend_tabs = st.tabs(["累计能耗趋势", "单次能耗分布", "实时功率变化"])
            
            with trend_tabs[0]:
                st.markdown("#### 累计能耗趋势对比")
                
                # 设置所有任务统一的标准化点数（100点足够展示趋势）
                standard_points = 100
                normalize_method = st.radio(
                    "标准化方法",
                    ["百分比进度", "插值到相同点数"],
                    horizontal=True,
                    help="百分比进度：按任务进度百分比对齐；插值到相同点数：将所有任务重采样到相同点数"
                )
                
                # 创建一个DataFrame存储所有任务的累计能耗
                energy_trend_data = pd.DataFrame()
                
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    # 计算累计能耗
                    total_cumsum = task.data['total_incremental_energy'].cumsum()
                    
                    if normalize_method == "百分比进度":
                        # 创建百分比进度索引
                        progress_pct = np.linspace(0, 100, len(total_cumsum))
                        # 添加到DataFrame
                        task_df = pd.DataFrame({task_name: total_cumsum.values}, index=progress_pct)
                        energy_trend_data = pd.concat([energy_trend_data, task_df], axis=1)
                    else:
                        # 对累计能耗数据进行插值，使所有任务具有相同点数
                        interpolated_cumsum = interpolate_data(total_cumsum, standard_points)
                        # 使用统一的索引添加到DataFrame
                        if energy_trend_data.empty:
                            energy_trend_data = pd.DataFrame(index=range(standard_points))
                        energy_trend_data[task_name] = interpolated_cumsum
                
                # 绘制累计能耗对比图
                st.line_chart(energy_trend_data)
                
                with st.expander("查看图表说明"):
                    if normalize_method == "百分比进度":
                        st.markdown("""
                        **累计能耗趋势对比说明：**
                        - X轴代表任务进度百分比，从0%到100%
                        - Y轴代表累计能耗，单位为Wh
                        - 每条线代表一个选中的任务
                        - 斜率越大的部分，表示该阶段能耗增长越快
                        """)
                    else:
                        st.markdown("""
                        **累计能耗趋势对比说明：**
                        - X轴代表标准化的数据点序号（通过插值将不同长度的任务调整为相同点数）
                        - Y轴代表累计能耗，单位为Wh
                        - 每条线代表一个选中的任务
                        - 斜率越大的部分，表示该阶段能耗增长越快
                        - 通过插值处理，可以直接比较不同长度任务的趋势
                        """)
            
            with trend_tabs[1]:
                st.markdown("#### 单次能耗分布对比")
                
                # 单次能耗分布的标准化设置
                st.write("##### 数据标准化设置")
                energy_normalize_method = st.radio(
                    "选择标准化方法",
                    ["保持原始点数", "插值到最大点数", "插值到固定点数"],
                    horizontal=True
                )
                
                if energy_normalize_method == "插值到固定点数":
                    fixed_points = st.slider("设置标准化点数", min_value=10, max_value=500, value=100, step=10)
                
                # 为每个任务准备单次能耗数据
                energy_distribution_data = pd.DataFrame()
                
                # 确定目标点数
                if energy_normalize_method == "插值到最大点数":
                    target_points = max([len(task.data) for task in selected_tasks])
                elif energy_normalize_method == "插值到固定点数":
                    target_points = fixed_points
                
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    # 获取单次能耗数据
                    single_energy = task.data['total_incremental_energy']
                    
                    if energy_normalize_method == "保持原始点数":
                        # 重置索引为问答序号
                        single_energy = single_energy.reset_index(drop=True)
                        # 添加到DataFrame
                        energy_distribution_data[task_name] = single_energy
                    else:
                        # 对单次能耗数据进行插值
                        interpolated_energy = interpolate_data(single_energy, target_points)
                        # 使用统一的索引添加到DataFrame
                        if energy_distribution_data.empty:
                            energy_distribution_data = pd.DataFrame(index=range(target_points))
                        energy_distribution_data[task_name] = interpolated_energy
                
                # 使用折线图展示分布趋势
                st.line_chart(energy_distribution_data)
                
                # 创建分布摘要数据
                distribution_summary = pd.DataFrame({
                    '任务': [],
                    '最小值': [],
                    '25%分位数': [],
                    '中位数': [],
                    '75%分位数': [],
                    '最大值': [],
                    '平均值': [],
                    '标准差': []
                })
                
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    energy_stats = task.data['total_incremental_energy'].describe()
                    
                    new_row = pd.DataFrame({
                        '任务': [task_name],
                        '最小值': [energy_stats['min']],
                        '25%分位数': [energy_stats['25%']],
                        '中位数': [energy_stats['50%']],
                        '75%分位数': [energy_stats['75%']],
                        '最大值': [energy_stats['max']],
                        '平均值': [energy_stats['mean']],
                        '标准差': [energy_stats['std']]
                    })
                    
                    distribution_summary = pd.concat([distribution_summary, new_row])
                
                # 显示分布统计摘要
                st.markdown("##### 能耗分布统计摘要")
                st.dataframe(distribution_summary)
                
                with st.expander("查看图表说明"):
                    if energy_normalize_method == "保持原始点数":
                        st.markdown("""
                        **单次能耗分布对比说明：**
                        - X轴代表问答序号
                        - Y轴代表单次能耗，单位为Wh
                        - 每条线代表一个选中的任务
                        - 注意：各任务行数不同，直接比较时要考虑这一点
                        - 统计摘要表格提供了各任务能耗分布的关键统计指标
                        """)
                    else:
                        st.markdown("""
                        **单次能耗分布对比说明：**
                        - X轴代表标准化后的问答序号
                        - Y轴代表单次能耗，单位为Wh
                        - 每条线代表一个选中的任务
                        - 通过插值处理，所有任务具有相同的点数，便于直接比较
                        - 统计摘要表格提供了各任务能耗分布的关键统计指标（基于原始数据）
                        """)
                     
            with trend_tabs[2]:
                st.markdown("#### 实时功率变化对比")
                
                # 功率变化的标准化设置
                power_normalize_method = st.radio(
                    "功率对比标准化方法",
                    ["百分比进度", "插值到相同点数"],
                    horizontal=True
                )
                
                if power_normalize_method == "插值到相同点数":
                    power_points = st.slider("功率对比标准化点数", min_value=10, max_value=500, value=100, step=10)
                
                # 计算并绘制实时功率变化
                power_trend_data = pd.DataFrame()
                
                for task in selected_tasks:
                    task_name = task.basic_info['name']
                    # 计算时间间隔（秒）
                    task.data['start_time'] = pd.to_datetime(task.data['start_time'])
                    task.data['end_time'] = pd.to_datetime(task.data['end_time'])
                    task.data['duration'] = (task.data['end_time'] - task.data['start_time']).dt.total_seconds()
                    
                    # 计算实时功率 (W = J/s, 能耗单位为Wh，需要转换为W)
                    # 功率 = 能耗(Wh) * 3600 / 持续时间(s)
                    task.data['power'] = task.data['total_incremental_energy'] * 3600 / task.data['duration']
                    
                    if power_normalize_method == "百分比进度":
                        # 创建百分比进度索引
                        progress_pct = np.linspace(0, 100, len(task.data))
                        # 添加到DataFrame
                        task_df = pd.DataFrame({task_name: task.data['power'].values}, index=progress_pct)
                        power_trend_data = pd.concat([power_trend_data, task_df], axis=1)
                    else:
                        # 对功率数据进行插值
                        interpolated_power = interpolate_data(task.data['power'], power_points)
                        # 使用统一的索引添加到DataFrame
                        if power_trend_data.empty:
                            power_trend_data = pd.DataFrame(index=range(power_points))
                        power_trend_data[task_name] = interpolated_power
                
                # 绘制实时功率对比图
                st.line_chart(power_trend_data)
                
                with st.expander("查看图表说明"):
                    if power_normalize_method == "百分比进度":
                        st.markdown("""
                        **实时功率变化对比说明：**
                        - X轴代表任务进度百分比，从0%到100%
                        - Y轴代表实时功率，单位为W (瓦特)
                        - 每条线代表一个选中的任务
                        - 峰值表示该时刻能耗强度最高
                        """)
                    else:
                        st.markdown("""
                        **实时功率变化对比说明：**
                        - X轴代表标准化后的数据点序号
                        - Y轴代表实时功率，单位为W (瓦特)
                        - 每条线代表一个选中的任务
                        - 通过插值处理，所有任务具有相同的点数，便于直接比较
                        - 峰值表示该时刻能耗强度最高
                        """)

# 重置激活页
st.session_state.current_page_index = 4
