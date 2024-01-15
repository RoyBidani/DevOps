# phase 1:
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

# phase2:

class CloudService:
    def __init__(self):
        self.machines = {}

    def start(self, machine_id, type):
        if machine_id not in self.machines:
            self.machines[machine_id] = Machine(type)
        else:
            print(f"Error: Machine with ID {machine_id} already exist.")

    def stop(self, machine_id):
        if machine_id in self.machines:
            machine = self.machines[machine_id]
            machine.stop_machine()
        else:
            print(f"Error: Machine with ID {machine_id} does not exist.")

    def prices(self):
        total = 0
        for machine in self.machines.values():
            cost = machine.calculate_cost()
            total += cost
        return total


cloud_service = CloudService()

cloud_service.start("A", 1)
cloud_service.start("B", 1)
cloud_service.start("C", 1)

time.sleep(60)
cloud_service.stop("B")

total = cloud_service.prices()
print(f"Total prices: {total}")






























