#coding=utf-8

from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMainWindow

def new_window():
	global app,widget,textLabel,window
	import sys
	from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QMainWindow
	from PyQt5.QtGui import QIcon
	from PyQt5.QtCore import pyqtSlot

	app = QApplication(sys.argv)# create pyqt5 app
	window = Window()# create the instance of our Window
	return app.exec_()
	
	widget = QWidget()

	textLabel = QLabel(widget)
	textLabel.setText("Hello World! 0")
	textLabel.move(110,85)

	widget.setGeometry(50,50,320,200)
	widget.setWindowTitle("PyQt5 Example")
	widget.setStyleSheet('QWidget#vc{background-color: transparent}')
	widget.show()
	app.exec_()
	# sys.exit(app.exec_())

class Window(QMainWindow):
  
  
	def __init__(self):
		super().__init__()
		# set the title
		self.setWindowTitle("Python")
  
		self.setWindowOpacity(0.5)
 
  
		# setting  the geometry of window
		self.setGeometry(60, 60, 600, 400)
  
		# creating a label widget
		self.label_1 = QLabel("transparent ", self)
		# moving position
		self.label_1.move(100, 100)
  
		self.label_1.adjustSize()
  
		# show all the widgets
		self.show()
  
  

  	
	
	
if __name__ == '__main__':
	new_window()