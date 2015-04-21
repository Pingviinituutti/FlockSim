from PyQt5.QtGui import QVector2D
import abc

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
        
    def move(self, time):
#         print(self.position, end=', new position: ')
        self.position = self.position + self.velocity * time
#         print(self.position)

    @abc.abstractmethod
    def draw(self, painter, screen_size):
        """draw the individual"""
        return
        
        
        