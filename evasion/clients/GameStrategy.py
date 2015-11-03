import websocket
import sys
import json
import math
from time import sleep
class GameStrategy(object):
    def __init__(self, role, ws, publisher, wall_limit, build_frequency):
        """docstring for __init__"""
        self.role = role
        self.ws = ws
        self.publisher = publisher
        self.first_move = True
        self.hunter_prev_move = (0, 0)
        self.prey_prev_move = (230, 200)
        self.last_wall_time = -1
        self.max_num_wall = wall_limit
        self.build_frequency = build_frequency

    def _send_to_server(self, command_dict):
        """docstring for _send_to_server"""
        json_string = json.dumps(command_dict)
        self.ws.send(json_string)
        return_msg = None
        if command_dict['command'] == "P" or command_dict['command'] == "W":
            return_msg = self.ws.recv()
        return return_msg

    def hunterStrategy(self):
        """docstring for hunterStrategy"""
        while self.ws.connected:
            if self.first_move:
                self._send_to_server({"command": "M"})
                self.first_move = False
            else:
                status = self.publisher.recv()
                status = json.loads(status)
                hunter_pos = status["hunter"]
                prey_pos = status["prey"]
                walls = status["walls"]
                time = status["time"]
                hunter_direction = self._get_direction(self.hunter_prev_move, hunter_pos)
                self._remove_walls(walls, hunter_pos)
                wall_check = self._time_to_build_wall(hunter_direction, hunter_pos, prey_pos)
                if time - self.last_wall_time > self.build_frequency and wall_check[0]:
                    self._build_entire_wall(wall_check[1])
                    time = self.last_wall_time
                self.hunter_prev_move = hunter_pos
                self._send_moving_message()
                sleep(0.1)

    def _remove_walls(self, walls, hunter_pos):
        """docstring for _remove_walls"""
        NS_dist = 500
        NS_closest_id = -1
        EW_dist = 500
        EW_closest_id = -1
        remove_ids = []
        for wall in walls:
            if wall["direction"] == [0, 1] or wall["direction"] == [0, -1]:
                hunter_dist = abs(wall["position"][0] - hunter_pos[0])
                if hunter_dist >= EW_dist:
                    remove_ids.append(wall["id"])
                else:
                    EW_dist = hunter_dist
                    if EW_closest_id != -1:
                        remove_ids.append(EW_closest_id)
                    EW_closest_id = wall["id"]
            else:
                hunter_dist = abs(wall["position"][1] - hunter_pos[1])
                if hunter_dist >= NS_dist:
                    remove_ids.append(wall["id"])
                else:
                    NS_dist = hunter_dist
                    if NS_closest_id != -1:
                        remove_ids.append(NS_closest_id)
                    NS_closest_id = wall["id"]
        if len(remove_ids) > 0:
            self._delete_walls(remove_ids)

    def prey_strategy(self):
        """docstring for preyStrategy"""
        while self.ws.connected:
            if self.first_move:
                pos = self._get_position()
                hunter_pos = pos["hunter"]
                prey_pos = pos["prey"]
                hunter_direction = self._get_direction(self.hunter_prev_move, hunter_pos)
                self._if_can_be_caught_change_direction(hunter_direction, hunter_pos, prey_pos)
                best_direction = self._get_best_move_direction(hunter_direction, hunter_pos[0] - prey_pos[0], hunter_pos[1] - prey_pos[1])
                self._send_moving_message(best_direction)
                self.first_move = False
                self.hunter_prev_move = hunter_pos
            else:
                i = 0
                while self.publisher.recv():
                    if i == 0:
                        i += 1
                        continue
                    pos = self._get_position()
                    hunter_pos = pos["hunter"]
                    prey_pos = pos["prey"]
                    hunter_direction = self._get_direction(self.hunter_prev_move, hunter_pos)
                    if self._if_can_be_caught_change_direction(hunter_direction, hunter_pos, prey_pos) != None:
                        best_direction = self._if_can_be_caught_change_direction(hunter_direction, hunter_pos, prey_pos)
                    else:
                        best_direction = self._get_best_move_direction(hunter_direction, hunter_pos[0] - prey_pos[0], hunter_pos[1] - prey_pos[1])
                    self._send_moving_message(best_direction)
                    sleep(0.1)
                    self.first_move = False
                    self.hunter_prev_move = hunter_pos
                    i = 0

    def _time_to_build_wall(self, hunter_direction, hunter_pos, prey_pos):
        if hunter_direction == "SE":
            if prey_pos[1] - hunter_pos[1] < 4 and prey_pos[1] - hunter_pos[1] > 0:
                return (True, "H")
            elif prey_pos[0] - hunter_pos[0] < 4 and prey_pos[0] - hunter_pos[0] > 0:
                return (True, "V")
        elif hunter_direction == "NW":
            if hunter_pos[1] - prey_pos[1] < 4 and hunter_pos[1] - prey_pos[1] > 0:
                return (True, "H")
            elif hunter_pos[0] - prey_pos[0] < 4 and hunter_pos[0] - prey_pos[0] > 0:
                return (True, "V")
        elif hunter_direction == "NE":
            if hunter_pos[1] - prey_pos[1] < 4 and hunter_pos[1] - prey_pos[1] > 0:
                return (True, "H")
            elif prey_pos[0] - hunter_pos[0] < 4 and prey_pos[0] - hunter_pos[0] > 0:
                return (True, "V")
        else:
            if prey_pos[1] - hunter_pos[1] < 4 and prey_pos[1] - hunter_pos[1] > 0:
                return (True, "H")
            elif hunter_pos[0] - prey_pos[0] < 4 and hunter_pos[0] - prey_pos[0] > 0:
                return (True, "V")
        return (False, "")

    def _if_can_be_caught_change_direction(self, hunter_direction, hunter_pos, prey_pos):
        if hunter_direction == "NW" or hunter_direction == "SE":
            distance = abs(prey_pos[0] - prey_pos[1] + hunter_pos[1] - hunter_pos[0]) / math.sqrt(1 + 1)
            if distance < 5 or abs(hunter_pos[1] - prey_pos[1]) < 5:
                if - hunter_pos[1] + prey_pos[1] + hunter_pos[0] > prey_pos[1]:
                    return "SW"
                else:
                    return "NE"
            if abs(hunter_pos[0] - prey_pos[0]) < 5 or abs(hunter_pos[1] - prey_pos[1]) < 5:
                if hunter_pos[0] < prey_pos[0]:
                    return "E"
                else:
                    return "W"
        else:
            distance = abs(prey_pos[0] + prey_pos[1] - hunter_pos[1] - hunter_pos[0]) / math.sqrt(1 + 1)
            if distance < 5:
                if hunter_pos[1] - prey_pos[1] + hunter_pos[0] > prey_pos[1]:
                    return "NW"
                else:
                    return "SE"
            if abs(hunter_pos[0] - prey_pos[0]) < 5 or abs(hunter_pos[1] - prey_pos[1]) < 5:
                if hunter_pos[0] < prey_pos[0]:
                    return "S"
                else:
                    return "N"

    def _get_best_move_direction(self, hunter_direction, relative_x, relative_y):
        if hunter_direction == 'NW':
            if relative_x > 0 and relative_y > 0:
                best_move = 'SE'
            else:
                best_move = 'NW'
        elif hunter_direction == 'NE':
            if relative_x < 0 and relative_y > 0:
                best_move = 'SW'
            else:
                best_move = 'NE'
        elif hunter_direction == 'SW':
            if relative_x > 0 and relative_y < 0:
                best_move = 'NE'
            else:
                best_move = "SW"
        else:
            if relative_x < 0 and relative_y < 0:
                best_move = 'NW'
            else:
                best_move = 'SE'
        return best_move

    def _get_direction(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] < pos2[1]:
            return "S"
        elif pos1[0] == pos2[0] and pos1[1] > pos2[1]:
            return "N"
        elif pos1[0] < pos2[0] and pos1[1] == pos2[1]:
            return "E"
        elif pos1[0] > pos2[0] and pos1[1] == pos2[1]:
            return "W"
        elif pos1[0] > pos2[0] and pos1[1] > pos2[1]:
            return "NW"
        elif pos1[0] < pos2[0] and pos1[1] > pos2[1]:
            return "NE"
        elif pos1[0] < pos2[0] and pos1[1] < pos2[1]:
            return "SE"
        else:#  pos1[0] > pos2[0] and pos1[1] < pos2[1]:
            return "SW"

    def _send_moving_message(self, direction=""):
        if direction == "":
            message = {"command": "M"}
        else:
            message = {"command": "M", "direction": direction}
        self._send_to_server(message)

    def _build_entire_wall(self, direction):
        message = {"command": "B", "wall": {"direction": direction}}
        self._send_to_server(message)

    def _delete_walls(self, wall_ids):
        message = {"command": "D", "wallIds": wall_ids}
        self._send_to_server(message)

    def _get_walls(self):
        message = {"command": "W"}
        json_string = self._send_to_server(message)
        obj = json.loads(json_string)
        walls = obj["walls"]
        return walls

    def _get_position(self):
        message = {"command": "P"}
        json_string = self._send_to_server(message)
        obj = json.loads(json_string)
        return obj

    def run(self):
        """docstring for run"""
        if self.role == "H":
            self.hunterStrategy()
        else:
            self.prey_strategy()


def main():
    """docstring for main"""
    publisher = websocket.create_connection("ws://localhost:1990")
    if sys.argv[1] == "H":
        role = "H"
        port = "1991"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
    else:
        role = 'P'
        port = "1992"
        url = "ws://localhost:" + port
        ws = websocket.create_connection(url)
    M = 5 # max number of wall for hunter
    N = 5 # wall building frequency limit

    if len(sys.argv) > 2:
        M = sys.argv[2]
        N = sys.argv[3]

    strategy = GameStrategy(role, ws, publisher, M, N)
    strategy.run()

if __name__ == '__main__':
    main()
