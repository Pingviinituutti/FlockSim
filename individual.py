from PyQt5.QtGui import QVector2D
import abc
import math

class Individual():

    def __init__(self, id, x, y, velo_x, velo_y):
        self.id = id
        self.position = QVector2D(x, y)
        self.velocity = QVector2D(velo_x, velo_y)
        self.rule_vector = QVector2D(0, 0)
        
    def updateVectors(self, time_coefficient, rule_vector = QVector2D(0, 0)):
        self.rule_vector = rule_vector
        self.velocity += rule_vector * time_coefficient
        
    def move(self, time):
#         print(self.position, end=', new position: ')
        self.position += (self.velocity) * time
#         print(self.position)

    def calculateAngle(self, rule_vector = QVector2D(0, 0)):
#         master_vector = self.velocity + rule_vector
        if self.velocity.x() == 0:
            self.angle = 90 * self.velocity.y()/abs(self.velocity.y())
        else:
            self.angle = math.atan(self.velocity.y()/self.velocity.x()) * 180/math.pi
#         print("ID: {id},unmodified angle: {ang:.2f}".format(id=self.id, ang=self.angle), end=', ')
        if self.velocity.x() < 0:
            self.angle = 180 + self.angle

    @abc.abstractmethod
    def draw(self, painter, screen_size):
        """draw the individual"""
        return
        
        
        