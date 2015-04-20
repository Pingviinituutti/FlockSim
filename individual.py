from simulation import Simulation
from PyQt5.QtGui import QVector2D


class Individual():

    def __init__(self, id, x, y, velo_x, velo_y):
        '''
        Constructor
        '''
        self.id = id
        self.position = QVector2D(x, y)
        self.velocity = QVector2D(velo_x, velo_y)
        
#     def __init__(self, id, position, velocity):
#         self.position = position
#         self.velocity = velocity
        
    def move(self, sim):
        new_position = self.position + self.velocity * sim.time
        