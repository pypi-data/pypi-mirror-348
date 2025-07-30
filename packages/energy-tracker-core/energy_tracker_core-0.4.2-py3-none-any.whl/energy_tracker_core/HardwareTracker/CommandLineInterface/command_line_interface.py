"""
使用rich结合原生logging实现命令行界面。
"""

import logging
from rich.console import Console
from rich.logging import RichHandler
import time
# ——1. 创建全局 Console（可自定义主题）
console = Console()

# ——2. 配置 RichHandler：对齐 level（8 列），显示时间，不显示文件路径
handler = RichHandler(
    console=console,
    show_time=True,
    log_time_format="%b %d %a %H:%M:%S",
    show_path=False     # 不要默认的 filename:lineno
)

# ——3. 基础 Logging 配置，只用 RichHandler
logging.basicConfig(
    level="DEBUG",
    format="%(message)s",  # 由 RichHandler 负责输出时间、级别等前缀
    handlers=[handler]
)
logger = logging.getLogger("app")

# ——4. 自定义 Adapter：注入“stage”到消息前，无对齐
class StageAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        stage = self.extra.get("stage")
        if stage:
            msg = f"[{stage}] {msg}"
        return msg, kwargs

# ——5. 演示：在不同阶段记录日志
if __name__ == "__main__":
    init_log = StageAdapter(logger, {"stage": "INIT"})
    proc_log = StageAdapter(logger, {"stage": "PROCESS"})
    finish_log = StageAdapter(logger, {"stage": "FINISH"})

    proc_log.debug("Connecting to database")
    proc_log.info("Processing data")
    finish_log.warning("Low disk space")
    finish_log.error("Failed to write output")
    time.sleep(1)
    init_log.info("Loading configuration")
    proc_log.debug("Connecting to database")
    proc_log.info("Processing data")
    finish_log.warning("Low disk space")
    finish_log.error("Failed to write output")
