from rule import Rule
from PyQt5.Qt import QVector2D

class Cohesion(Rule):
    def __init__(self, coefficient):
        Rule.__init__(self, coefficient)
        self.name = "Cohesion rule"
        
    def algorithm(self, individuals, individual):
        sum_vector = QVector2D(0, 0)
        for i in individuals:
            if i is individual:
                continue
            sum_vector += i.position
            
        sum_vector /= (len(individuals) - 1)
        sum_vector -= individual.position
        sum_vector *= (self.coefficient)
        individual.velocity += sum_vector
        