import sys, random
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont, QVector2D
from PyQt5.QtCore import Qt, QElapsedTimer, QTimer, QBasicTimer, pyqtSignal, QPoint
from individual import Individual
from bird import Bird
from rule import Rule
from alignment import Alignment
from cohesion import Cohesion
from separation import Separation
from PyQt5.Qt import QVBoxLayout, QHBoxLayout, QAction, QFileDialog
from slider import Slider
from toOrigin import toOrigin
from test.test_buffer import indices

class Simulation(QWidget):
    
    title = "Flock Simulator 2015"
    tick_rate = 1 # how many milliseconds between each tick
    
    def __init__(self):
        
        self.width = 800
        self.height = 640
        self.max_fps = 60
        self.show_fps = True
        self.debug = True
        self.k = 0.01 # time coefficient
        self.individuals = []
        self.rules = []
        self.scale = 1
        self.slider_accuracy = 100
        self.right_mouse_down = False
        self.mouse_down_position = QVector2D(0, 0)
        self.mouse_translation = QPoint(0, 0)
        self.left_mouse_down = False
        self.left_mouse_start_position = QPoint(0, 0)
        self.left_mouse_position = QPoint(0, 0)
        
        super().__init__()
        
        self.initRules()
        self.initUI()
        self.initTimers()
        self.initSimulation()
        self.resetTimer()
        
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
        
        # time controls
        time_control = QHBoxLayout()
        rewindb = QPushButton('Rewind')
        self.playb = QPushButton('Pause')
        forwardb = QPushButton('Fastforward')
        
        # make the buttons unfocusable
        rewindb.setFocusPolicy(0)
        self.playb.setFocusPolicy(0)
        forwardb.setFocusPolicy(0)
        
        rewindb.clicked[bool].connect(self.manipulateTime)
        self.playb.clicked[bool].connect(self.manipulateTime)
        forwardb.clicked[bool].connect(self.manipulateTime)
        
        time_control.addWidget(rewindb)
        time_control.addWidget(self.playb)
        time_control.addWidget(forwardb)
        vbox.addLayout(time_control)
        
        # individual controls (e.g. adding or removing)
        vbox.addStretch(1)
        individual_control = QHBoxLayout()
        remove_indb = QPushButton('-')
        self.show_indb = QPushButton('0')
        add_indb = QPushButton('+')
        
        remove_indb.setFocusPolicy(0)
        self.show_indb.setFocusPolicy(0)
        add_indb.setFocusPolicy(0)
        
        self.show_indb.setFlat(True)
        remove_indb.clicked[bool].connect(self.removeIndividual)
        add_indb.clicked[bool].connect(self.addIndividual)
        
        individual_control.addWidget(remove_indb)
        individual_control.addWidget(self.show_indb)
        individual_control.addWidget(add_indb)
        
        vbox.addLayout(individual_control)
        vbox.addStretch(1)
        # save or load buttons
#         openFile = QAction(QIcon('open.png'), 'Open', self)
#         openFile.setShortcut('O')
#         openFile.setStatusTip('Open new File')
#         openFile.triggered.connect(self.showDialog)
        
        sim_files = QHBoxLayout()
        save_game = QPushButton('Save')
        load_game = QPushButton('Load')
        
        save_game.clicked[bool].connect(lambda: self.showDialog())
        load_game.clicked[bool].connect(lambda: self.showDialog())
        
        save_game.setFocusPolicy(0)
        load_game.setFocusPolicy(0)
        
        sim_files.addWidget(save_game)
        sim_files.addWidget(load_game)
        
        vbox.addLayout(sim_files)
        
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
        
    def showDialog(self):
        self.pause()
        source = self.sender()
        if source.text() == 'Load':
#             print("in load file dialog")
            fname = QFileDialog.getOpenFileName(self, 'Open file', '', '*.sim')
#             print(fname[0])
            self.loadSimulation(fname[0])
            
        elif source.text() == 'Save':
#             print("in save file dialog")
            fname = QFileDialog.getSaveFileName(self, 'Save file', '', '*.sim')
#             print(fname)
            fname = ''.join((fname[0].replace('.sim',''), fname[1].strip('*')))
#             print(fname)
            
            self.saveSimulation(fname)
            
            
    def loadSimulation(self, fname):
        f = open(fname, 'r')
        chunk_list = []
        line = f.readline()
#         print("line: " +line)
        while len(line) > 0:
            if line == '\n':
                line = f.readline()
                continue
            line = line.split(',')
#             print(line[0])
#             print(len(chunk_list))
#             print(line[0])
            if line[0].split()[0] == '#':
                chunk_list.append([line])
#                 print(len(chunk_list))
            else:
#                 print(len(chunk_list))
                chunk_list[len(chunk_list)-1].append(line)
#                 print(len(chunk_list))
            line = f.readline()          
        coefficient_chunk = []
        individual_chunk = []    
        for c in chunk_list:
#             print(c[0])
            if c[0][0] == '# koefficients\n':
                coefficient_chunk = c
            elif c[0][0] == '# individuals\n':
                individual_chunk = c
#             print(c)
#         print(coefficient_chunk)
        for r in self.rules:
            for i in range(1,len(coefficient_chunk)):
                if r.name == coefficient_chunk[i][0]:
                    r.coefficient = float(coefficient_chunk[i][1])
        self.individuals.clear()
#         print(individual_chunk)
        for i in range(1, len(individual_chunk)):
#             print(i)
#             print(individual_chunk[i][1], individual_chunk[i][2], individual_chunk[i][3], individual_chunk[4])
            self.addIndividual(float(individual_chunk[i][1]), float(individual_chunk[i][2]), float(individual_chunk[i][3]), float(individual_chunk[i][4]))
        f.close
            
            
    def saveSimulation(self, fname):
        f = open(fname, 'w+')
        f.write("# FlockSimulator 2015 v1.0\n\n")
        f.write("# koefficients\n")
        for r in self.rules:
            f.write("{rname},{c:.10f}\n".format(rname = r.name, c = r.coefficient))
        
        f.write("\n# individuals\n")
        for i in self.individuals:
            f.write("{id},{x:.10f},{y:.10f},{vx:.10f},{vy:.10f}\n".format(id = i.id, x = i.position.x(), y = i.position.y(), vx = i.velocity.x(), vy = i.velocity.y()))
        f.close
        
    def changeValue(self, value):
        source = self.sender()
        source.rule.setCoefficient(value/self.slider_accuracy/100)
        
    def addIndividual(self, x = 0, y = 0, vx = 0, vy = 0):
        if x == 0:
            x = random.randint(-self.size().width(), self.size().width())
        if y == 0:
            y = random.randint(-self.size().height(), self.size().height())
        if vx == 0:
            vx = random.randint(-10,10)
        if vy == 0:
            vy = random.randint(-10,10)
        self.individuals.append(Bird(len(self.individuals) + 1, x, y, vx, vy))
        self.show_indb.setText(str(len(self.individuals)))
        self.update()
        
    def removeIndividual(self, id = 0):
        if len(self.individuals) == 0:
            return
        if id == 0:
            self.individuals.pop()
        else:
            self.individuals.pop(id)
        self.show_indb.setText(str(len(self.individuals)))
        self.update()
        
    def initRules(self):
        self.rules.append(Separation(1))
        self.rules.append(Alignment(0.0001))
        self.rules.append(Cohesion(0.00001))
        self.rules.append(toOrigin(0.00001))    
    
    def initSimulation(self, n = 5):
        # spawns individuals inside the current screen
        size = self.size() / self.scale / 3 * 2
        for i in range(n):
            self.addIndividual(random.randint(-size.width()/2, size.width()/2), random.randint(-size.height()/2, size.height()/2))
        
    def initTimers(self):
        self.ticker = QBasicTimer()
        self.timer = QElapsedTimer()
        
    def resetTimer(self):
        self.ticker.start(self.tick_rate, self)
        self.timer.start()
        
        self.previous_time = self.timer.elapsed()
        self.previous_tick = self.previous_time
        self.simulation_time = 0
        self.drawing_time = 0
        self.fps = 0
        
    def resetSimulation(self):
        for i in self.individuals:
            i.reset()
        self.update()
        
    def newSimulation(self):
        n = len(self.individuals)
        self.individuals.clear()
        self.initSimulation(n)
            
    # this calculates the position of the individuals in the simulation
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
            i.updateVectors(self.k, rule_vector)
            i.move(time*self.k)
        self.simulation_time = self.timer.elapsed()
            
                
    def manipulateTime(self, pressed):
        source = self.sender()
        if source.text() == "Rewind":
            self.rewind()
        elif source.text() == "Play":
            self.play()
        elif source.text() == "Pause":
            self.pause()
        else:
            self.fastForward()

    def drawFrame(self):
        # define the presets for the painter and move origin to center of window
        painter = QPainter()
        painter.begin(self)
        painter.translate(self.size().width()/2, self.size().height()/2)
        
        self.drawCoordinateAxes(painter)    
        
        # draw the individuals
        for i in self.individuals:
            painter.resetTransform()
            painter.translate(self.size().width()/2, self.size().height()/2)
            painter.translate(-self.mouse_translation.x(), -self.mouse_translation.y())
            painter.scale(self.scale, self.scale)
            i.draw(painter, self.debug)

        self.drawing_time = self.timer.elapsed()
        self.drawSpeedArrow(painter)

        self.drawLabels(painter)
        
        # draw fps counter last so that it won't be drawn behind anything
        self.drawFPS(painter)
        painter.end()
        
    def drawSpeedArrow(self, painter):
        if not self.left_mouse_down:
            return
        painter.resetTransform()
        
        painter.setPen(Qt.red)
        painter.drawLine(self.left_mouse_start_position, self.left_mouse_position)
        
    def drawLabels(self, painter):
        layout = self.layout().itemAt(2)
        painter.setPen(Qt.red)
        painter.setFont(QFont('Decorative', 10))
        painter.resetTransform()
        for i in range(len(self.rules)):
            painter.drawText(layout.itemAt(i*2).geometry(), Qt.AlignLeft, self.rules[i].name)    
        
    def drawCoordinateAxes(self, painter):
        if not self.debug:
            return
        painter.setPen(Qt.black)
        painter.translate(-self.mouse_translation.x(), -self.mouse_translation.y())
        painter.drawLine(-self.size().width()/2, 0, self.size().width()/2, 0)
        painter.drawLine(0, -self.size().height()/2, 0, self.size().height()/2)
            
    def drawFPS(self, painter):
        if not self.show_fps and not self.debug:
            return
        painter.setPen(Qt.red)
        painter.setFont(QFont('Decorative', 10))
        painter.resetTransform()
        painter.drawText(0, 10, "FPS:{fps:.2f}".format(fps=self.fps))
        if self.debug:
            painter.drawText(0, 20, "SIMTIME:{simTime:.2f}".format(simTime=self.simulation_time - self.previous_tick))
            painter.drawText(0, 30, "DRAWTIME{drawTime:.2f}".format(drawTime=self.drawing_time - self.simulation_time))
        
    def timerEvent(self, e):
        time = self.timer.elapsed()
        self.simulate(time - self.previous_tick)
        self.previous_tick = time
        if time - self.previous_time > 1000 / self.max_fps:
            
            self.fps = 1000/(time - self.previous_time)
            self.previous_time = time
            self.update()
            
    def rewind(self):
        if not self.ticker.isActive():
            self.play()
        if self.k > 0:
            self.k = -0.01
        else:
            self.k *= 2
            
    def fastForward(self):
        if not self.ticker.isActive():
            self.play()
        else:
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
        self.drawFrame()
        
    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.right_mouse_down = True
            self.mouse_down_position = e.pos()
            self.previous_translation = self.mouse_translation
        elif e.button() == Qt.LeftButton:
            self.left_mouse_down = True
            self.left_mouse_start_position = e.pos()
            self.left_mouse_position = self.left_mouse_start_position
        
    def mouseMoveEvent(self, e):
        if self.right_mouse_down:
            self.mouse_translation = self.previous_translation + self.mouse_down_position - e.pos()
            
        elif self.left_mouse_down:
            self.left_mouse_position = e.pos()
        self.update()
        
    def mouseReleaseEvent(self, e):
        if self.right_mouse_down:
            self.right_mouse_down = False
        if self.left_mouse_down:
            self.addIndividual((self.left_mouse_start_position.x() + self.mouse_translation.x() - self.size().width() / 2) / self.scale, 
                               (self.left_mouse_start_position.y() + self.mouse_translation.y() - self.size().height() / 2) / self.scale, 
                               (self.left_mouse_position - self.left_mouse_start_position).x() / self.size().width() * 100, 
                               (self.left_mouse_position - self.left_mouse_start_position).y() / self.size().height() * 100)
            self.left_mouse_down = False
        self.update()
        
    def wheelEvent(self, e):
        if e.angleDelta().y() > 0:
            self.scale *= 2
        else:
            self.scale /= 2
        self.update()
        

    def keyPressEvent(self, e):
        
        if e.key() == Qt.Key_Escape:
            self.close()
        if e.key() == Qt.Key_F2:
            self.show_fps = (not self.show_fps)
            self.update()
        if e.key() == Qt.Key_F3:
            self.debug = (not self.debug)
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
        if e.key() == Qt.Key_N:
            self.newSimulation()
            self.update()
        if e.key() == Qt.Key_Left:
            self.rewind()
        if e.key() == Qt.Key_Right:
            self.fastForward()
#         if e.key() == Qt.Key_Space:
#             self.play()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    sim = Simulation()
    sys.exit(app.exec_())  
    
