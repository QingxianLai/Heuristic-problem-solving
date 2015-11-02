import websocket
import sys
import json


def main():
    """docstring for main"""
    publisher = websocket.create_connection("ws://localhost:1990")
    if sys.argv[1] == "H":
        role = "H"
        port = "1991"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
        # prey = websocket.create_connection("ws://localhost:1992")
    else:
        role = 'P'
        port = "1992"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
        # hunter = websocket.create_connection("ws://localhost:1991")

    print "%s, Welcome!" % role
    test = None

    while True:
        times = 1
        if role == "H":
            times = 2
        for i in range(times):
            a = raw_input("command >")
            pack = {}
            if a == "B":
                wall_length = raw_input("wall_lenth >")
                wall_direct = raw_input("wall direction >")
                pack = {"command": "B", "wall": {"length": wall_length,
                                                 "direction": wall_direct}}
            elif a == "D":
                wall_index = raw_input("wall index>")
                pack = {"command": "D", "wallindex": wall_index}
            elif a == "M":
                if role == "P":
                    direction = raw_input("move direction>")
                    pack = {"command": "M", "direction": direction}
                else:
                    pack = {"command": "M"}
            elif a == "P":
                pack = {"command": "P"}
            elif a == "W":
                pack = {"command": "W"}
            else:
                print "unknown command"
                continue
            json_string = json.dumps(pack)
            print "==|| message sent: %s" % json_string
            ws.send(json_string)
            test = 1

            if a == "P" or a == "W":
                result = ws.recv()
                print "==|| Get message: %s" % result
            # elif test != None:
            #     result = publisher.recv()
            #     print result

def server_on_message(ws, e):
    """docstring for server_on_message"""
    print e

def hunter_on_message(ws, e):
    """docstring for server_on_message"""
    print e

def prey_on_message(ws, e):
    """docstring for server_on_message"""
    print e

def on_open(ws):
    print "hello"

def h_on_open(ws):
    print "hello, H"

def p_on_open(ws):
    print "hello, P"

def main2():
    """docstring for main2"""
    role = "H"
    port = "1991"
    if len(sys.argv) > 1:
        role = sys.argv[1]
        if role == 'P':
            port = "1992"

    # websocket.enableTrace(True)
    HSocket = websocket.WebSocketApp("ws://localhost:1991", on_open = h_on_open, on_message = hunter_on_message)
    print "<2>"
    PSocket = websocket.WebSocketApp("ws://localhost:1992", on_open = p_on_open, on_message = prey_on_message)
    print "<3>"
    mainSocket = websocket.WebSocketApp("ws://localhost:1990", on_open = on_open, on_message = server_on_message)
    print "<1>"

    # HSocket.run_forever()
    # mainSocket.run_forever()
    # PSocket.run_forever()

    while True:
        a = raw_input("command >")
        pack = {}
        if a == "B":
            wall_length = raw_input("wall_lenth >")
            wall_direct = raw_input("wall direction >")
            pack = {"command": "B", "wall": {"length": wall_length,
                                             "direction": wall_direct}}
        elif a == "D":
            wall_index = raw_input("wall index>")
            pack = {"command": "D", "wallindex": wall_index}
        elif a == "M":
            if role == "P":
                direction = raw_input("move direction>")
                pack = {"command": "M", "direction": direction}
            else:
                pack = {"command": "M"}
        elif a == "P":
            pack = {"command": "P"}
        elif a == "W":
            pack = {"command": "W"}
        else:
            print "unknown command"
            continue
        json_string = json.dumps(pack)
        HSocket.send(json_string)


if __name__ == '__main__':
    main()
