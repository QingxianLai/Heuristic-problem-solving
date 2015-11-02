import websocket
import time


def main():
    ws = websocket.create_connection("ws://localhost:1991")
    while True:
        rec = None
        time.sleep(1)
        rec = ws.recv()
        if rec:
            print rec

if __name__ == '__main__':
    main()
