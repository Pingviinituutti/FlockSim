# from PyQt5.QtGui import QVector2D
from PyQt5.QtGui import QPainter, QColor, QPixmap
from individual import Individual
import math

from PyQt5.QtCore import Qt, QRect

class Bird(Individual):
    
    max_speed = 10
    max_turn_rate = 30 # degrees

    def __init__(self, id, x, y, velo_x, velo_y):
#         super(Individual, self).__init__(x, y, velo_x, velo_y)
        Individual.__init__(self, id, x, y, velo_x, velo_y)
        self.sprite = QPixmap()
        self.sprite.load('bird', 'png')
        
    def move(self, time):
        if self.velocity.length() > self.max_speed:
            self.velocity /= (self.velocity.length())
        Individual.move(self, time)
        
    def draw(self, painter, screen_size):
#         print(self.position)
#         painter.translate(-self.sprite.width()/2, -self.sprite.height()/2)
        painter.translate(self.position.x(), self.position.y())
        
        if self.velocity.x() == 0:
            angle = 90 * self.velocity.y()/abs(self.velocity.y())
        else:
            angle = math.atan(self.velocity.y()/self.velocity.x()) * 180/math.pi
        print("unmodified angle: {ang:.2f}".format(ang=angle), end=', ')
        if self.velocity.x() < 0:
            angle = 180 + angle
        print(self.position, end=', velocity: ')
        print(self.velocity, end=', angle: ')
        print(angle) #, end=', transformed coordinates: ')
#         angle = 10
        painter.rotate(angle)
#         cosa = math.cos(angle)
#         sina = math.sin(angle)
#         x2 = (self.position.x() * cosa + self.position.y() * sina)
#         y2 = (self.position.x() * -sina + self.position.y() * cosa)
#         print(x2,y2)
#         painter.translate(x2,y2 )
#         painter.translate(self.position.x(), self.position.y())
#         painter.scale(4,4)

        painter.setPen(Qt.green)
        painter.drawLine(-300, 0, 300, 0)
        painter.drawLine(0, -300, 0, 300)
        rect = QRect(-64, -64, 128, 128)
        painter.setPen(Qt.black)
        # velocity vector
        painter.drawLine(0, 0, 100, 0)
        painter.drawLine(80, -20, 100, 0)
        painter.drawLine(80, 20, 100, 0) 
        painter.drawPixmap(-self.sprite.width()/2, -self.sprite.height()/2, self.sprite)
        painter.drawRect(rect)
#         rect2 = QRect(-64,-64,128,128)
#         painter.drawRect(rect2)
#         painter.resetTransform()
        painter.restore()
        painter.setPen(Qt.red)
#         painter.drawPixmap(0,0,self.sprite)
        
        
        
        
        
        