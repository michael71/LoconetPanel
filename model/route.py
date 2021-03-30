from model.constants import BtnState, RouteState
import config


def check_routes():
    btn1 = None
    btn2 = None
    # check for first active button
    for b in config.rtBtns:
        if b.state == BtnState.FIRST_SEL:
            btn1 = b
            break

    # check for second active button
    for b in config.rtBtns:
        if b.state == BtnState.SECOND_SEL:
            btn2 = b
            break

    if btn1 is not None and btn2 is not None:
        rt_found = False
        for rt in config.routes:
            if rt.btn1 == btn1.adr and rt.btn2 == btn2.adr:
                print("route found, from btn1=" + str(btn1.adr) + " to btn2=" + str(btn2.adr))
                rt_found = True
                # TODO set route
                # deactivate both buttons
                btn2.state = BtnState.NOT_SEL
                btn1.state = BtnState.NOT_SEL
                return

        if not rt_found:
            print("no route found from btn1="+ str(btn1.adr) + " to btn2=" + str(btn2.adr))
            btn2.state = BtnState.NOT_SEL

    return



def one_btn_selected():
    for b in config.rtBtns:
        if b.state == BtnState.FIRST_SEL:
            return True # at least one button is selected
    return False


class Route():

    def __init__(self, attr):
        self.state = RouteState.NOT_ACTIVE   # state is always known at start (not stored in Intellibox!)
        self.adr = int(attr['adr'].value)
        self.btn1 = int(attr['btn1'].value)
        self.btn2 = int(attr['btn2'].value)
        self.route = attr['route'].value
        self.sensors = attr['sensors'].value

    def __repr__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

    def __str__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

