import _io
import os

from .. import information


def dataFolders(name: str, *args) -> str | bool:
    """
    数据文件夹
    :return:
    """
    if name in information.information.dataFolders:
        if args is None:
            return information.information.dataFolders[name]

        else:
            return os.path.join(information.information.dataFolders[name], *args)

    else:
        return False


def temporaryFolders(name: str, *args) -> str | bool:
    """
    临时文件夹
    :return:
    """
    if name in information.information.temporaryFolders:
        if args is None:
            return information.information.temporaryFolders[name]

        else:
            return os.path.join(information.information.temporaryFolders[name], *args)

    else:
        return False


def fileOperations(path: str, *args, **kwargs) -> _io.open:
    """
    文件操作
    :return:
    """
    try:
        file = open(path, *args, **kwargs)
        return file

    except Exception as e:
        return False

