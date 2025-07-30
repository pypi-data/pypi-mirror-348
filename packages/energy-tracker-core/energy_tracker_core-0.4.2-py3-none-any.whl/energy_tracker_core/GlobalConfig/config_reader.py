from pathlib import Path
from pydantic import BaseModel, Field
from typing import Optional

class EnergyTrackerConfig(BaseModel):
    
    enable_cpu_power_monitor: bool = True
    use_actual_cpu_power: bool = True
    enable_gpu_power_monitor: bool = True
    use_actual_gpu_power: bool = True
    measurement_interval: float = 3.0
    cpu_power_bias: float = 0.0
    cpu_power_coefficient: float = 1.0
    gpu_power_bias: float = 0.0
    gpu_power_coefficient: float = 1.0



class GlobalConfig(BaseModel):
    energy_tracker_config: EnergyTrackerConfig

def load_config(path: Optional[Path | str] = None) -> GlobalConfig:
    # 自动定位项目根下的 config/config.json
    if path == None:
        # 从当前目录开始向上搜索，直到找到同级目录中有config目录
        current_path = Path(__file__).resolve().parent
        while current_path.parent != current_path:  # 防止到达根目录还未找到
            # 检查当前目录同级是否有config目录
            config_dir = current_path.parent / "config"
            if config_dir.exists() and config_dir.is_dir():
                break
            current_path = current_path.parent
        
        if current_path.parent == current_path:  # 到达根目录仍未找到
            raise FileNotFoundError("无法找到包含config目录的项目根目录")
            
        project_root = current_path.parent
        print(f"找到项目根目录: {project_root}")
        path = project_root / "config" / "config.json"
    with open(path) as f:
        return GlobalConfig.model_validate_json(f.read())

class PathSettings:
    def __init__(self):
        # 项目根目录
        # 自下而上搜索同级目录中带有config文件夹的父目录作为项目包目录
        current_path = Path(__file__).resolve().parent
        while current_path.parent != current_path:  # 防止到达根目录还未找到
            # 检查当前目录同级是否有config目录
            config_dir = current_path.parent / "config"
            if config_dir.exists() and config_dir.is_dir():
                self.package_root = current_path.parent
                break
            current_path = current_path.parent
        
        if current_path.parent == current_path:  # 到达根目录仍未找到
            # 如果找不到，回退到默认值
            self.package_root = Path(__file__).resolve().parents[3]

        # 各功能目录，默认基于 project_root 生成
        self.data_dir = self.package_root / "data"
        self.config_dir = self.package_root / "config"

# 全局单例，其他模块直接 `from your_package.paths import PATHS` 使用
PATHS = PathSettings()

# 测试用例
if __name__ == "__main__":
    # 测试配置文件加载
    config = load_config()
    print("能源追踪配置:")
    print(f"  启用CPU监控: {config.energy_tracker_config.enable_cpu_power_monitor}")
    print(f"  启用GPU监控: {config.energy_tracker_config.enable_gpu_power_monitor}")
    
    # 测试路径设置
    paths = PathSettings()
    print("\n路径设置:")
    print(f"  项目包目录: {paths.package_root}")
    print(f"  配置目录: {paths.config_dir}")
    print(f"  资源目录: {paths.resources_dir}")
    print(f"  数据目录: {paths.data_dir}")

