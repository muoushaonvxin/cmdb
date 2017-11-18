from .linux import linux_network, linux_cpu
from .windows import windows_network


def GetLinuxCpuStatus():
	return linux_cpu.monitor()

def GetNginxStatus():
	pass

def GetLinuxMemStatus():
	pass

def GetLinuxNetworkStatus():
	return linux_network.monitor()

def GetMySQLStatus():
	pass