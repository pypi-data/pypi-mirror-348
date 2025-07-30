import _io

from . import config
from . import fileMappingConfig
from .error import Mistake


class FilemappingDict(dict):
    # 用于包装字典
    # 可以通过 . 访问属性
    def __getattr__(self, item):
        if item in self:
            return self.get(item)

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")


class Application(FilemappingDict): ...


class CallObject(FilemappingDict): ...


class Invoke(FilemappingDict): ...


class ReturnValue(FilemappingDict): ...


class Public(FilemappingDict): ...


class Information(FilemappingDict):
    appRegister: dict
    readRegistration: dict
    dataFolders: list[str | ...]  # 这个是保存插件申请的数据文件夹


class Logs(FilemappingDict):
    run: int
    parameterApplication: dict

    pluginLogs: list
    fileMappingLogs: list

    def plugInsOutput(self, msg: str | Exception | Mistake) -> bool:
        # 专门对插件的日志输出
        self.pluginLogs.append(msg)
        return True

    def fileMappingOutput(self, msg: str | Exception | Mistake) -> bool:
        # 专门对 fileMapping 的日志输出
        self.fileMappingLogs.append(msg)
        return True


class File:
    callObject: CallObject
    invoke: Invoke
    returnValue: ReturnValue
    public: Public
    information: Information
    logs: Logs

    printLog: bool = False
    printPosition: _io
    path: str
    lordPath: str

    run_order: dict
    listOfFiles: dict


application = Application({})
callObject = CallObject({})
invoke = Invoke({})
returnValue = ReturnValue({})
public = Public({})
information = Information({
    "appRegister": {},
    "readRegistration": {}
})

logs = Logs({
    "run": 1,
    "parameterApplication": {
        "error": []
    },
    "pluginLogs": [],
    "fileMappingLogs": []
})
