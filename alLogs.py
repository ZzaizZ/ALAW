class LogString():
	
	def __init__(self, log_name = 'syslog'):
		self.log_name = log_name



	def __prepare_string(self, origin_string):
		splitted_string = origin_string.split(" ", 5)
		log_string = {"Date": "", "Time": "", "Source": "", "ProcessName": "", "Event": ""}
		log_string['Month'] = splitted_string[0] + " " + splitted_string[1]
		log_string['Time'] = splitted_string[2]
		log_string['Source'] = splitted_string[3]
		log_string['ProcessName'] = splitted_string[4][:-1]
		log_string['Event'] = splitted_string[5]
		return log_string

	def get_log_str(self):
		return self.__prepare_string()

class SystemLog():

	
	def __init__(self, log_name):
		self.log_name = log_name
		self.log_strings = []

	def __add_string(self, string):
		self.strings.append(string)

	def read_log(self):
		if self.log_name[-2:] == 'gz':
			with gzip.open('/var/log/'+self.log_name, 'r') as f:
				lines = []
				for line in f.readlines():
					lines.append(line.decode('utf-8'))						
		else:						
			with open('/var/log/'+self.log_name, 'r') as f:
				lines = f.readlines()
		for log_string in lines:
			splitted_string = log_string.split(" ", 5)
			log_string = {"Date": "", "Time": "", "Source": "", "ProcessName": "", "Event": ""}
			log_string['Date'] = splitted_string[0] + " " + splitted_string[1]
			log_string['Time'] = splitted_string[2]
			log_string['Source'] = splitted_string[3]
			log_string['ProcessName'] = splitted_string[4][:-1]
			log_string['Event'] = splitted_string[5]
			self.log_strings.append(log_string)
	
	def 

test = SystemLog('syslog')
test.read_log()

