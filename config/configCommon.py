# -*- coding: utf-8 -*-
import datetime
import os
import random
import time


def getNowTimestamp():
    return time.time()


def decMakeDir(func):
    def handleFunc(*args, **kwargs):
        dirname = func(*args, **kwargs)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        elif not os.path.isdir(dirname):
            pass

        return dirname

    return func


def getWorkDir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#
# def fileOpen(path):
#     """
#     文件读取兼容2和3
#     :param path: 文件读取路径
#     :return:
#     """
#     try:
#         with open(path, "r", ) as f:
#             return f
#     except TypeError:
#         with open(path, "r", ) as f:
#             return f



@decMakeDir
def getTmpDir():
    return os.path.join(getWorkDir(), "tmp")


@decMakeDir
def getLogDir():
    return os.path.join(getTmpDir(), "log")


@decMakeDir
def getCacheDir():
    return os.path.join(getTmpDir(), "cache")


@decMakeDir
def getVCodeDir():
    return os.path.join(getTmpDir(), "vcode")


def getVCodeImageFile(imageName):
    return os.path.join(getVCodeDir(), imageName + ".jpg")


def getCacheFile(cacheType):
    return os.path.join(getCacheDir(), cacheType + ".cache")