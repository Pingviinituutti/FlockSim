import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt, QElapsedTimer, pyqtSignal
from individual import Individual
from bird import Bird

class Simulation(QWidget):
    
    title = "Flock Simulator 2015"
    width = 800
    height = 640
    show_fps = True
    k = 1 # time coefficient
    individuals = []
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
#         self.initPainter()
        self.initSimulation()
        self.painter = QPainter(self)
#         self.painter.beg
        
    def initUI(self):
        
        self.setGeometry(10, 30, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
          
#         self.setAutoFillBackground(True)
#         white = self.palette()
#         white.setColor(self.backgroundRole(), Qt.red)
#         self.setPalette(white)   
    
        self.show()
        
    def getFrame(self):
        return self.time * self.k
    
    def initSimulation(self):
        self.timer = QElapsedTimer()
        self.timer.start()
        
        self.individuals.append(Bird(len(self.individuals) + 1 , 400, 320, 0, 0))
#         for i in range(1,4)

    def drawFrame(self):
        print(self.timer.elapsed())
        for i in self.individuals:
            i.draw(self.painter)

#         self.update()
        
    