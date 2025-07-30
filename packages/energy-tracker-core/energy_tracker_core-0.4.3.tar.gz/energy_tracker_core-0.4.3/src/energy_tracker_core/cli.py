import click
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.console import Console
import time

@click.group()
def cli():
    """能源追踪器命令行工具

    这个工具可以用来启动异步服务和可视化界面。
    """
    pass

@cli.command('server')
@click.option('--host', default='127.0.0.1', help='服务器主机地址')
@click.option('--port', default=8000, type=int, help='服务器端口')
def start_server(host, port):
    """启动硬件监控异步服务。

    这个服务会收集CPU和GPU的能耗数据。
    """
    from energy_tracker_core.HardwareTracker.AsyncService.async_server import app
    from aiohttp import web
    
    console = Console()
    click.echo(f"正在启动异步服务器，地址：{host}，端口：{port}")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]服务器启动中...", total=100)
        
        # 模拟启动过程
        for i in range(100):
            time.sleep(0.02)  # 添加小延迟使进度条可见
            progress.update(task, advance=1)
            
            # 在特定进度点显示额外信息
            if i == 30:
                progress.print("[yellow]正在初始化硬件监控...")
            elif i == 60:
                progress.print("[yellow]正在配置数据收集器...")
            elif i == 90:
                progress.print("[yellow]正在启动异步服务...")
    
    console.print("[green]服务器启动完成！[/green]")
    web.run_app(app, host=host, port=port)

@cli.command('viz')
def start_visualization():
    """启动Streamlit可视化界面。

    这个界面用于展示能耗数据的图表和统计信息。
    """
    import streamlit.web.cli as stcli
    import sys
    from pathlib import Path
    
    click.echo("正在启动可视化界面...")
    
    # 获取app.py的路径
    app_path = Path(__file__).parent / "Visulization" / "app.py"
    
    # 使用streamlit CLI来运行应用
    sys.argv = ["streamlit", "run", str(app_path), "--server.headless", "true"]
    stcli.main()

@cli.command('info')
def system_info():
    """显示系统硬件信息。

    包括CPU、GPU等硬件的详细信息和当前状态。
    """
    click.echo("正在收集系统硬件信息...")
    try:
        import platform
        import wmi
        import pynvml
        
        # 初始化WMI和NVML
        w = wmi.WMI()
        pynvml.nvmlInit()
        
        # 获取系统信息
        system_name = platform.system()
        system_version = platform.version()
        
        # 获取CPU信息
        cpu_info = w.Win32_Processor()[0]
        cpu_name = cpu_info.Name
        cpu_cores = cpu_info.NumberOfCores
        
        # 获取GPU信息
        device_count = pynvml.nvmlDeviceGetCount()
        gpu_info = []
        
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)
            name = pynvml.nvmlDeviceGetName(handle)
            gpu_info.append(name)
        
        # 输出信息
        click.echo(f"系统: {system_name} {system_version}")
        click.echo(f"CPU: {cpu_name} ({cpu_cores}核)")
        click.echo("GPU:")
        for i, gpu in enumerate(gpu_info):
            click.echo(f"  [{i}] {gpu}")
            
        pynvml.nvmlShutdown()
    except Exception as e:
        click.echo(f"获取系统信息失败: {str(e)}")
        click.echo("请确保安装了所有必要的依赖并且有适当的权限。")

if __name__ == '__main__':
    cli()
