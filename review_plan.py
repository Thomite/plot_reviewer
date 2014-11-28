class Review_Plan():
	
	def __init__(self, config_filename):

		config_file = open(config_filename, "r")
		lines = [line.strip() for line in config_file]
		self.problem_texts = [line.split(",")[0].strip() for line in lines]
		self.problem_vars = [line.split(",")[1].strip() for line in lines]
		config_file.close()