def circularDependenciesError(logs: dict, logs_path: tuple):
    logs["run"] += 1
    logs["error"] = "循环依赖"
    logs["data"] = logs_path


class Mistake(Exception):
    # 这个是对错误进行记录
    msg: str
    traceback: str
    listOfLanguages: list[...]

    def __init__(self, msg: str, traceback: str): ...

    def dict(self) -> dict:
        """
        这个是对 错误/异常 进行 json/dict 记录
        可以更好地提供日志数据
        """
        return {}


class Register(Mistake):
    def __init__(self, func: str, error: Exception, traceback: str):
        self.func = func
        self.error = error
        self.traceback = traceback
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self) -> str:
        return f"Register the function: {self.func} error: {self.error}"

    def chinese(self) -> str:
        return f"注册函数: {self.func} error: {self.error}"

    def dict(self) -> dict: ...


class ParameterApplication(Register):
    def __init__(self, func: str, error: Exception, traceback: str):
        self.func = func
        self.error = error
        self.traceback = traceback
        self.listOfLanguages = [
            self.english, self.chinese
        ]


class AppInit(ParameterApplication):
    def english(self) -> str:
        return f"An error occurred while initializing the function for the registration function: {self.func} error: {self.error}"

    def chinese(self) -> str:
        return f"注册函数在进行初始化函数时发生了错误: {self.func} error: {self.error}"


class AppEnd(ParameterApplication):
    def english(self) -> str:
        return f"An error occurred while registering the function while performing the ending function: {self.func} error: {self.error}"

    def chinese(self) -> str:
        return f"注册函数在进行结束函数时发生了错误: {self.func} error: {self.error}"


class EndOfPlugin(Mistake):
    def __init__(self, pluginName: str, func: str, error: Exception, traceback: str):
        self.pluginName = pluginName
        self.func = func
        self.error = error
        self.traceback = traceback
        self.listOfLanguages = [
            self.english, self.chinese
        ]

    def english(self):
        return f"'fileMapping' An error occurred while running the plugin's ending function\n" \
               f"The name of the plugin: {self.pluginName} function: {self.func} error: {self.error}"

    def chinese(self):
        return f"fileMapping 在运行插件的结束函数时发生错误 插件名字:{self.pluginName} 函数: {self.func} error: {self.error}"
