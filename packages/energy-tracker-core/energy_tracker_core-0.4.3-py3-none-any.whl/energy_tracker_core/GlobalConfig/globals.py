from .config_reader import PATHS, load_config
# 加载全局配置
CONFIG = load_config()
# 导出路径设置为全局变量
PACKAGE_ROOT = PATHS.package_root
DATA_DIR = PATHS.data_dir
CONFIG_DIR = PATHS.config_dir
# 导出能源追踪配置为全局变量
ENABLE_CPU_MONITOR = CONFIG.energy_tracker_config.enable_cpu_power_monitor
ENABLE_GPU_MONITOR = CONFIG.energy_tracker_config.enable_gpu_power_monitor
USE_ACTUAL_CPU_POWER = CONFIG.energy_tracker_config.use_actual_cpu_power
USE_ACTUAL_GPU_POWER = CONFIG.energy_tracker_config.use_actual_gpu_power
MEASUREMENT_INTERVAL = CONFIG.energy_tracker_config.measurement_interval
CPU_POWER_BIAS = CONFIG.energy_tracker_config.cpu_power_bias
CPU_POWER_COEFFICIENT = CONFIG.energy_tracker_config.cpu_power_coefficient
GPU_POWER_BIAS = CONFIG.energy_tracker_config.gpu_power_bias
GPU_POWER_COEFFICIENT = CONFIG.energy_tracker_config.gpu_power_coefficient
