import abc

class Rule:
    __metaclass__ = abc.ABCMeta

    def __init__(self, coefficient):
        self.coefficient = coefficient
        
    def setCoefficient(self, coefficient):
        self.coefficient = coefficient
        
    @abc.abstractmethod
    def algorithm(self, individuals, individual):
        """Applies the algorithm to the individual"""
        return
        