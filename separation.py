from rule import Rule
from PyQt5.Qt import QVector2D

class Separation(Rule):
    def __init__(self, coefficient):
        Rule.__init__(self, coefficient)
        self.name = "Separation rule"
        
    def algorithm(self, individuals, individual):
        sum_vector = QVector2D(0, 0)
        for i in individuals:
            if i is individual:
                continue
            tmp_vector = individual.position - i.position
            tmp_vector /= tmp_vector.lengthSquared()
            sum_vector += tmp_vector
        sum_vector *= (self.coefficient / (len(individuals) - 1))
        return sum_vector
#         individual.velocity += sum_vector
        