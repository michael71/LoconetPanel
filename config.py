# config.py
#
# define some global flags and variables


trks = None  # list of all tracks
sens = None  # list of all sensors
turn = None  # list of all turnouts
signals = None
rtBtns = None
routes = None


# print statistical info about panel data
def print_statistics():
    print("main, #trks=" + str(len(trks)))
    print("main, #sens=" + str(len(sens)))
    print("main, #turn=" + str(len(turn)))
    print("main, #signals=" + str(len(signals)))
    print("main, #rt-buttons=" + str(len(rtBtns)))
    print("main, #routes=" + str(len(routes)))


def draw_all(qpainter, addr_flag, route_flag):
    # draw Tracks
    for t in trks:
        t.draw(qpainter, addr_flag)

    # draw Sensors
    for t in sens:
        t.draw(qpainter, addr_flag)

    # draw Turnouts (depend on t.state)
    for t in turn:
        t.draw(qpainter, addr_flag)

    # draw signals (depend on t.state)
    for t in signals:
        t.draw(qpainter, addr_flag)

    if route_flag:
        # draw route buttons
        for t in rtBtns:
            t.draw(qpainter, addr_flag)
