import os
import sys
from collections import ChainMap

from . import information as f_information
from .helperFunctions_expansion import helperFunctions
from .helperFunctions_expansion import multithreading

from .information import error as file_error
from . import helperFunctions_expansion
from .multithreading_fileMapping import fileMapping_func
from . import pluginLoading
from .information import fileMappingConfig
from . import string
from . import register

Application: f_information.FilemappingDict = f_information.application


class File(f_information.File):
    """
    callObject
        - 调用对象
    invoke
        - 内行参数
    returnValue
        - 返回参数
    public
        - 公共
    information
        - 信息
    logs
        - 日志
    """
    callObject = f_information.callObject
    invoke = f_information.invoke
    returnValue = f_information.returnValue
    public = f_information.public
    information = f_information.information
    logs = f_information.logs

    path = None

    def __init__(self,
                 absolutePath: os.path,
                 screening=None,
                 config: dict = None,
                 printLog: bool = False,
                 printPosition=sys.stdout
                 ):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件
        :param config: 配置文件 它将会被映射到 public['config']
        :param printLog: 是否打印日志
        :param printPosition: 日志输出位置 默认为 sys.stdout 在终端输出
        """
        """
        设计思路
        
        1. 遍历文件夹下的所有文件
        2. 筛选出符合要求的文件
        3. 加载配置文件
        4. 加载映射文件 
            - 多线程 & 异步
        5. 运行映射文件
            - 多线程 & 异步
        """
        if screening is None:
            # 目前只支持py, 这里是为了以后做铺垫
            screening = ["py"]

        if self.__pathValidation__(absolutePath if isinstance(absolutePath, (list, tuple)) else [absolutePath]):
            raise FileNotFoundError(f"不是一个有效的绝对路径。: '{absolutePath}'")

        if isinstance(absolutePath, str):
            # 为了兼容 File 多个路径
            absolutePath = [absolutePath]

        # 加载配置文件
        self.public["config"] = helperFunctions.deep_update(helperFunctions.configConvertTodict(f_information.config),
                                                            config) \
            if config else helperFunctions.configConvertTodict(f_information.config)

        self.printLog = printLog
        self.printPosition = printPosition
        self.path = absolutePath
        self.lordPath = absolutePath[0]
        # self.lordPath = absolutePath[0] if isinstance(absolutePath, list) else absolutePath

        self.run_order = {}
        self.listOfFiles = {}
        fileMappingConfig.log['printPosition'] = self.printPosition
        fileMappingConfig.log['printLog'] = self.printLog
        self.listOfFiles = self.__dictMerge__(*[self.__fileFiltering__(i, screening) for i in absolutePath])
        # self.listOfFiles = self.__fileFiltering__(absolutePath, screening)
        if self.public.config.get('multithreading', False):
            self.multithreading = multithreading.enableMultithreading(
                self.public['config']['numberOfThreads']
            )
            self.__multithreading__()

        else:
            self.__singleThreaded__()
        # 使用应用参数
        helperFunctions_expansion.parameterApplication.ApplyParameter(self)

    def __run__(self, name, kwargs):
        """
        运行映射文件
        :return:
        """
        _ = self.returnValue[name] = self.callObject[name].run(**kwargs)
        if not isinstance(_, fileMappingConfig.error_list_a2):
            string.theRunFileWasSuccessful(name)

        else:
            string.theRunFileFailed(name, _)

    def runAll(self, **kwargs):
        """
        运行所有映射文件
        :return:
        """
        for key, data in self.run_order.items():
            for i in data:
                if self.callObject[i]:
                    self.__run__(i, kwargs)

    def runOne(self, name: str, **kwargs):
        """
        运行单个映射文件
        :return:
        """
        if self.callObject.get(name, False):
            self.__run__(name, kwargs)

        else:
            string.errorNoFile(name)

    def run(self, name: str = None, **kwargs):
        """
        计划在后续版本移除

        运行映射文件
        :return:
        """
        if name is None:
            for key, data in self.listOfFiles.items():
                if self.callObject[key]:
                    self.__run__(key, kwargs)

        else:
            if self.callObject.get(name, False):
                self.__run__(name, kwargs)

            else:
                string.errorNoFile(name)

    def __dictMerge__(self, *args: list[dict]) -> dict:
        """
        多个dict合并
        :param args: dict
        """
        return dict(ChainMap(*reversed(args)))  # 需要反转参数顺序

    def __fileFiltering__(self, cpath, screening):
        """
        文件筛选
        :param cpath: 路径
        :param screening: 文件
        """
        return {
            i.split('.')[0]: os.path.join(cpath, i)
            if os.path.isfile(os.path.join(cpath, i)) and i.split('.')[-1] in screening
            else os.path.join(cpath, i, fileMappingConfig.functionsName["__init__.py"])
            for i in os.listdir(cpath)
            if (os.path.isfile(os.path.join(cpath, i)))
               or (os.path.isdir(os.path.join(cpath, i))
                   and os.path.isfile(os.path.join(cpath, i, fileMappingConfig.functionsName["__init__.py"])))
        }

    def __pathValidation__(self, pathLit: list) -> bool:
        """
        路径验证
        :param pathLit: 路径 list
        """
        return False in [
            (os.path.isabs(i) or os.path.exists(i))
            for i in pathLit
        ]

    def __multithreading__(self):
        """
        多线程运行
        :return:
        """
        # 读取文件 & 文本解析 & 排序插件
        self.run_order = fileMapping_func.file_read(self.multithreading, self.listOfFiles)
        self.run_order = fileMapping_func.text_parsing(self.multithreading, self.run_order)
        self.run_order = helperFunctions_expansion.informationProcessing.sorting_plugin(self.run_order)
        if not isinstance(self.run_order, tuple):
            time_wrapper = register.TimeWrapper()
            info_wrapper = register.InfoWrapper(fileMappingConfig.functions)
            for __level__, L in self.run_order.items():
                data = fileMapping_func.file_import(self.multithreading, pluginLoading.f, L, self.listOfFiles,
                                                    wrapper_list=[time_wrapper.wrapper, info_wrapper.wrapper])
                self.callObject |= dict(zip(L, data))
                self.invoke |= dict(zip(L, [i.pack for i in data]))

            else:
                # 获取 时间 & 信息 -> information.run_time & file_info
                self.information["run_time"] = time_wrapper.data
                self.information["file_info"] = info_wrapper.data

        else:
            # sorting_plugin -> tuple 表示插件循环依赖
            self.logs = file_error.circularDependenciesError(self.logs, self.run_order)
            return False

    def __singleThreaded__(self):
        """
        单线程运行
        """
        # 读取文件 & 文本解析 & 排序插件
        self.run_order = {}
        for i in self.listOfFiles:
            with open(self.listOfFiles[i], "r", encoding="utf-8") as f:
                self.run_order[i] = helperFunctions_expansion.informationProcessing.get_all(f.read())

        self.information = {"file_info": self.run_order, "run_time": {}}
        self.run_order = helperFunctions_expansion.informationProcessing.sorting_plugin(self.run_order)
        if not isinstance(self.run_order, tuple):
            time_wrapper = register.TimeWrapper()
            info_wrapper = register.InfoWrapper(fileMappingConfig.functions)
            for __level__, L in self.run_order.items():
                for name in L:
                    pluginLoading.f.__name__ = name
                    self.callObject[name] = info_wrapper.wrapper(time_wrapper.wrapper(pluginLoading.f))(
                        self.listOfFiles[name])
                    self.invoke[name] = self.callObject[name].pack

            else:
                # 获取 时间 & 信息 -> information.run_time & file_info
                self.information["run_time"] = time_wrapper.data
                self.information["file_info"] = info_wrapper.data

        # sorting_plugin -> tuple 表示插件循环依赖
        else:
            file_error.circularDependenciesError(self.logs, self.run_order)
            return False
