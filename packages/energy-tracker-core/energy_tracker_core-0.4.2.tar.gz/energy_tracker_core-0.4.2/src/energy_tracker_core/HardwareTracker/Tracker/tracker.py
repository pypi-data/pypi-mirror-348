"""
本模块提供能耗测量和计算以及日志持久化的类。
"""

# 标准库
import datetime
from typing import Generator, Optional
# 自定义库
from energy_tracker_core.HardwareTracker.Tracker import power_monitor
from energy_tracker_core.HardwareTracker.CommandLineInterface import console, logger, StageAdapter
from energy_tracker_core.GlobalConfig import *
from energy_tracker_core.HardwareTracker.Tracker.csv_handler import CSV_Handler
from energy_tracker_core.HardwareTracker.Tracker.power_monitor import CPU_Power_Monitor, GPU_Power_Monitor
class InferenceRecord:
    """
    推理记录类，负责记录单次推理过程中的能耗信息。
    """

    def __init__(self, token: str, cpu_name: str, gpu_name: str):
        self.token = token
        self.cpu_name = cpu_name
        self.gpu_name = gpu_name
    
    def start(self, question, cpu_accumulated_energy_start, gpu_accumulated_energy_start):
        self.start_time = datetime.datetime.now()
        self.question = question
        self.cpu_accumulated_energy_start = cpu_accumulated_energy_start
        self.gpu_accumulated_energy_start = gpu_accumulated_energy_start
        self.total_accumulated_energy_start = cpu_accumulated_energy_start + gpu_accumulated_energy_start
    
    def stop(self, answer, is_correct, is_valid, cpu_accumulated_energy_end, gpu_accumulated_energy_end):
        self.end_time = datetime.datetime.now()
        self.answer = answer
        self.is_correct = is_correct
        self.is_valid = is_valid
        self.cpu_accumulated_energy_end = cpu_accumulated_energy_end
        self.gpu_accumulated_energy_end = gpu_accumulated_energy_end
        self.total_accumulated_energy_end = cpu_accumulated_energy_end + gpu_accumulated_energy_end

    def dump_to_csv(self, csv_handler: CSV_Handler):
        """
        将推理记录写入CSV文件。
        """

        csv_handler.log_ligne(self.start_time, self.end_time, self.cpu_name, self.gpu_name, self.cpu_accumulated_energy_end - self.cpu_accumulated_energy_start, self.gpu_accumulated_energy_end - self.gpu_accumulated_energy_start, self.total_accumulated_energy_end - self.total_accumulated_energy_start, self.question, self.answer, self.is_correct, self.is_valid)

class Tracker:
    """
    能耗测量服务主体，负责异步执行能耗测量任务和响应任务。
    """

    def __init__(self, csv_handler: CSV_Handler=CSV_Handler()):
        self.logger = StageAdapter(logger, {"stage": "Tracker"})
        self.cpu_monitor: Optional[CPU_Power_Monitor] = None
        self.gpu_monitor: Optional[GPU_Power_Monitor] = None
        self.cpu_name = 'Default CPU'   
        self.gpu_name = 'Default GPU'
        if ENABLE_CPU_MONITOR:
            self.cpu_monitor = power_monitor.CPU_Power_Monitor()
            self.cpu_name = self.cpu_monitor.name
        if ENABLE_GPU_MONITOR:
            self.gpu_monitor = power_monitor.GPU_Power_Monitor()
            self.gpu_name = self.gpu_monitor.name

        self.cpu_accumulated_energy: float = 0
        self.gpu_accumulated_energy: float = 0
        self.inference_records_list: dict[str, InferenceRecord] = {}
        self.csv_handler = csv_handler

    def start(self, period:float=5):
        """
        启动能耗测量任务。
        """ 

        self.period = datetime.timedelta(seconds=period)
        self.start_time = datetime.datetime.now()
        self.last_measurement_time = self.start_time
        self.time_generator = self._time_generator()

    def _time_generator(self) -> Generator[datetime.datetime, None, None]:
        expected_next_time = datetime.datetime.now() + self.period
        while True:
            yield expected_next_time
            expected_next_time += self.period

    def do_measurements(self):
        """
        执行一次能耗测量。
        """

        period = datetime.datetime.now() - self.last_measurement_time
        self.last_measurement_time = datetime.datetime.now()
        period = period.total_seconds()
        if self.cpu_monitor is not None:
            append_cpu_energy = self.cpu_monitor.mesure_power()*period/3600
            self.cpu_accumulated_energy += append_cpu_energy
            self.logger.debug(f"CPU能耗追加{append_cpu_energy}Wh")
        if self.gpu_monitor is not None:
            append_gpu_energy = self.gpu_monitor.mesure_power()*period/3600
            self.gpu_accumulated_energy += append_gpu_energy
            self.logger.debug(f"GPU能耗追加{append_gpu_energy}Wh")

    def start_inference_record(self, token: str, question: str):
        """
        开始一次推理记录。
        """
        self.inference_records_list[token] = InferenceRecord(token, self.cpu_name, self.gpu_name)
        self.inference_records_list[token].start(question, self.cpu_accumulated_energy, self.gpu_accumulated_energy)

    def stop_inference_record(self, token: str, answer: str, is_correct: bool, is_valid: bool):
        """
        结束一次推理记录。
        """
        self.inference_records_list[token].stop(answer, is_correct, is_valid, self.cpu_accumulated_energy, self.gpu_accumulated_energy)
        self.inference_records_list[token].dump_to_csv(self.csv_handler)
        del self.inference_records_list[token]

    def stop(self):
        """
        资源回收。
        """
        self.csv_handler.close()
            

 