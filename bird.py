# from PyQt5.QtGui import QVector2D
from PyQt5.QtGui import QPainter, QColor, QPixmap, QFont
from individual import Individual
import math

from PyQt5.QtCore import Qt, QRect

class Bird(Individual):
    
    max_speed = 100
    max_turn_rate = 30 # degrees

    def __init__(self, id, x, y, velo_x, velo_y):
#         super(Individual, self).__init__(x, y, velo_x, velo_y)
        Individual.__init__(self, id, x, y, velo_x, velo_y)
        self.sprite = QPixmap()
        self.sprite.load('bird', 'png')
        
    def move(self, time):
        if self.velocity.length() > self.max_speed:
            self.velocity /= 1.1 #(self.velocity.length() * self.max_speed)
        Individual.move(self, time)
        
    def draw(self, painter, screen_size):
#         print(self.position)
#         painter.translate(-self.sprite.width()/2, -self.sprite.height()/2)
        painter.translate(self.position.x(), self.position.y())
        
        # calculate angle of bird
        self.calculateAngle()
#         print(self.position, end=', velocity: ')
#         print(self.velocity, end=', angle: ')
#         print(self.angle)
        painter.rotate(self.angle)

        painter.setPen(Qt.green)
        painter.drawLine(-300, 0, 300, 0)
        painter.drawLine(0, -300, 0, 300)
        rect = QRect(-64, -64, 128, 128)
        painter.setPen(Qt.red)
        
        # velocity vector
        painter.drawLine(0, 0, 100, 0)
        painter.drawLine(80, -20, 100, 0)
        painter.drawLine(80, 20, 100, 0) 
        painter.drawPixmap(-self.sprite.width()/2, -self.sprite.height()/2, self.sprite)
        painter.drawRect(rect)
        painter.rotate(90)
        painter.setFont(QFont('Decorative', 10))
        painter.drawText(-self.sprite.width()/2, self.sprite.height()/2, str(self.id))
        
        
        
        
        
        