import websocket
import sys
import json


def main():
    """docstring for main"""
    role = "H"
    port = "1991"
    if len(sys.argv) > 1:
        role = sys.argv[1]
        if role == 'P':
            port = "1992"
    player_url = "ws://localhost:" + port
    ws = websocket.create_connection(player_url)

    server_url = "ws://localhost:1990"
    server_ws = websocket.create_connection(server_url)

    print "%s, Welcome!" % role

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
        print "==|| message sent: %s" % json_string
        ws.send(json_string)
        if pack['command'] == "P" or pack['command'] == "W":
            result = server_ws.recv()
            print "==|| Get message: %s" % result

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
