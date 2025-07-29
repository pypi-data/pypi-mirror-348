# -*- coding: utf-8 -*-
import os
from fastapi.exceptions import RequestValidationError
from uvicorn import Config, Server

from .exceptions.exception import HTTPException, CustomException
from fastapi import FastAPI,Request,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .._result import OperateResult, CamelCaseUtil
from .._logger import logger


class BaseFastApp:
    def __init__(self,router_path:str=""):
        self.router_path = router_path
        """将属性名称app暴露出去，方便在其它地方引用"""
        self.app = self.create_app()

    '''加载所有路由，此处约定所有的接口文件放在routers目录下'''

    def load_all_router(self):
        router_list = []
        if self.router_path:
            for root, dirs, files in os.walk(self.router_path):
                if not os.path.isdir(root):
                    continue
                if self.in_ignore_dir(root):
                    continue
                for file in files:
                    if "router" in file:
                        router_list.append(os.path.join(root, file))
        return router_list

    @staticmethod
    def in_ignore_dir(root):
        ignore_flag = False
        ignore_dir = ("__pycache__")
        root_split = root.split(os.sep)
        for sub_dir in root_split:
            if sub_dir in ignore_dir:
                ignore_flag = True
                break
        return ignore_flag

    '''获取所有已加载的路由信息，用于权限控制或其它用途'''

    @staticmethod
    def get_all_router(app):
        router_list = app.routes
        for router in router_list:
            item = router.__dict__
            path = item['path']

    '''Header方法中的三个点表示参数为必填项 None表示选填项'''

    def create_app(self):
        """初始化FastAPI对象，并注入全局依赖"""
        openapi_url = "/openapi.json"
        app = FastAPI(
            title="生成服务",  # swagger标题
            default_response_class=ApiResultResponse,
            openapi_url=openapi_url,
        )
        # 添加中间件
        # app.add_middleware(LoginMiddleware)
        """允许跨域的url列表，可以是IP，也可以是域名"""
        origins = ["*"]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"]
        )
        @app.get("/actuator/health")
        async def actuator_health():
            return {"status": "UP"}


        routers = self.load_all_router()
        for file in routers:
            file_name = os.path.splitext(os.path.basename(file))[0]
            dir_name = os.path.dirname(file).replace("/", ".").replace("\\", ".")
            # 动态导入模块
            router_module = __import__(f"{dir_name}.{file_name}", fromlist=["router"])
            router = getattr(router_module, "router", None)
            if router:
                app.include_router(router)

        @app.exception_handler(RequestValidationError)
        def validation_exception_handler(request: Request, exc: RequestValidationError):
            msg = ["{}: {} ({})".format("->".join(error.get("loc", "")), error.get("msg", ""), error.get("type", "")) for
                       error in
                       exc.errors()]
            '''发生请求验证异常时（比如请求参数缺失或参数类型错误），接口数据的返回格式'''
            response = JSONResponse({
                "code": status.HTTP_400_BAD_REQUEST,  # 状态码
                "body": exc.body,  # 请求的参数
                "msg": msg  # 错误信息提示
            })
            return response
        @app.exception_handler(HTTPException)
        def custom_exception_handler(request: Request, exc: HTTPException):
            """发生一般异常时（比如业务处理错误），接口数据的返回格式"""
            '''code 和 msg 为 CustomException 自定义类中的属性'''
            response = JSONResponse({
                "code": exc.status_code,
                "msg": exc.detail
            })
            return response

        @app.exception_handler(CustomException)
        def custom_exception_handler(request: Request, exc: CustomException):
            """发生一般异常时（比如业务处理错误），接口数据的返回格式"""
            '''code 和 msg 为 CustomException 自定义类中的属性'''
            response = JSONResponse({
                "code": exc.code,
                "msg": exc.message
            })
            return response

        @app.exception_handler(Exception)
        async def all_exception_handler(request: Request, exc: Exception):
            response = JSONResponse({
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(exc)
            })
            return response
        return app


class ApiResultResponse(JSONResponse):
    """fastapi 自定义响应类"""

    def render(self, content: any) -> bytes:
        if "application/json" in self.media_type:
            msg = "success"
            code = 1
            if content is None:
                code = 5
                msg = 'data null'
                data = None
            elif isinstance(content, OperateResult):
                data = CamelCaseUtil.transform(content.data) if content.data and isinstance(content.data,
                                                                                            dict) or isinstance(
                    content.data, list) else content.data
                msg = content.msg
                code = content.code
            elif isinstance(content, dict):
                code = content.get("code", None)
                msg = content.get("msg", None)
                data = CamelCaseUtil.transform(content.get("data", None)) if content.get("data", None) and isinstance(
                    content.get("data", None), dict) or isinstance(content.get("data", None), list) else content.get(
                    "data", None)
                if not code and not msg and not data:
                    code = 1
                    msg = "success"
                    data = content
            else:
                data = content
            result = OperateResult(code=code, message=msg, data=data)
            content = result.dumps()
        return super().render(content)

def start_app_server(app:FastAPI,host="0.0.0.0", port=5000):
    logger.log("启动api")
    config = Config(app, host=host, port=port, workers=16, access_log=False, backlog=2048)
    config.timeout_keep_alive = 60  # 设置 timeout_keep_alive 值
    server = Server(config)
    logger.init_config()
    server.run()