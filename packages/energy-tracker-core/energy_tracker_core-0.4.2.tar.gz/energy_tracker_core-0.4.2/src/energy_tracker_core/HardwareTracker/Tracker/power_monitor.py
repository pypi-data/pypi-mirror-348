"""
本模块用于提供检测物理机cpu和gpu功率的类。
"""

# 标准库
import logging
import time
from abc import ABC, abstractmethod
import sys
# 非标准库
import pynvml
import wmi
# 自定义库
from energy_tracker_core.HardwareTracker.CommandLineInterface import console, logger, StageAdapter
from energy_tracker_core.GlobalConfig import *
class BasePowerMonitor(ABC):
    """
    基础监测器类，提供监测器的基本功能。
    """

    @abstractmethod
    def mesure_power(self) -> float:
        """
        执行一次测量，获取当前功率。
        """
    
    # 测试测量功率所需时间，避免测量周期小于测量耗时，导致数据周期紊乱
    @abstractmethod
    def test_measurement_time(self) -> float:
        """
        测试测量功率所需时间。
        """

        pass

class CPU_Power_Monitor(BasePowerMonitor):
    """
    CPU 监测器类，继承自基础监测器类。
    根据OpenHardwareMonitorAPI获取CPU的当前功率和累计能耗。
    """
    def __init__(self):
        self.name: str = wmi.WMI().Win32_Processor()[0].Name
        self.cpu_logger = StageAdapter(logger, {"stage": "CPU monitor"})
        self.last_valid_power = 0.0

        if USE_ACTUAL_CPU_POWER:
            self.initialize()
            self.cpu_logger.info(f"CPU能耗测量启用，将使用LibreHardwareMonitor获取实际功耗, 返回：{CPU_POWER_BIAS} + {CPU_POWER_COEFFICIENT} * 测得功率")
        else:
            self.cpu_logger.warning(f"CPU实际功耗测量被禁用，将返回设置值：{CPU_POWER_BIAS}")

    def initialize(self):
        """
        初始化监测器。
        """

        self.name: str = wmi.WMI().Win32_Processor()[0].Name
        self.wmi_obj = wmi.WMI(namespace="root\\LibreHardwareMonitor")
        # 确认能否通过wmi访问LibreHardwareMonitor的cpu数据。同时传感器名称
        # 可能的功率传感器访问字段

        sensor_name_list = ["CPU Package", "Package"]
        self.sensor_filed = None
        try:
            for sensor_name in sensor_name_list:
                query = f"SELECT Value FROM Sensor WHERE Name = '{sensor_name}' AND SensorType = 'Power'"
                sensor = self.wmi_obj.query(query)
                if not sensor:
                    continue
                self.sensor_filed = sensor_name
                self.is_exist = True
                self.cpu_logger.info(f"CPU监测器连接底层API成功，CPU名称为：{self.name}")
                time = self.test_measurement_time()
                self.cpu_logger.info(f"CPU监测器测量耗时：{time}秒")
                return
            raise Exception("CPU功率传感器未找到")
        except:
            self.cpu_logger.error("CPU_Monitor初始化失败，请确认LibreHardwareMonitor或WMI是否正常工作。")
            sys.exit(1)

    

    def mesure_power(self) -> float:
        """
        执行一次测量，获取CPU的当前功率（单位：瓦特）。
        """
        
        query = f"SELECT Value FROM Sensor WHERE Name = '{self.sensor_filed}' AND SensorType = 'Power'"
        
        try:
            sensor = self.wmi_obj.query(query)
            cpu_power_sensor = sensor[0]
            self.last_valid_power = cpu_power_sensor.Value
            self.cpu_logger.debug(f"GPU功耗测量值：{self.last_valid_power}W")
            return self.last_valid_power*CPU_POWER_COEFFICIENT + CPU_POWER_BIAS
        except:
            self.cpu_logger.error("测量失败，CPU监测器未找到,请确认LibreHardwareMonitor是否正常工作, 或检查功率传感器字段是否对应。")
            sys.exit(1)


    def test_measurement_time(self)->float:
        """
        测试测量功率所需时间。
        """

        start_time = time.time()
        self.mesure_power()
        end_time = time.time()
        return end_time - start_time
        
class GPU_Power_Monitor(BasePowerMonitor):
    """
    GPU 监测器类，继承自基础监测器类。
    根据nvml获取GPU的当前功率和累计能耗。
    """

    def __init__(self):
        self.name = "GPU Name"
        self.last_valid_power = 0.0
        self.gpu_logger = StageAdapter(logger, {"stage": "GPU monitor"})

        if USE_ACTUAL_GPU_POWER:
            self.initialize()
            self.gpu_logger.info(f"GPU实际功耗测量启用, 将使用nvml获取实际功耗, 将返回：{GPU_POWER_BIAS} + {GPU_POWER_COEFFICIENT} * 测得功率")
        else:
            self.gpu_logger.warning(f"GPU实际功耗测量被禁用，将返回设置值：{GPU_POWER_BIAS}")
        
        

    def initialize(self):
        """
        接通底层硬件api
        """

        # 测量失败次数
        self.error_count = 0
        # 测量失败容错次数阈值
        self.error_tolerance = 5
        try:
            pynvml.nvmlInit()
            self.name = pynvml.nvmlDeviceGetName(pynvml.nvmlDeviceGetHandleByIndex(0))
            self.handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            self.gpu_logger.info(f"GPU监测器连接底层API成功，GPU名称为：{self.name}")
            time = self.test_measurement_time()
            self.gpu_logger.info(f"GPU监测器测量耗时：{time}秒")
        except:
            self.gpu_logger.error("GPU_Monitor底层API初始化失败，不能正常访问Nvidia GPU，服务失败")
            sys.exit(1)

    def mesure_power(self):
        try:
            power = pynvml.nvmlDeviceGetPowerUsage(self.handle)
            self.last_valid_power = power / 1000.0  # 转换为瓦特并保存最后有效值
            self.gpu_logger.debug(f"GPU功耗测量值：{self.last_valid_power}W")
            if self.error_count > 0:
                self.gpu_logger.warning(f"GPU进行了一次有效测量，重置错误次数")
                self.error_count = 0
            return self.last_valid_power*GPU_POWER_COEFFICIENT + GPU_POWER_BIAS
        
        except pynvml.NVMLError as e:
            self.error_count += 1
            if self.error_count >= self.error_tolerance:
                self.gpu_logger.error(f"GPU功耗测量错误次数超过阈值，测量终止。")
                sys.exit(1)
            self.gpu_logger.warning(f"GPU功耗测量失败，但没有超过阈值，返回上次有效值")
            return getattr(self, 'last_valid_power', 0.0)*GPU_POWER_COEFFICIENT + GPU_POWER_BIAS

    def test_measurement_time(self)->float:
        """
        测试测量功率所需时间。
        """

        start_time = time.time()
        self.mesure_power()
        end_time = time.time()
        return end_time - start_time

if __name__ == "__main__":
    # 测试本模块能否正常测量能耗

    cpu_monitor = CPU_Power_Monitor()
    gpu_monitor = GPU_Power_Monitor()
    
    for i in range(10):
        print(f"CPU power: {cpu_monitor.mesure_power()}")
        print(f"GPU power: {gpu_monitor.mesure_power()}")
        time.sleep(1)
