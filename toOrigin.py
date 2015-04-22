from rule import Rule
from PyQt5.Qt import QVector2D

class toOrigin(Rule):

    def __init__(self, coefficient):
        Rule.__init__(self, coefficient)
        self.name = "To Origin rule"
        
    def algorithm(self, individuals, individual):
        sum_vector = -individual.position
        
        sum_vector *= self.coefficient
        return sum_vector
#         individual.velocity += sum_vector
        