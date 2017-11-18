from core.client import ClientHandlers
import sys

class main_command(object):

    def __init__(self, sys_argv):
        self.sys_argv = sys_argv
        if len(sys_argv) < 2:
            sys.exit(u"""Please input start or stop:

                        start:  argument start is start the monitor client. 
                        stop:   argument stop is stop the monitor client.

                """)
        else:
            self.entry_command()

    def entry_command(self):
        if hasattr(self, self.sys_argv[1]):
            func = getattr(self, self.sys_argv[1])
            return func()
        else:
            print(u"请输入正确的命令")

    def start(self):
        client = ClientHandlers()
        client.forever_run()

    def stop(self):
        pass

