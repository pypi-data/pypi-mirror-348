from __future__ import annotations
import os
from pathlib import Path
from dataclasses import dataclass, field
import pandas as pd
import numpy as np

@dataclass
class Task:
    """
    处理单个 CSV 文件的任务。
    属性:
        csv_filepath: str        # 初始化时必须提供
        basic_info: dict         # 扫描得到的基本信息字典，包括开始/结束时间、时长、行数和首条问题
        data: pd.DataFrame       # 加载后的 DataFrame（init=False，运行时赋值）
        statistics: dict         # 统计分析结果字典（init=False，运行时赋值）
    方法:
        scan, load, analyse
    """

    csv_filepath: str
    basic_info: dict = field(default_factory=dict)
    data: pd.DataFrame = field(default=None, init=False)
    statistics: dict = field(default_factory=dict, init=False)

    def __post_init__(self) -> None:
        # 确保路径为绝对路径
        self.csv_filepath = str(Path(self.csv_filepath).absolute())

    def scan(self) -> None:
        """扫描 CSV 文件的核心信息：开始时间、结束时间、时长、行数和首条问题"""
        df = pd.read_csv(self.csv_filepath)
        if df.empty:
            raise ValueError(f"CSV 文件 {self.csv_filepath} 为空，无法扫描基本信息。")
        start = pd.to_datetime(df.iloc[0]['start_time'])
        end = pd.to_datetime(df.iloc[-1]['end_time'])
        duration = end - start
        capacity = len(df)
        first_question = df.iloc[0].get('question', 'None')
        self.basic_info = {
            'name': os.path.basename(self.csv_filepath),
            'start_time': start.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': end.strftime('%Y-%m-%d %H:%M:%S'),
            'duration': str(duration),
            'capacity': int(capacity),
            'first_question': first_question
        }

    def load(self) -> None:
        """将 CSV 文件加载为 DataFrame"""
        self.data = pd.read_csv(self.csv_filepath)

    def analyse(self, top_n: int = 3) -> None:
        """对 DataFrame 执行所需统计分析，包括累计能耗、功率计算和极值统计"""
        if self.data is None or self.data.empty:
            self.load()
        
        df = self.data.copy()
        total_count = int(df.shape[0])
        
        # 1. 计算每行的持续时间并累加
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds()
        total_duration_sec = float(df['duration'].sum())
        
        # 2. 累加能耗值
        total_cpu_energy = float(df['cpu_incremental_energy'].sum())
        total_gpu_energy = float(df['gpu_incremental_energy'].sum())
        total_energy = float(df['total_incremental_energy'].sum())
        
        # 3. 计算平均功率 (能量/时间)
        avg_cpu_power = float(total_cpu_energy*3600 / total_duration_sec) if total_duration_sec else 0.0
        avg_gpu_power = float(total_gpu_energy*3600 / total_duration_sec) if total_duration_sec else 0.0
        avg_total_power = float(total_energy*3600 / total_duration_sec) if total_duration_sec else 0.0
        
        # 平均每次问答的能耗
        avg_cpu_energy_per_q = float(total_cpu_energy / total_count) if total_count else 0.0
        avg_gpu_energy_per_q = float(total_gpu_energy / total_count) if total_count else 0.0
        avg_energy_per_q = float(total_energy / total_count) if total_count else 0.0
        
        # 4. 找到最大和最小值对应的行
        max_duration_row = df.loc[[df['duration'].idxmax()]]
        min_duration_row = df.loc[[df['duration'].idxmin()]]
        
        max_cpu_energy_row = df.loc[[df['cpu_incremental_energy'].idxmax()]]
        min_cpu_energy_row = df.loc[[df['cpu_incremental_energy'].idxmin()]]
        
        max_gpu_energy_row = df.loc[[df['gpu_incremental_energy'].idxmax()]]
        min_gpu_energy_row = df.loc[[df['gpu_incremental_energy'].idxmin()]]
        
        max_total_energy_row = df.loc[[df['total_incremental_energy'].idxmax()]]
        min_total_energy_row = df.loc[[df['total_incremental_energy'].idxmin()]]
        
        # 将最大/最小值行转换为numpy数组形式备用
        max_duration_array = np.array([max_duration_row['start_time'].iloc[0], max_duration_row['end_time'].iloc[0], 
                                      max_duration_row['duration'].iloc[0], max_duration_row['total_incremental_energy'].iloc[0]])
        min_duration_array = np.array([min_duration_row['start_time'].iloc[0], min_duration_row['end_time'].iloc[0], 
                                      min_duration_row['duration'].iloc[0], min_duration_row['total_incremental_energy'].iloc[0]])
        
        max_cpu_energy_array = np.array([max_cpu_energy_row['start_time'].iloc[0], max_cpu_energy_row['end_time'].iloc[0], 
                                        max_cpu_energy_row['cpu_incremental_energy'].iloc[0]])
        min_cpu_energy_array = np.array([min_cpu_energy_row['start_time'].iloc[0], min_cpu_energy_row['end_time'].iloc[0], 
                                        min_cpu_energy_row['cpu_incremental_energy'].iloc[0]])
        
        max_gpu_energy_array = np.array([max_gpu_energy_row['start_time'].iloc[0], max_gpu_energy_row['end_time'].iloc[0], 
                                        max_gpu_energy_row['gpu_incremental_energy'].iloc[0]])
        min_gpu_energy_array = np.array([min_gpu_energy_row['start_time'].iloc[0], min_gpu_energy_row['end_time'].iloc[0], 
                                        min_gpu_energy_row['gpu_incremental_energy'].iloc[0]])
        
        max_total_energy_array = np.array([max_total_energy_row['start_time'].iloc[0], max_total_energy_row['end_time'].iloc[0], 
                                          max_total_energy_row['total_incremental_energy'].iloc[0]])
        min_total_energy_array = np.array([min_total_energy_row['start_time'].iloc[0], min_total_energy_row['end_time'].iloc[0], 
                                          min_total_energy_row['total_incremental_energy'].iloc[0]])
        
        # 能耗最高/最低的 N 次问答
        highest_energy_qas = df.nlargest(top_n, 'total_incremental_energy').to_dict(orient='records')
        lowest_energy_qas = df.nsmallest(top_n, 'total_incremental_energy').to_dict(orient='records')
        
        # 正确率
        correct_rate = float(df['is_correct'].sum() / total_count) if total_count else 0.0
        # 更新统计信息
        self.statistics = {
            '问答总数': total_count,
            '总持续时间(秒)': total_duration_sec,
            '正确率': correct_rate,
            '平均每次问答时间(秒)': float(total_duration_sec / total_count) if total_count else 0.0,
            
            # 累计能耗数据 (Wh)
            'CPU总能耗(Wh)': total_cpu_energy,
            'GPU总能耗(Wh)': total_gpu_energy,
            '总能耗(Wh)': total_energy,
            
            # 平均每次问答能耗 (Wh)
            'CPU平均每次问答能耗(Wh)': avg_cpu_energy_per_q,
            'GPU平均每次问答能耗(Wh)': avg_gpu_energy_per_q,
            '平均每次问答总能耗(Wh)': avg_energy_per_q,
            
            # 功率数据 (W)
            'CPU平均功率(W)': avg_cpu_power,
            'GPU平均功率(W)': avg_gpu_power,
            '总平均功率(W)': avg_total_power,
            
            # 最大/最小值数组
            '最长持续时间数组': max_duration_array,
            '最短持续时间数组': min_duration_array,
            'CPU最大能耗数组': max_cpu_energy_array,
            'CPU最小能耗数组': min_cpu_energy_array,
            'GPU最大能耗数组': max_gpu_energy_array,
            'GPU最小能耗数组': min_gpu_energy_array,
            '最大总能耗数组': max_total_energy_array,
            '最小总能耗数组': min_total_energy_array,
            
            # 最值DataFrame
            '最长持续时间数据': max_duration_row,
            '最短持续时间数据': min_duration_row,
            'CPU最大能耗数据': max_cpu_energy_row,
            'CPU最小能耗数据': min_cpu_energy_row,
            'GPU最大能耗数据': max_gpu_energy_row,
            'GPU最小能耗数据': min_gpu_energy_row,
            '最大总能耗数据': max_total_energy_row,
            '最小总能耗数据': min_total_energy_row,
            
            # 极值记录
            '能耗最高问答': highest_energy_qas,
            '能耗最低问答': lowest_energy_qas
        }

@dataclass
class WorkSpace:
    """
    管理工作目录下的 CSV 文件，并生成对应 Task 列表。
    属性:
        workspace_dirpath: str       # 初始化时必须提供
        csvfile_list: list[str]      # 扫描时赋值（init=False）
        task_list: list[Task]        # scan 时初始化并赋值（init=False）
    方法:
        scan, analyse
    """
    workspace_dirpath: str
    csvfile_list: list[str] = field(default_factory=list, init=False)
    task_list: list[Task] = field(default_factory=list, init=False)
    task_showframe: pd.dataframe = field(default=None, init=False)

    def __post_init__(self) -> None:
        self.workspace_dirpath = str(Path(self.workspace_dirpath).absolute())

    def scan(self) -> None:
        """扫描目录下所有 CSV 文件，初始化 Task 并执行 scan"""
        if not os.path.isdir(self.workspace_dirpath):
            raise NotADirectoryError(f"{self.workspace_dirpath} 不是有效目录")
        self.csvfile_list = [f for f in os.listdir(self.workspace_dirpath) if f.lower().endswith('.csv')]
        self.task_list = []
        for fname in self.csvfile_list:
            path = os.path.join(self.workspace_dirpath, fname)
            task = Task(path)
            task.scan()
            self.task_list.append(task)
        # 生成任务描述 DataFrame
        self.task_showframe = pd.DataFrame([task.basic_info for task in self.task_list])
        self.task_showframe['is_selected'] = False

    def analyse(self, top_n: int = 3) -> None:
        """对所有 Task 执行 load 与 analyse"""
        if not self.task_list:
            self.scan()
        for task in self.task_list:
            task.load()
            task.analyse(top_n=top_n)

    def get_task_by_name(self, name: str) -> Task:
        """根据任务名称获取对应的 Task 对象"""
        for task in self.task_list:
            if task.basic_info['name'] == name:
                return task
        raise ValueError(f"未找到名称为 {name} 的任务")
    
# 示例用法
if __name__ == "__main__":
    ws = WorkSpace("D:\\3PI_2024\\EnergyTracker_Dev\\log")
    ws.scan()
    for t in ws.task_list:
        print(f"Basic info for {t.csv_filepath}: {t.basic_info}")
    ws.analyse(top_n=0)
    for t in ws.task_list:
        print(f"Statistics for {t.csv_filepath}: {t.statistics}")
