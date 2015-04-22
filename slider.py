'''
Created on 22.4.2015

@author: Henrik
'''
from PyQt5.Qt import QSlider

class Slider(QSlider):

    def __init__(self, qorientation, qwidget, rule, accuracy):
        QSlider.__init__(self, qorientation, qwidget)
        self.rule = rule
        self.setMinimum(-1 * accuracy)
        self.setMaximum(1 * accuracy)
        
#     def valueChanged(self, value):
#         print("slider change event!")
#         self.rule.setCoefficient(value)
#         QSlider.valueChanged(self, value)
#         