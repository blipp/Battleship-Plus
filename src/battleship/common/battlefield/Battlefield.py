from typing import List, Optional, Any, Dict, Tuple
from ..constants import Orientation, Direction, ErrorCode
from .battleship import Ship
""" class Battlefield
    The Battlefield is an abstract model of a battlefield for a single player.
    It contains of two matrix fields and the ship list of the responsible player.
"""


class Battlefield:

    def __init__(self, length: int, ships, ships_table: List[int]):
        self._length: int = length
        self._ships = ships
        self._ships_table: List[int] = ships_table
        self._ships_table_not_placed: List[int] = ships_table
        self._my_battlefield = [[0 for x in range(self._length)] for y in range(self._length)]
        self._enemy_battlefield = [[0 for x in range(self._length)] for y in range(self._length)]

    # move a ship one position further
    def move(self, ship_id, direction):
        x_pos, y_pos = self.get_move_coordinate(ship_id, direction)
        ship = self.get_ship(ship_id)
        if ship.move(direction):
            return True
        else:
            return False

    # enemy strike
    def strike(self, x_pos, y_pos):
        self._my_battlefield[x_pos][y_pos] = 2
        for ship in self._ships:
            if ship.is_ship_at_location(x_pos, y_pos):
                if ship.strike(x_pos, y_pos):
                    self._my_battlefield[x_pos][y_pos] = 1
                    return True
        # no hit
        return False

    # shoot at enemy battlefield
    def shoot(self, x_pos, y_pos):
        if self._enemy_battlefield[x_pos][y_pos] == 0 or self._enemy_battlefield[x_pos][y_pos] == 2:
            self._enemy_battlefield[x_pos][y_pos] = 1
            return True
        else:
            return False

    # place the ship
    def place(self, ship_id, x_pos, y_pos, orientation):
        ship = self.get_ship(ship_id)
        if ship.place(x_pos, y_pos, orientation):
            ship_type = ship.get_ship_type()
            if ship_type == "carrier":
                self._ships_table_not_placed[0] -= 1
            elif ship_type == "battleship":
                self._ships_table_not_placed[1] -= 1
            elif ship_type == "cruiser":
                self._ships_table_not_placed[2] -= 1
            elif ship_type == "destroyer":
                self._ships_table_not_placed[3] -= 1
            elif ship_type == "submarine":
                self._ships_table_not_placed[4] -= 1
            return True
        return False

    def no_ship_at_place(self, x_pos, y_pos):
        bound_x = [-1, 0, 1]
        bound_y = [-1, 0, 1]
        for ship in self._ships:
            for i in bound_x:
                for j in bound_y:
                    check_x = i + x_pos
                    check_y = j + y_pos
                    if ship.is_ship_at_location(check_x, check_y):
                        return False
        return True

    def no_ship_at_place_but(self, x_pos, y_pos, ship_id):
        bound_x = [-1, 0, 1]
        bound_y = [-1, 0, 1]
        for ship in self._ships:
            if not ship.get_ship_id() == ship_id:
                for i in bound_x:
                    for j in bound_y:
                        check_x = i + x_pos
                        check_y = j + y_pos
                        if ship.is_ship_at_location(check_x, check_y):
                            return False
        return True

    def no_strike_at_place(self, x_pos, y_pos):
        if self._my_battlefield[x_pos][y_pos] == 0 or self._my_battlefield[x_pos][y_pos] == 2:
            return True
        else:
            return False

    def no_hit_at_place(self, x_pos, y_pos):
        if self._enemy_battlefield[x_pos][y_pos] == 0 or self._enemy_battlefield[x_pos][y_pos] == 2:
            return True
        else:
            return False

    def no_border_crossing(self, x_pos, y_pos):
        if 0 <= x_pos < self._length and 0 <= y_pos < self._length:
            return True
        else:
            return False

    def placement_finished(self):
        for ship in self._ships:
            if not ship.is_placed():
                return False
        return True

    def ship_is_moveable(self, ship_id):
        ship = self.get_ship(ship_id)
        return not ship.is_hit()

    def ship_id_exists(self, ship_id):
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                return True
        return False

    def get_ship_coordinate(self, ship_id):
        ship = self.get_ship(ship_id)
        return ship.get_ship_coordinate()

    def get_move_coordinate(self, ship_id, direction):
        x_pos = 0
        y_pos = 0
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                ship_coordinates = ship.get_ship_coordinates()
                x_pos = ship_coordinates[0][0]
                y_pos = ship_coordinates[0][1]
                if direction == Direction.EAST:
                    x_pos += 1
                if direction == Direction.SOUTH:
                    y_pos += 1
                if direction == Direction.WEST:
                    x_pos -= 1
                if direction == Direction.NORTH:
                    y_pos -= 1
        return x_pos, y_pos

    def get_ship(self, ship_id):
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                return ship

    def count_ships(self):
        return len(self._ships)

    def calc_filled(self):
        result = 0
        for ship in self._ships:
            result = result + ship.get_ship_length()
        return result

    @property
    def ships(self):
        return self._ships_table

    @property
    def length(self):
        return self._length

    @property
    def ships_not_placed(self):
        return self._ships_table_not_placed

    def get_ship_from_location(self, x_pos, y_pos):
        for ship in self._ships:
            if ship.is_ship_at_location(x_pos, y_pos):
                return ship

    def get_ship_id_from_location(self, x_pos, y_pos):
        for ship in self._ships:
            if ship.is_ship_at_location(x_pos, y_pos):
                return ship.get_ship_id()

    def get_next_ship_id_to_place(self):
        for ship in self._ships:
            if not ship.is_placed():
                return ship.get_ship_id()

    def get_next_ship_id_by_type_to_place(self, ship_type):
        for ship in self._ships:
            if ship.get_ship_type() == ship_type and not ship.is_placed():
                return ship.get_ship_id()

    def get_ship_type_by_id(self, ship_id):
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                return ship.get_ship_type()

    def all_ships_sunk(self):
        for ship in self._ships:
            if not ship.is_sunk():
                return False
        return True

    def get_all_ship_states(self):
        ship_states = []
        for ship in self._ships:
            ship_states.append(ship.get_ship_state())
        return ship_states

    def get_all_ships_coordinates(self):
        ship_coordinates_list = []
        for ship in self._ships:
            if ship.is_placed():
                    ship_coordinates_list.append(ship.get_ship_coordinate())
        return ship_coordinates_list

    def get_ship_coordinates_by_id(self, ship_id):
        ship_coordinates_list = []
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                ship_coordinates_list.append(ship.get_ship_coordinate())
        return ship_coordinates_list

    def get_ship_state_with_type(self, ship_type):
        ship_state_list = []
        for ship in self._ships:
            if ship.is_placed():
                if ship.get_ship_type() == ship_type:
                    ship_state_list.append(ship.get_ship_coordinate(), ship.get_ship_orientation())
        return ship_state_list

    def get_moved_ship_hit_positions(self, ship_id):
        moved_to_hit_positions = []
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                for i in range(self._length):
                    for j in range(self._length):
                        if self._my_battlefield[i][j] == 2:
                            if ship.is_ship_at_location(i, j):
                                moved_to_hit_positions.append((i, j))
        return moved_to_hit_positions

    def shot_missed(self, x_pos, y_pos):
        self._enemy_battlefield[x_pos][y_pos] = 2

    def get_ship_orientation_by_id(self, ship_id):
        for ship in self._ships:
            if ship.get_ship_id() == ship_id:
                return ship._orientation
        return None