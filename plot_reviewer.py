from PyQt4 import QtGui, QtCore

import sys
import glob

inputs = len(sys.argv)

if inputs < 2:

	"""
	app = QtGui.QApplication(sys.argv)
	temp_widget = QtGui.QWidget()
	temp_widget_grid = QtGui.QGridLayout()
	temp_label = QtGui.QLabel("Test", app)
	temp_label.setAlignment(QtCore.Qt.AlignCenter)

	#self.image_widget_grid.addWidget(self.image, 2, 1, 1, 4)

	temp_widget_grid.addWidget(temp_label, 1, 1, 1, 1)
	temp_widget.setLayout(temp_widget_grid)

	temp_widget.setStyleSheet(all_style)
	temp_widget.show()
	"""
	print("Requires a folder")
	sys.exit()
else:
	folder = sys.argv[1]

print folder

pampro_red = "#FA1010"
pampro_green = "#10FA10"
pampro_blue = "#1010FA"
pampro_darkgrey = "#101010"
pampro_lightgrey = "#FAFAFA"
pampro_background = "#FFFFFF"

all_style = """
QWidget { background-color: """+pampro_background+"""; font-size:12px; font-weight:Bold;}
"""

import review_manager, plot_review

image_width = 1240
image_height = 760

manager = review_manager.Review_Manager(folder)

class GUI(QtGui.QMainWindow):

	def __init__(self):

		self.current_review = manager.get_current_review()

		# Prepare GUI

		super(GUI, self).__init__()

		self.setGeometry(0, 0, 400, 400)
		self.setWindowTitle('Plot reviewer')
		#self.setWindowIcon(QtGui.QIcon('temp.png'))


		# Create the two displays
		self.image_display = self.create_image_display()
		self.input_display = self.create_input_display()

		# Make it pretty
		self.setStyleSheet(all_style)
		self.center()

		# Load the first review
		self.load_review(self.current_review)

		# And begin
		self.show()

	def center(self):
		"""Centers the GUI on the screen"""

		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def create_image_display(self):

		self.image_widget = QtGui.QWidget()
		self.image_widget_grid = QtGui.QGridLayout()
		self.image_label = QtGui.QLabel("Test",self)
		self.image_label.setAlignment(QtCore.Qt.AlignCenter)

		self.image = QtGui.QLabel("Test", self)
		self.image.setScaledContents(True)
		self.image.setFixedSize(image_width, image_height)
		self.image_widget_grid.addWidget(self.image, 2, 1, 1, 4)
		self.image_widget_grid.addWidget(self.image_label, 1, 1, 1, 4)
		self.image_widget.setLayout(self.image_widget_grid)

		self.image_widget.setStyleSheet(all_style)
		self.image_widget.show()

		return self.image_widget

	def create_input_display(self):
		# Input widget

		self.input_display = QtGui.QWidget(self)
		self.grid = QtGui.QGridLayout()
		self.grid.setSpacing(10)

		self.current_input = {}
		self.input_holder = QtGui.QWidget()
		self.input_holder_grid = QtGui.QGridLayout()


		self.image_label_input = QtGui.QLabel("Test",self)
		self.image_label_input.setAlignment(QtCore.Qt.AlignCenter)
		self.input_holder_grid.addWidget(self.image_label_input, 1, 1, 1, 3)
		for i,(prob_text,prob_var) in enumerate(zip(manager.problem_texts, manager.problem_vars)):

			lab = QtGui.QLabel(prob_text, self)
			box = QtGui.QCheckBox(self)
			input_field = QtGui.QLineEdit(self)
			self.current_input[prob_var+"_tick"] = box
			self.current_input[prob_var+"_text"] = input_field

			self.input_holder_grid.addWidget(lab, 2+i, 1, 1, 1)
			self.input_holder_grid.addWidget(box, 2+i, 2, 1, 1)
			self.input_holder_grid.addWidget(input_field, 2+i, 3, 1, 1)
		# -- -- -- -- -- --
		self.input_holder.setLayout(self.input_holder_grid)



		# Navigation buttons

		self.button_prev = QtGui.QPushButton('Previous', self)
		action_prev = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Prev', self)
		action_prev.setShortcut('Key_Left')
		action_prev.triggered.connect(self.prev)
		self.button_prev.clicked.connect(self.prev)

		self.button_next = QtGui.QPushButton('Next', self)
		action_next = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Next', self)
		action_next.setShortcut('N')
		action_next.triggered.connect(self.next)
		self.button_next.clicked.connect(self.next)

		self.button_holder = QtGui.QWidget()
		self.button_holder_grid = QtGui.QGridLayout()
		self.button_holder_grid.addWidget(self.button_prev, 1, 1, 1, 1)
		self.button_holder_grid.addWidget(self.button_next, 1, 2, 1, 1)
		self.button_holder.setLayout(self.button_holder_grid)

		self.grid.addWidget(self.input_holder, 1, 1, 1, 1)
		self.grid.addWidget(self.button_holder, 2, 1, 1, 1)

		self.input_display.setLayout(self.grid)
		self.input_display.resize(self.input_display.sizeHint())

		return self.input_display


	def set_image(self, filename):
		"""Loads the image specified by filename and displays it"""

		print filename
		pm = QtGui.QPixmap(filename)
		blah = pm.load(filename)
		size = pm.size()

		pm = pm.scaled(image_width, image_height)
		self.image.setPixmap(pm)



	def load_review(self, review):

		self.current_review = review

		self.set_image(review.filename)
		self.image_label.setText(review.filename_sans_path)
		self.image_label_input.setText(review.filename_sans_path)

		for k,v in review.review.items():

			widget = self.current_input[k]
			if "_tick" in k:
				widget.setChecked(False)
				if v == "True":
					widget.setChecked(True)

			elif "_text" in k:
				widget.setText(v)




	def next(self):
		"""Advances to the next image in the folder and displays it"""

		self.commit_result()
		self.load_review(manager.next_review())


	def prev(self):
		"""Advances to the previous image in the folder and displays it"""

		self.commit_result()
		self.load_review(manager.previous_review())


	def commit_result(self):
		"""Update the line in the CSV result file corresponding to the current file, using the current input state"""

		"""
		for prob_text, prob_var in zip(manager.problem_texts, manager.problem_vars):

			checkbox = self.current_input[prob_var + "_tick"]
			checked = checkbox.isChecked()

			input_field = self.current_input[prob_var + "_text"]
			text = input_field.displayText()

			print prob_text, checked, text
		"""

		self.current_review.absorb_changes(self.current_input)
		manager.update_output()


if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	m = GUI()
	sys.exit(app.exec_())
