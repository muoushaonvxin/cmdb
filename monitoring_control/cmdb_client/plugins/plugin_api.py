# _*_ encoding: utf-8 _*_
from .linux import GetLinuxSysInfo
#from .windows import GetWindowsSysInfo


def LinuxSysInfo():
    return GetLinuxSysInfo.collect()

#def WindowsSysInfo():
#    return GetWindowsSysInfo.collect()
