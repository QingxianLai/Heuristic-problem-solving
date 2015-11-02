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
                

if __name__ == '__main__':
    main()
