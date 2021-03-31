from model import ln_command
from model.constants import BtnState, RouteState, SensorRouteState, State
import config
from model.routebutton import reset_rtbtns
from model.sensor import set_sensors_route_state


def is_signal(adr):
    for s in config.signals:
        if s.adr == adr:
            return True
    return False


def get_active_route():
    for rt in config.routes:
        if rt.state == RouteState.ACTIVE:
            return rt
    return None


def check_routes(ln_interface):
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
        for rt in config.routes:
            if rt.btn1 == btn1.adr and rt.btn2 == btn2.adr:
                print("route found, from btn1=" + str(btn1.adr) + " to btn2=" + str(btn2.adr))
                rt.set(ln_interface)
                return # there should be a single route only from btn1 to a btn2 should
        # else no route found
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
        self.btn1 = int(attr['btn1'].value)  # address of btn1, not btn1 really
        self.btn2 = int(attr['btn2'].value)
        self.route = attr['route'].value
        self.sensors = attr['sensors'].value
        return

    def __repr__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

    def __str__(self):
        return "Route adr={}, btn1={} btn2= {}".format(self.adr, self.btn1, self.btn2)

    def set(self, ln_interface):
        print("setting route with adr="+str(self.adr))
        set_sensors_route_state(self.sensors, SensorRouteState.IN_ROUTE)
        # set turnouts and signals
        acc_val_pairs = self.route.split(';')
        print(acc_val_pairs)
        for p in acc_val_pairs:
            pa = p.split(',')
            lnstring = ln_command.set_accessory(int(pa[0]), int(pa[1]))
            if lnstring:
                ln_interface.send_message(lnstring)
        self.state = RouteState.ACTIVE
        return

    def reset(self, ln_interface):
        print("resetting route with adr="+str(self.adr))
        reset_rtbtns()
        set_sensors_route_state(self.sensors, SensorRouteState.NOT_IN_ROUTE)
        # reset signals, keep turnouts in current state
        acc_val_pairs = self.route.split(';')
        print(acc_val_pairs)
        for p in acc_val_pairs:
            pa = p.split(',')
            if is_signal(int(pa[0])):
                lnstring = ln_command.set_accessory(int(pa[0]), State.CLOSED)
                if lnstring:
                    ln_interface.send_message(lnstring)
        self.state = RouteState.NOT_ACTIVE
        return
