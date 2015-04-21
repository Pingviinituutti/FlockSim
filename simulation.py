import sys, random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from PyQt5.QtCore import Qt, QElapsedTimer, QTimer, QBasicTimer, pyqtSignal
from individual import Individual
from bird import Bird
from rule import Rule
from alignment import Alignment
from cohesion import Cohesion
from separation import Separation

class Simulation(QWidget):
    
    title = "Flock Simulator 2015"
    tick_rate = 1 # how many milliseconds between each tick
    
    def __init__(self):
        self.width = 1280
        self.height = 800
        self.max_fps = 60
        self.show_fps = True
        self.draw_coordinate_axes = True
        self.k = 0.01 # time coefficient
        self.individuals = []
        self.num_individuals = 2
        self.rules = []
        
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
        self.rules.append(Separation(1))
        self.rules.append(Alignment(0.0001))
        self.rules.append(Cohesion(0.00001))
        for i in range(self.num_individuals):
#             self.individuals.append(Bird(len(self.individuals) + 1 , random.randint(1, size.width()-1), random.randint(1, size.height()-1), random.randint(-5,5), random.randint(-5,5)))
            self.individuals.append(Bird(len(self.individuals) + 1 , random.randint(-size.width()/2,size.width()/2), random.randint(-size.height()/2,size.height()/2), random.randint(-10,10), random.randint(-10,10)))
        
        self.ticker = QBasicTimer()
        self.timer = QElapsedTimer()
        
        self.resetTimer()
        
    def resetTimer(self):
        self.ticker.start(self.tick_rate, self)
        self.timer.start()
        
        self.previous_time = self.timer.elapsed()
        self.previous_tick = self.previous_time
        self.fps = 0
            
    def simulate(self, time):
        for i in self.individuals:
            for r in self.rules:
                if len(self.individuals) == 1:
                    break
                r.algorithm(self.individuals, i)
            i.move(time*self.k)

    def drawFrame(self):
        painter = QPainter()
        painter.begin(self)
        painter.translate(self.size().width()/2, self.size().height()/2)
        painter.save()
        
        self.drawCoordinateAxes(painter)    
        
        for i in self.individuals:
            i.draw(painter, self.size())

        # draw fps counter last so that it won't be draw behind anything
        self.drawFPS(painter)
        painter.end()
        
    def drawCoordinateAxes(self, painter):
        if not self.draw_coordinate_axes:
            return
        painter.setPen(Qt.red)
        painter.drawLine(-self.size().width()/2, 0, self.size().width()/2, 0)
        painter.drawLine(0, -self.size().height()/2, 0, self.size().height()/2)
            
    def drawFPS(self, painter):
        if not self.show_fps:
            return
        painter.setPen(Qt.red)
        painter.setFont(QFont('Decorative', 10))
        painter.resetTransform()
        painter.drawText(self.rect(), Qt.AlignLeft, "{fps:.2f}".format(fps=self.fps))
        
    def timerEvent(self, e):
#         self.clicks += 1
#         print("timer event!")
        time = self.timer.elapsed()
        self.simulate(time - self.previous_tick)
        self.previous_tick = time
        if time - self.previous_time > 1000 / self.max_fps:
            
            self.fps = 1000/(time - self.previous_time)
#             print("{fps:.2f}".format(fps=self.fps), end=", ")
#             print(self.previous_time, end=', ')
            self.previous_time = time
#             self.time = self.timer.elapsed()
#             print(self.previous_time)
            self.update()
            
    def paintEvent(self, e):
#         print("paint event!")
        self.drawFrame()

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_F2:
            self.show_fps = (not self.show_fps)
            self.update()
        if e.key() == Qt.Key_F3:
            self.draw_coordinate_axes = (not self.draw_coordinate_axes)
            self.update()
        if e.key() == Qt.Key_Space:
            if self.ticker.isActive():
                self.ticker.stop()
            else:
                self.resetTimer()
        
            
#         if e.key() == Qt.Key_Space:
#             self.drawFrame()
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    sim = Simulation()
#     sim.drawFrame()
    sys.exit(app.exec_())  
    
