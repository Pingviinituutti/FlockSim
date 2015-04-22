from rule import Rule
from PyQt5.Qt import QVector2D

class Alignment(Rule):

    def __init__(self, coefficient):
        Rule.__init__(self, coefficient)
        self.name = "Alignment rule"
        
    def algorithm(self, individuals, individual):
        sum_vector = QVector2D(0, 0)
        for i in individuals:
            if i is individual:
                continue
            sum_vector += i.velocity
        sum_vector *= (self.coefficient / (len(individuals) - 1))
        individual.velocity += sum_vector
        
        
        