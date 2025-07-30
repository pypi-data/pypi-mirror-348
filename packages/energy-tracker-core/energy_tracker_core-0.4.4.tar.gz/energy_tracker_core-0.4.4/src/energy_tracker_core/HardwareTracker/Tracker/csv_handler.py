"""
本模块提供能耗日志记录功能。
"""

# 标准库
import csv
import datetime
import os
from energy_tracker_core.GlobalConfig import *
from energy_tracker_core.HardwareTracker.CommandLineInterface import logger, console, StageAdapter

class CSV_Handler:
    """
    提供一个持久化CSV日志记录器，用于记录能耗数据。
    """

    def __init__(self, filename: str=datetime.datetime.now().strftime("%Y%m%d_%H%M%S")):
        """
        初始化日志记录器，并保持文件对象和 writer 对象长期有效
        """

        question_answer_list = []
        self.filename = filename
        # 固定列
        self.fixed_columns = [
            'start_time',
            'end_time',
            'cpu_name',
            'gpu_name',
            'cpu_incremental_energy',
            'gpu_incremental_energy',
            'total_incremental_energy',
            'question',
            'answer',
            'is_correct',
            'is_valid'
        ]

        csv_file_path = os.path.join(DATA_DIR, self.filename + '.csv')
        self.file = open(csv_file_path, mode='w', newline='', encoding='utf-8')
        self.writer = csv.DictWriter(self.file, fieldnames=self.fixed_columns)
        self.writer.writeheader()
        self.file.flush()  # 立即写入表头

    def log_ligne(self, start_time: datetime.datetime, end_time: datetime.datetime, cpu_name: str, gpu_name: str, cpu_incremental_energy: float,
            gpu_incremental_energy: float, total_incremental_energy: float, question: str = 'NULL', answer: str = 'NULL', is_correct: bool = False, is_valid: bool = False):
        """
        写入一条日志记录


        """
        # 构造一行日志记录
        row = {
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'cpu_name': cpu_name,
            'gpu_name': gpu_name,
            'cpu_incremental_energy': cpu_incremental_energy,
            'gpu_incremental_energy': gpu_incremental_energy,
            'total_incremental_energy': total_incremental_energy,
            'question': question,
            'answer': answer,
            'is_correct': is_correct,
            'is_valid': is_valid
        }

        self.writer.writerow(row)
        self.file.flush()  # 及时刷新写入的数据

    def close(self):
        """关闭文件对象，结束日志记录"""
        self.file.close()

