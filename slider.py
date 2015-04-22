'''
Created on 22.4.2015

@author: Henrik
'''
from PyQt5.Qt import QSlider

class Slider(QSlider):

    def __init__(self, qorientation, qwidget, name):
        QSlider.__init__(self, qorientation, qwidget)
        self.name = name
        