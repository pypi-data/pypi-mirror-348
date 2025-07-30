from aiohttp import web
import asyncio
import datetime
import logging

from energy_tracker_core.HardwareTracker.CommandLineInterface import console, logger, StageAdapter
from energy_tracker_core.HardwareTracker.Tracker.tracker import Tracker


# 设置asyncio的日志级别为WARNING，只显示错误信息，避免日志格式混乱
logging.getLogger('asyncio').setLevel(logging.ERROR)

# 设置aiohttp的日志级别为ERROR，只显示错误信息，避免日志格式混乱
logging.getLogger('aiohttp').setLevel(logging.ERROR)
logging.getLogger('aiohttp.access').setLevel(logging.ERROR)
logging.getLogger('aiohttp.client').setLevel(logging.ERROR)
logging.getLogger('aiohttp.internal').setLevel(logging.ERROR)
logging.getLogger('aiohttp.server').setLevel(logging.ERROR)
logging.getLogger('aiohttp.web').setLevel(logging.ERROR)
logging.getLogger('aiohttp.websocket').setLevel(logging.ERROR)

# 创建不同阶段的日志适配器
server_log = StageAdapter(logger, {"stage": "服务信息"})
request_log = StageAdapter(logger, {"stage": "请求处理"})
auto_mesure_log = StageAdapter(logger, {"stage": "自动能耗测量"})

# 创建日志中间件
@web.middleware
async def log_middleware(request: web.Request, handler):
    # 记录请求开始时间
    start_time = datetime.datetime.now()
    # 记录请求信息，包括header
    headers_info = {k: v for k, v in request.headers.items()}
    if request.body_exists:
        body_info = await request.text()
    else:
        body_info = ""
    request_log.debug(f"收到请求: {request.method} {request.path} {headers_info} {body_info}")
    
    try:
        # 处理请求
        response = await handler(request)
        
        # 记录响应信息
        process_time = (datetime.datetime.now() - start_time).total_seconds()
        request_log.debug(f"请求处理完成: {request.method} {request.path} - 状态码: {response.status} - 处理时间: {process_time:.3f}秒")
        
        return response
    except Exception as e:
        # 记录错误信息
        request_log.error(f"请求处理出错: {request.method} {request.path} - 错误: {str(e)}")
        raise

async def hd_post_start_inference(request: web.Request):
    # 读取Token
    token = request.headers.get('Token', '')
    request_log.info(f"能耗追踪任务开始，Token: {token}")
    data = await request.post()
    tracker.start_inference_record(token, str(data['question']))
    return web.json_response({"status": "success"})

async def hd_post_stop_inference(request: web.Request):
    # 读取Token
    token = request.headers.get('Token', '')
    request_log.info(f"能耗追踪任务结束，Token: {token}")
    
    data = await request.post()       
    tracker.stop_inference_record(
        token, 
        str(data['answer']), 
        data['is_correct'].lower() == 'true', 
        data['is_valid'].lower() == 'true'
    )
    return web.json_response({"status": "success"})

async def periodic_task():
    while True:
        tracker.do_measurements()
        waited_time = (next(tracker.time_generator) - datetime.datetime.now()).total_seconds()
        while waited_time < 0:
            waited_time = (next(tracker.time_generator) - datetime.datetime.now()).total_seconds()
        await asyncio.sleep(waited_time)

async def start_background_tasks(app: web.Application):
    # 创建后台任务
    app['periodic_task'] = asyncio.create_task(periodic_task())
    server_log.info("后台能耗测量任务已启动")

async def cleanup_background_tasks(app: web.Application):
    # 清理后台任务
    app['periodic_task'].cancel()
    await app['periodic_task']
    server_log.info("后台能耗测量任务已清理")


# 创建能耗追踪器
tracker = Tracker()
tracker.start()

# 创建应用
app = web.Application()

# 添加中间件
app.middlewares.append(log_middleware)

# 添加路由
app.add_routes([web.post('/start_inference', hd_post_start_inference),
                web.post('/stop_inference', hd_post_stop_inference)])

# 添加启动和清理后台任务的处理函数
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)


if __name__ == '__main__':
    server_log.info("异步服务器启动中...")
    web.run_app(app, host='127.0.0.1', port=8000)
    
