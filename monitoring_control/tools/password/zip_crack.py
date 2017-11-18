import zipfile
import threading

class ZipCracker(threading.Thread):
	thread_list = []

	@staticmethod
	def CrackZip(dic_list, target_file):
		thread_index = 0
		ret = []
		for dic_lib in dic_list:
			thread_index += 1
			temp_thread = ZipCracker(target_file, dic_lib, thread_index)
			temp_thread.start()
			ZipCracker.thread_list.append(temp_thread)
			print("cracker thread:", thread_index, "has started")

	def __init__(self,target_file,pwd_dictionary,index):
		threading.Thread.__init__(self)
		self.z_file = zipfile.ZipFile(target_file, "r")
		self.pwd_number = 0
		self.pwd_dictionary = pwd_dictionary
		self.index = index
		self.stop = False

	def __shutdown(self):
		for cracker in ZipCracker.thread_list:
			cracker.Stop()
		print("all thread has shutdown.")

	def Stop(self):
		print("thread:", self.index, "has shutdown.")
		self.stop = True

	def __test_pwd(self, pwd):
		self.pwd_number += 1
		if self.pwd_number % 10000 == 0:
			print("thread:", self.index, "-----", self.pwd_number, "pwd has ")
		try:
			self.z_file.extractall(pwd=pwd.decode())
			print("password has founded!!!","target zipfile password is:....")
			print("ready to shut down all threads...")
			self.__shutdown()
			return True
		except Exception as e:
			return False

	def run(self):
		pwd_index = 0
		pwd_lib = open(self.pwd_dictionary, "r")
		dic_lib = pwd_lib.readlines()

		while not self.stop:
			try:
				password = dic_lib[pwd_index].strip("\n")
				pwd_index += 1
				if self.__test_pwd(password):
					print("try password number:", self.pwd_number)
			except Exception as e:
				self.Stop()

if __name__ == '__main__':
	dic = ["dictionary123.txt"]
	ZipCracker.CrackZip(dic, "test.zip")
	