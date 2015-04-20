import sys
from PyQt5.QtWidgets import QApplication, QWidget
from simulation import Simulation

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    sim = Simulation()
    sim.drawFrame()
    sys.exit(app.exec_())  