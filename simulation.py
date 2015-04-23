import sys, random
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont, QVector2D
from PyQt5.QtCore import Qt, QElapsedTimer, QTimer, QBasicTimer, pyqtSignal
from individual import Individual
from bird import Bird
from rule import Rule
from alignment import Alignment
from cohesion import Cohesion
from separation import Separation
from PyQt5.Qt import QVBoxLayout, QHBoxLayout
from slider import Slider
from toOrigin import toOrigin

class Simulation(QWidget):
    
    title = "Flock Simulator 2015"
    tick_rate = 1 # how many milliseconds between each tick
    
    def __init__(self):
        self.width = 800
        self.height = 640
        self.max_fps = 60
        self.show_fps = True
        self.draw_coordinate_axes = True
        self.k = 0.01 # time coefficient
        self.individuals = []
        self.num_individuals = 15
        self.rules = []
        self.scale = 1
        self.slider_accuracy = 100
        
        super().__init__()
        
        self.initRules()
        self.initUI()
        self.initSimulation()
        
    def initUI(self):
        
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        
        # initialize sliders
        self.sliders = []
        for r in self.rules:
            slider = Slider(Qt.Horizontal, self, r, self.slider_accuracy)
            slider.valueChanged.connect(self.changeValue)
            vbox.addStretch(1)
            self.sliders.append(slider)
            vbox.addWidget(slider)
        vbox.addStretch(1)
        
        time_control = QHBoxLayout()
        rewindb = QPushButton('Rewind')
        self.playb = QPushButton('Pause')
        forwardb = QPushButton('Fastforward')
        
        rewindb.clicked[bool].connect(self.manipulateTime)
        self.playb.clicked[bool].connect(self.manipulateTime)
        forwardb.clicked[bool].connect(self.manipulateTime)
        
        self.playb.setChecked(True)
        
        time_control.addWidget(rewindb)
        time_control.addWidget(self.playb)
        time_control.addWidget(forwardb)
        vbox.addLayout(time_control)
        vbox.addStretch(8)

        hbox.addStretch()
        hbox.addStretch()
        hbox.addLayout(vbox)
        
        self.setLayout(hbox)
        
        self.setGeometry(10, 30, self.width, self.height)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('icon.png'))
          
        self.setAutoFillBackground(True)
        white = self.palette()
        white.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(white)
            
        self.show()
        
    def changeValue(self, value):
        source = self.sender()
        
        print("Setting {rname} to value {sval}".format(rname = source.rule.name, sval = value))
        source.rule.setCoefficient(value/self.slider_accuracy/100)
        
    def manipulateTime(self, pressed):
        source = self.sender()
        
        if source.text() == "Rewind":
            self.rewind()
        elif source.text() == "Play":
#             source.setText("Pause")
            self.play()
        elif source.text() == "Pause":
#             source.setText("Play")
            self.pause()
        else:
            self.fastForward()
        
    def initRules(self):
        self.rules.append(Separation(1))
        self.rules.append(Alignment(0.0001))
        self.rules.append(Cohesion(0.00001))
        self.rules.append(toOrigin(0.00001))    
    
    def initSimulation(self):
        size = self.size()
        for i in range(self.num_individuals):
            self.individuals.append(Bird(len(self.individuals) + 1 , random.randint(-size.width()/2,size.width()/2), random.randint(-size.height()/2,size.height()/2), random.randint(-10,10), random.randint(-10,10)))
#             self.individuals.append(Bird(len(self.individuals) + 1 , 0, 0, random.randint(-10,10), random.randint(-10,10)))
#             self.individuals.append(Bird(len(self.individuals) + 1 , 0, 0, 3, 2))
        
        self.ticker = QBasicTimer()
        self.timer = QElapsedTimer()
        
        self.resetTimer()
        
    def resetTimer(self):
        self.ticker.start(self.tick_rate, self)
        self.timer.start()
        
        self.previous_time = self.timer.elapsed()
        self.previous_tick = self.previous_time
        self.fps = 0
        
    def resetSimulation(self):
        self.individuals.clear()
        self.initSimulation()
        self.resetTimer()
            
    def simulate(self, time):
        if time == 0:
            return
        for i in self.individuals:
            rule_vector = QVector2D(0, 0)
            for r in self.rules:
                if len(self.individuals) == 1:
                    break
                tmp_vector = r.algorithm(self.individuals, i)
                rule_vector += tmp_vector 
                print(r.name, tmp_vector)
#             print(i.id, time, self.k)
            i.updateVectors(self.k, rule_vector)
            i.move(time*self.k)

    def drawFrame(self):
        # define the presets for the painter and move origin to center of window
        painter = QPainter()
        painter.begin(self)
        painter.translate(self.size().width()/2, self.size().height()/2)
#         painter.scale(self.scale, self.scale)
#         painter.save()
        
        self.drawCoordinateAxes(painter)    
        
        for i in self.individuals:
            painter.resetTransform()
            painter.translate(self.size().width()/2, self.size().height()/2)
            painter.scale(self.scale, self.scale)
            i.draw(painter, self.size())
#             painter.restore()

        self.drawLabels(painter)
        # draw fps counter last so that it won't be draw behind anything
        self.drawFPS(painter)
        painter.end()
        
    def drawLabels(self, painter):
        layout = self.layout().itemAt(2)
        painter.setPen(Qt.red)
        painter.setFont(QFont('Decorative', 10))
        painter.resetTransform()
        for i in range(len(self.rules)):
#             print(i,self.rules[i].name)
            painter.drawText(layout.itemAt(i*2).geometry(), Qt.AlignLeft, self.rules[i].name)    
        
    def drawCoordinateAxes(self, painter):
        if not self.draw_coordinate_axes:
            return
        painter.setPen(Qt.black)
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
            
    def rewind(self):
        if not self.ticker.isActive():
            self.play()
        if self.k > 0:
            self.k = -0.01
        else:
            self.k *= 2
            
    def fastForward(self):
        if self.k < 0:
            self.k = 0.02
        else:
            self.k *= 2
            
    def play(self):
        self.k = 0.01
        self.resetTimer()
        self.playb.setText("Pause")
        self.update()
        
    def pause(self):
        self.k = 0.01
        self.ticker.stop()
        self.playb.setText("Play")
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
                self.pause()
            else:
                self.play()
        if e.key() == Qt.Key_Plus:
            self.scale *= 2
            self.update()
        if e.key() == Qt.Key_Minus:
            self.scale /= 2
            self.update()
        if e.key() == Qt.Key_R:
            self.resetSimulation()
            self.update()
        if e.key() == Qt.Key_A:
            self.rewind()
        if e.key() == Qt.Key_E:
            self.fastForward()
        if e.key() == Qt.Key_O:
            self.play()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())  
    
