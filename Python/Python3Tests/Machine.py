import time
from datetime import datetime


class Machine:
    def __init__(self, type):
        self.type = type
        self.start = datetime.now()
        self.end = None
        if type == 1:
            self.cost = 2
        else:
            self.cost = 5

    def start_machine(self):
        self.start = datetime.now()

    def stop_machine(self):
        self.end = datetime.now()

    def calculate_cost(self):
        if self.end:
            end = self.end
        else:
            end = datetime.now()
        time = (end - self.start).total_seconds() / 60
        cost = time * self.cost
        return cost



























