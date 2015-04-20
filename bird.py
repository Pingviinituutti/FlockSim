
from PyQt5.QtGui import QVector2D
from PyQt5.QtGui import QPainter, QColor 
from simulation import Simulation
from individual import Individual

class Bird(Individual):
    
    max_speed = 10
    max_turn_rate = 30 # degrees

    def __init__(self, id, x, y, velo_x, velo_y):
        super.__init__(id, x, y, velo_x, velo_y)
        
    def move(self, simulation):
        if self.velocity.length() > self.max_speed:
            self.velocity /= (self.velocity.length()/10)
        Individual.move(self, simulation)
        
    def draw(self, sim):
        
        
        
        
        