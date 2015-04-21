from PyQt5.QtGui import QVector2D
from PyQt5.QtGui import QPainter, QColor, QPixmap
from individual import Individual

class Bird(Individual):
    
    max_speed = 10
    max_turn_rate = 30 # degrees

    def __init__(self, id, x, y, velo_x, velo_y):
#         super(Individual, self).__init__(x, y, velo_x, velo_y)
        Individual.__init__(self, id, x, y, velo_x, velo_y)
        self.sprite = QPixmap()
        self.sprite.load('bird', 'png')
        
    def move(self, simulation):
        if self.velocity.length() > self.max_speed:
            self.velocity /= (self.velocity.length()/10)
        Individual.move(self, simulation)
        
    def draw(self, painter):
#         print(self.position)
        painter.drawPixmap(self.position.x(), self.position.y(), self.sprite)
#         painter.drawPixmap(0,0,self.sprite)
        
        
        
        
        
        