from model.constants import State


class Route():

    def __init__(self, attr):
        self.state = State.CLOSED   # state is always known at start (not stored in Intellibox!)
        self.adr = int(attr['adr'].value)
        self.btn1 = int(attr['btn1'].value)
        self.btn2 = int(attr['btn2'].value)
        self.route = attr['route'].value
        self.sensors = attr['sensors'].value

    def __repr__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

    def __str__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

