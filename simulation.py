import sys, random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QElapsedTimer, QTimer, QBasicTimer, pyqtSignal
from individual import Individual
from bird import Bird

class Simulation(QWidget):
    
    title = "Flock Simulator 2015"
    width = 800
    height = 640
    max_fps = 60
    
    def __init__(self):
        self.show_fps = True
        self.k = 0.00001 # time coefficient
        self.individuals = []
        
        super().__init__()
        
        self.initUI()
        self.initSimulation()
        
    def initUI(self):
        
        self.setGeometry(10, 30, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
          
        self.setAutoFillBackground(True)
        white = self.palette()
        white.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(white)
    
        self.show()
    
    def initSimulation(self):
        size = self.size()
        for i in range(4):
            self.individuals.append(Bird(len(self.individuals) + 1 , random.randint(1, size.width()-1), random.randint(1, size.height()-1), random.randint(-5,5), random.randint(-5,5)))
        
        self.ticker = QBasicTimer()
        self.timer = QElapsedTimer()
        
        self.ticker.start(1, self)
        self.timer.start()
        
        self.previous_time = self.timer.elapsed()
        self.fps = 0

    def timerEvent(self, e):
#         self.clicks += 1
#         print("timer event!")
        time = self.timer.elapsed()
        self.simulate(time)
        if time - self.previous_time > 1000 / self.max_fps:
            
            self.fps = 1000/(time - self.previous_time)
#             print("{fps:.2f}".format(fps=self.fps), end=", ")
#             print(self.previous_time, end=', ')
            self.previous_time = time
#             self.time = self.timer.elapsed()
#             print(self.previous_time)
            self.update()
            
    def simulate(self, time):
        for i in self.individuals:
            i.move(time*self.k)
        
    def drawFPS(self, painter):
#         print(self.clicks)
        painter.setPen(Qt.red)
        painter.setFont(QFont('Decorative', 10))
        painter.drawText(self.rect(), Qt.AlignLeft, "{fps:.2f}".format(fps=self.fps))

    def drawFrame(self):
        painter = QPainter()
        painter.begin(self)
        
        if self.show_fps:
            self.drawFPS(painter)
#         painter.setPen(Qt.red)
#         size = self.size()
#         print(self.timer.elapsed())
#         for i in range(1000):
#             x = random.randint(1, size.width()-1)
#             y = random.randint(1, size.height()-1)
#             painter.drawPoint(x, y)   
        
#         print(self.timer.elapsed())    
#         painter.drawRect(10, 15, 90, 60)
        
#         print(self.timer.elapsed())
        for i in self.individuals:
            i.draw(painter)

        painter.end()
        
    def paintEvent(self, e):
#         print("paint event!")
        self.drawFrame()

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_F2:
            self.show_fps = (not self.show_fps)
            
#         if e.key() == Qt.Key_Space:
#             self.drawFrame()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    sim = Simulation()
#     sim.drawFrame()
    sys.exit(app.exec_())  
    
