import sys
import glob

class Plot_Review():

	def __init__(self, filename, review_manager):

		self.filename = filename
		self.review_manager = review_manager
		self.filename_sans_path = self.filename.replace("\\", "/").split("/")[-1]

		self.review = {}
		for problem_var in self.review_manager.problem_vars:
	
			self.review[problem_var + "_tick"] = ""
			self.review[problem_var + "_text"] = ""

	def absorb_changes(self, current_input):

		for problem_var in self.review_manager.problem_vars:

			checkbox = current_input[problem_var + "_tick"]
			checked = str(checkbox.isChecked())
			
			input_field = current_input[problem_var + "_text"]
			text = input_field.displayText()

			self.review[problem_var + "_tick"] = checked
			self.review[problem_var + "_text"] = text

	def csv_output(self):
	
		output = self.filename_sans_path

		for problem_var in self.review_manager.problem_vars:
	


			output += "," + self.review[problem_var + "_tick"] + "," + self.review[problem_var + "_text"]

		output += "\n"
		return output