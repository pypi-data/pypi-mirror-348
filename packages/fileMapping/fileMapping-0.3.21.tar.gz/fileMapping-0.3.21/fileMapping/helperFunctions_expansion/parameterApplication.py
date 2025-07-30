"""
参数的具体应用
fileMappingConfig.functions


"""
import atexit
import shutil
import functools
import os
import traceback
import types

from .. import information
from . import empty

registerData = {
    "list": [],
    "end_func": [],
    "logsFunc": ''
}


@atexit.register
def AppEnd():
    for i in registerData["end_func"]:
        func = i["func"]
        name = i["name"]
        try:
            func()
        except Exception as e:
            registerData["logsFunc"].fileMappingOutput(information.error.AppEnd(name, e, traceback.format_exc()))

        else:
            registerData["logsFunc"].fileMappingOutput(f"func: {name} ok!")


def ApplyParameter(self_info: information.File) -> bool:
    """
    应用参数

    规定如下
    类, 初始化时必须包含self_info参数
    可以有 init 和 end 方法, 用于初始化和结束
    """
    end_list = []
    registerData["logsFunc"] = self_info.logs

    for i in registerData["list"]:
        func = i(self_info)
        try:
            if hasattr(func, "init"):
                func.init()
        except Exception as e:
            self_info.logs.fileMappingOutput(information.error.AppInit(func, e, traceback.format_exc()))

        if hasattr(func, 'end'):
            end_list.append({
                "name": func.__ne__,
                "func": func.end
            })

    registerData["end_func"] = end_list
    return True


def wrapper(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        return func(*args, **kwargs)

    registerData["list"].append(wrapper_func)
    return func


@wrapper
class Framework:
    self_info: information.File
    def __init__(self, self_info: information.File): ...

    def init(self): ...

    def end(self): ...


@wrapper
class TemporaryFolders(Framework):
    def __init__(self, self_info: information.File):
        super().__init__(self_info)

        self.self_info = self_info
        self.temporaryFolders = True
        if not self_info.path in [False, True, None, '']:  # temporaryFolders 关闭
            self.path = os.path.join(self_info.lordPath, self_info.public.config['temporaryFolders'])

            self.information_temporaryFolders = self.self_info.information["temporaryFolders"] = {}  # 临时文件夹信息
            self.logs = self.self_info.logs["temporaryFolders"] = {"error": []}
            self.create_path = []
            self.init_tmp = False
            # 用于判断临时的文件夹是否自主创建，如果是的话则在结束时删除
            if not os.path.exists(self.path):
                os.mkdir(self.path)
                self.init_tmp = True

        else:
            self.temporaryFolders = False

    def __mkdir(self, temporaryFolders):
        path = os.path.join(self.path, temporaryFolders)
        try:
            if not os.path.exists(path):
                os.mkdir(path)
                self.create_path.append(path)

            self.information_temporaryFolders[temporaryFolders] = path
            return True

        except FileExistsError as e:
            self.logs["error"].append({path: e})
            return False

    def init(self):
        if not self.temporaryFolders:
            return False

        for key, value in self.self_info.information.file_info.items():
            temporaryFolders = value['__temporaryFolders__']
            if temporaryFolders is None:
                continue

            if isinstance(temporaryFolders, str):
                self.__mkdir(temporaryFolders)

            else:  # temporaryFolders is a list
                for folder in temporaryFolders:
                    self.__mkdir(folder)

    def end(self):
        for i in self.create_path:
            shutil.rmtree(i)

        if self.init_tmp:
            shutil.rmtree(self.path)


@wrapper
class DataFolders(Framework):
    def __init__(self, self_info: information.File):
        super().__init__(self_info)

        self.self_info = self_info
        self.dataFolders = True
        self.create_path = []
        self.rootPath = self_info.public.get("config", {}).get("rootPath", False)  # 根目录
        run = self_info.public.get("config", {}).get("dataFolder", False)
        if not ((self.rootPath is False) and (run is False)):
            # dataFolders 开启
            self.logs = self.self_info.logs["dataFolders"] = {"error": []}
            dataFolder_path = self_info.public.config["dataFolder"]
            self.information_dataFolders = self.self_info.information["dataFolders"] = {}  # 临时文件夹信息
            self.path = os.path.join(self.rootPath, dataFolder_path)
            if not os.path.exists(self.path):
                os.mkdir(self.path)  # 创建 dataFolder 目录

        else:
            self.dataFolders = False

    def __mkdir(self, file_path):
        path = os.path.join(self.path, file_path)
        try:
            if not os.path.exists(path):
                os.mkdir(path)
                self.create_path.append(path)

            self.information_dataFolders[file_path] = path
            return True

        except FileExistsError as e:
            self.logs["error"].append({path: e})
            return False

    def init(self):
        if not self.dataFolders:
            return False

        for key, value in self.self_info.information.file_info.items():
            dataFolders = value['__dataFolders__']
            if dataFolders is None:
                continue

            if isinstance(dataFolders, str):
                dataFolders = [dataFolders]

            for dataFolder in dataFolders:
                self.__mkdir(dataFolder)  # 创建 dataFolder 目录


@wrapper
class Function(Framework):
    def __init__(self, self_info: information.File):
        super().__init__(self_info)

        self.self_info = self_info

    def __empty__(self, key):
        self.self_info.callObject[key].pointer = empty.empty().run

    def init(self):
        for key, value in self.self_info.information.file_info.items():
            if value['__function__'] in [None, '']:
                self.__empty__(key)

            else:
                try:
                    self.self_info.callObject[key].pointer = getattr(self.self_info.callObject[key].pack,
                                                                     value['__function__'])

                except AttributeError as e:
                    self.__empty__(key)


@wrapper
class Run(Framework):
    def __init__(self, self_info: information.File):
        super().__init__(self_info)

        self.self_info = self_info

    def init(self):
        for key, value in self.self_info.information.file_info.items():
            if value['__run__'] is False:
                self.self_info.callObject[key].pointer = empty.empty().run


@wrapper
class ReadRegistration(Framework):
    def __init__(self, self_info: information.File):
        """
        register.threadRegistration

        :param self_info:
        """
        super().__init__(self_info)

        self.self_info = self_info
        self.info = self_info.information["readRegistration"]
        self.logs = self_info.logs["readRegistration"] = {"error": []}

    def init(self):
        func_list = {}
        for key, value in self.info.items():
            level = value['level']
            if level not in func_list:
                func_list[level] = []

            func_list[level].append(key)

        func_list = sorted(func_list.items(), key=lambda x: x[0])
        for level, func_list in func_list:
            for func in func_list:
                try:
                    func(**self.info[func]['kwargs'])

                except Exception as e:
                    self.self_info.logs['readRegistration']['error'].append({func: e})


@wrapper
class Config(Framework):
    def __init__(self, self_info: information.File):
        """
        终于解决每个插件，之间的配置问题
        运行时会插件的配置和用户的配置深度合成,并放入File.config到
        :param self_info: 初始化信息 -> fileMapping.File
        """
        super().__init__(self_info)

        self.self_info = self_info
        self.logs = self_info.logs["config"] = {"error": []}

    def init(self):
        for key, value in self.self_info.information.items():
            pass


@wrapper
class End(Framework):
    def __init__(self, self_info: information.File):
        """
        用于解决每个插件的结束 "end" / "__end__"

        """
        super().__init__(self_info)

        self.self_info = self_info

    def run(self, func: types.FunctionType) -> dict:
        try:
            func()
            return {
                "run": True
            }

        except information.fileMappingConfig.error_list_a2 as e:
            return {
                "run": False,
                "error": e,
                "traceback": traceback.format_exc()
            }

    def end(self):
        if not information.fileMappingConfig.endTheTask:
            return

        for key, value in self.self_info.invoke.items():
            if not information.fileMappingConfig.functionsName["__end__"] in dir(value):
                continue

            pointer = getattr(value, information.fileMappingConfig.functionsName["__end__"])
            if isinstance(pointer, str) and (pointer in dir(value)):
                pointer = getattr(value, pointer)

            elif isinstance(pointer, types.FunctionType):
                pass

            else:
                continue

            data = self.run(pointer)
            if data["run"]:
                self.self_info.logs.fileMappingOutput(
                    information.error.EndOfPlugin(
                        key, pointer.__name__, data["error"], data["traceback"]
                    )
                )

