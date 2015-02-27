import plot_review
import sys
import glob

class Review_Manager():

	def __init__(self, folder):

		self.folder = folder
		self.output_filename = "plot_review.csv"

		self.load_config()

		self.get_files()

		# If there is not a plot review file started
		if len(glob.glob(folder + "/" + self.output_filename)) == 0:
		#if 1==1:

			self.initialise_blank_reviews()
			self.update_output()
			self.current_index = 0

		else:

			self.load_output(folder + "/" + self.output_filename)
			self.current_index = self.next_unreviewed_index()

		self.build_lookup()

	def get_current_review(self):

		return self.get_review(self.current_index)

	def get_review(self, index):

		return self.reviews[index]

	def next_unreviewed_index(self):

		for index,r in enumerate(self.reviews):
			reviewed = False
			for k,v in r.review.items():
				if "_tick" in k:
					if v == "True" or v == "False":
						reviewed = True


			if reviewed == False:
				return index
		return 0

	def next_review(self):

		self.current_index += 1
		if self.current_index == len(self.files):
			self.current_index = 0
		return self.get_current_review()

	def previous_review(self):

		self.current_index -= 1
		if self.current_index == -1:
			self.current_index = len(self.files)-1
		return self.get_current_review()

	def get_files(self):

		self.files = glob.glob(self.folder + "/*.png")
		self.files.sort()

	def initialise_blank_reviews(self):

		self.reviews = [plot_review.Plot_Review(f, self) for f in self.files]


	def build_lookup(self):

		self.review_lookup = {}
		for r in self.reviews:
			self.review_lookup[r.filename] = r



	def load_config(self):

		config_file = open(self.folder + "/plot_problems.csv", "r")
		lines = [line.strip() for line in config_file]
		self.problem_texts = [line.split(",")[0].strip() for line in lines]
		self.problem_vars = [line.split(",")[1].strip() for line in lines]
		config_file.close()

	def load_output(self, output_filename):

		output_file = open(output_filename, "r")

		header = output_file.readline()

		variables = header.split(",")
		variables = [v.strip() for v in variables]
		#print variables

		self.reviews = []

		for line in output_file:

			vals = line.split(",")
			#print vals
			review = plot_review.Plot_Review(self.folder + "/" + vals[0], self)

			for v,h in zip(vals[1:], variables[1:]):
				review.review[h] = v
			self.reviews.append(review)

		output_file.close()

		print(variables)

	def write_output(self, output_filename):

		output_file = open(output_filename, "w")

		output_file.write("filename")
		for problem in self.problem_vars:
			output_file.write(", " + problem + "_tick, " + problem + "_text")
		output_file.write("\n")

		for r in self.reviews:
			output_file.write(r.csv_output())

		output_file.close()

	def update_output(self):

		self.write_output(self.folder + "/" + self.output_filename)

	def update_review(self, review):

		self.review_lookup[review.filename] = review
