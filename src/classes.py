import numpy as np
import json
from PyQt5 import QtWidgets, QtGui
import os.path
from xml.dom import minidom

# set the transform.rotate(...) to one of these --- flip does not mirror, it just rotates by 180 degrees. (-Jason)
SCHEM_ORIENTATIONS = {'upright': 0, 'CW1': 90, 'CCW1': -90, 'flip': 180}
# add the one that sets the second pin whichever direction you want the component to go. (-Jason)
PCB_ORIENTATIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


# class ComponentSVG:
#     def __init__(self, base_file_name="", base_xml=None, active_xml=None):
#         if active_xml == None:
#             if base_xml == None:
#                 self.active_xml = minidom.parse(base_file_name)
#             else:
#                 self.active_xml = base_xml
#         else:
#             self.active_xml = active_xml

#     # For filling in the pin to make it obvious it has been connected to.
#     def change_pin_state(self, pin_number, new_state):
#         # These are the two options: transparent or black - disconnected or connected.
#         fill_options = ["none", "#000000"]
#         fill = fill_options[new_state]

#         # Get a searchable xml from the svg file and find the circle (pin) objects
#         new_xml = self.active_xml
#         pins = new_xml.getElementsByTagName("circle")

#         # Split the style line into two sections: the fill section and the rest.
#         # Then get the current fill
#         style_line = pins[pin_number].attributes["style"].value
#         current_fill = style_line.split(';', 1)[0].split(':')[1]

#         # # This decides which element the new_fill will be based on the current_fill
#         # current_state = not current_fill == fill_options[0]
#         # new_fill = fill_options[not current_state]
#         # new_state = not current_state

#         style = f"fill:{fill};{style_line.split(';', 1)[1]}"
#         pins[pin_number].attributes["style"].value = style

#         # Update the active xml
#         self.active_xml = new_xml

#     # For debugging the xml output.
#     def print_svg_file(self, file_name):
#         with open(file_name, 'w') as f:
#             self.active_xml.writexml(f)

#     def to_dict(self):
#         svg_dict = {"active_xml": self.active_xml.toxml()}
#         return svg_dict


class Component:
    global SCHEM_ORIENTATIONS
    # The component type field is what determines which sprite will be used
    # and what component fields to pull from the .json database. As long as the
    # database has the dimensions corresponding to type: component type,
    # and the spritesheet has a picture for it, the component can be used. (-Jason)

    def __init__(self, id, label, num_pins, schem_position, schem_orientation, pcb_position, connections, svg_file_name):
        if self.valid_input({"id": id, "label": label, "schem_position": schem_position, "schem_orientation": schem_orientation}):
            self.id = id
            self.label = label
            self.num_pins = num_pins
            self.pin_states = [False for i in range(0, self.num_pins)]
            self.schem_position = schem_position
            self.schem_orientation = schem_orientation
            self.pcb_position = pcb_position
            self.connections = self.set_connections(connections)
            # self.svg_obj = ComponentSVG(
            #     base_file_name=svg_file_name)

    def valid_input(self, input_kwargs):
        for key in input_kwargs:
            if key == "id":
                if type(input_kwargs[key]) != int:
                    raise TypeError("Invalid id type")
                if input_kwargs[key] < 0:
                    raise ValueError("Invalid id value")
            elif key == "label":
                if type(input_kwargs[key]) != str:
                    raise TypeError("Invalid label type")
            elif key == "schem_position":
                if type(input_kwargs[key]) != list:
                    raise TypeError("Invalid schematic position type")
                if np.shape(input_kwargs[key]) != (2,):
                    raise ValueError("Invalid shape for schematic position")
            elif key == "schem_position":
                if type(input_kwargs[key]) != int:
                    raise TypeError("Invalid schematic orientation type")
                if not np.shape(input_kwargs[key]) in SCHEM_ORIENTATIONS.values:
                    raise ValueError("Invalid value for schematic orientation")
        return True

    def set_connections(self, connections):
        if len(connections) == 0:
            keys = [f"{self.id}_{pin_num}" for pin_num in range(
                0, self.num_pins)]
            vals = [[] for i in range(0, self.num_pins)]
            self.connections = {k: v for (k, v) in zip(keys, vals)}
        else:
            pin_ids = [[list(connections.keys())[0], str(that_pin_id)]
                       for that_pin_id in list(connections.values())[0]]
            for connection in pin_ids:
                self.connect(connection[0], connection[1])

    def set_schematic_pos(self, pos):
        self.schem_position = pos

    def connect(self, this_pin_id, that_pin_id):
        if this_pin_id in self.connections:
            self.connections[this_pin_id].append(that_pin_id)

            if len(self.connections) == 1:
                this_pin_num = this_pin_id.split("_")
                # self.active_svg_xml, self.pin_states[this_pin_num] = self.svg_obj.change_pin_state(
                #     this_pin_num, True)
                self.pin_states[this_pin_num] = True
        else:
            raise ValueError("Invalid pin id")

    def disconnect(self, this_pin_id, that_pin_id):
        if this_pin_id in self.connections:
            self.connections[this_pin_id].remove(that_pin_id)

            # If there aren't any more connections, update the image
            if len(self.connections) == 0:
                this_pin_num = this_pin_id.split("_")
                # self.active_svg_xml, self.pin_states[this_pin_num] = self.svg_obj.change_pin_state(
                #     this_pin_num, False)
                self.pin_states[this_pin_num] = False
        else:
            raise ValueError("Invalid pin id")

    # def get_svg_pin_position(self):
    #     raise NotImplementedError("Abstract method")

    # def get_svg_xml(self):
    #     return self.svg_obj.active_xml

    # def print_svg(self, file_name):
    #     self.svg_obj.print_svg_file(file_name)

    def edit_label(self, text=""):
        if text == "":
            raise ValueError("Invalid label text")
        self.label = text

    def draw(self):
        raise NotImplementedError("Abstract method")

    def to_string(self):
        return (f"component_type: {self.__class__.__name__}\n"
                f"id: {self.id}\n"
                f"label: {self.label}\n"
                f"num_pins: {self.num_pins}\n"
                f"schem_position: {self.schem_position}\n"
                f"schem_orientation: {self.schem_orientation} degrees\n"
                f"pcb_position: {self.pcb_position}\n"
                f"connections: {self.connections}\n")

    def to_dict(self):
        component_dict = {
            "id": self.id,
            "component_type": self.__class__.__name__,
            "label": self.label,
            "schem_position": self.schem_position,
            "schem_orientation": self.schem_orientation,
            "pcb_position": self.pcb_position,
            "connections": self.connections  # , "svg_obj": self.svg_obj.to_dict()
        }
        return component_dict


class Resistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Resistor.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class Capacitor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Capacitor.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class Inductor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Inductor.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class Diode(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Diode.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class Led(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Led.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10.025, 30], [150.025, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class Switch(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Switch.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


class VoltageSource(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/VoltageSource.svg"):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections, svg_file_name)
        self.svg_pin_positions = [[10, 30], [150, 30]]

    def get_svg_pin_position(self):
        return self.svg_pin_positions

    def draw(self):
        pass


# class Ground(Component):
#     def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}, svg_file_name="comp_img/Ground.svg"):
#         super().__init__(id, label, 1, schem_position,
#                          schem_orientation, pcb_position, connections, svg_file_name)
#         self.svg_pin_positions = [30, 150]

#     def get_svg_pin_position(self):
#         return self.svg_pin_positions

#     def draw(self):
#         pass


class Comment:
    def __init__(self, id, text="Type something here", position=[0, 0]):
        if self.valid_input({"id": id, "text": text, "position": position}):
            self.id = id
            self.text = text
            self.position = position

    def valid_input(self, input_kwargs):
        for key in input_kwargs:
            if key == "id":
                if type(input_kwargs[key]) != int:
                    raise TypeError("Invalid id type")
                if input_kwargs[key] < 0:
                    raise ValueError("Invalid id value")
            if key == "text":
                if type(input_kwargs[key]) != str:
                    raise TypeError("Invalid text type")
            if key == "position":
                if type(input_kwargs[key]) != list:
                    raise TypeError("Invalid position type")
                if len(input_kwargs[key]) != 2:
                    raise ValueError("invalid position shape")
        return True

    def edit_text(self, text):
        if self.valid_input({"text": text}):
            self.text = text

    def set_position(self, position):
        if self.valid_input({"position": position}):
            self.location = position

    def draw(self):
        pass

    def to_dict(self):
        comment_dict = {
            "id": self.id,
            "text": self.text,
            "position": self.position
        }
        return comment_dict


class GridNode:
    def __init__(self, pos, id="", taken=False):
        self.pos = pos
        self.id = id
        self.taken = taken
        self.g_cost = -1
        self.h_cost = -1

    # Using a heuristic based on the Chebyshev distance
    def h_cost(self, from, to):
        row_diff = abs(to[0] - from[0])
        col_diff = abs(to[1] - from[1])
        return max(row_diff, col_diff)

    def f_cost(self):
        return self.g_cost + self.h_cost


class PcbGrid:
    def __init__(self, dims=0, pin_placements_dict={}):
        self.dims = dims
        self.taken = {}
        self.nodes = self.initialize_grid(pin_placements_dict)

    def initialize_grid(self, pin_placements_dict):
        nodes = {}

        for i in range(0, self.dims):
            for j in range(0, self.dims):
                if [i, j] in pin_placements_dict
                nodes[f"[{i}, {j}]"]
        for pin_id, pos in pin_placements_dict.items():
            nodes[str(pos)] = GridNode(pos, pin_id, True)
            self.taken[str(pos)] = True

        return nodes

    def node_at(self, pos):
        if str(pos) in self.nodes.keys():
            return self.nodes(str(pos))
        else:
            return None

    def is_taken(self, pos):
        return taken[str(pos)]

    # def append_path_nodes(self):
    #     self.nodes

    def get_neighbors(self, node):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue

                neighbor_node_pos = [node.pos[0] + i, node.pos[1] + j]

                if neighbor_node_pos[0] >= 0 and neighbor_node_pos[0] < self.dims and neighbor_node_pos[1] >= 0 and neighbor_node_pos[1] < self.dims:
                    # Get whatever is at the location in the grid (existing node or none)
                    neighbor_node = self.node_at(neighbor_node_pos)
                    if neighbor_node != None:
                        neighbors.append(neighbor_node)
                    else:

                        self.nodes[str(neighbor_node_pos)] = GridNode(
                            neighbor_node_pos)
                        neighbors.append(self.nodes[str(neighbor_node_pos)])

        return neighbors

    def update_nodes(pin_placement_dict):
        self.taken.clear()
        self.nodes.clear()
        nodes = {}

        for pin_id, pos in pin_placements.items():
            nodes[str(pos)] = GridNode(taken[str(pos)], pos)
            self.taken[str(pos)] = True

    def g_cost(self, start_node, current_node):
        return 0

    def f_cost(self, node):
        grid_node = node_at(node.pos)
        return node_at(). + self.g_cost()


class Schematic:
    COMPONENT_CLASSES = {
        "Resistor": Resistor,
        "Capacitor": Capacitor,
        "Inductor": Inductor,
        "Diode": Diode,
        "Led": Led,
        "Switch": Switch,
        "VoltageSource": VoltageSource  # , "Ground": Ground
    }

    def __init__(self):
        self.components = {}
        self.comments = {}
        self.paths = {}
        self.pin_placement_dict = {}
        self.connections_list = []
        self.pcb_grid = PCBGrid()
        self.iteration_num = -1
        self.connection_num = -1
        self.last_runs_score = 1.0
        self.curr_runs_score = 0.0
        self.n_grid_spaces = 5
        self.grid_padding = 4
        self.max_iters = 10

    # Allows for setting the monte carlo params so it can continue (-Jason)
    def set_monte_carlo_parameters(self, n_grid_spaces=5, grid_padding=4, max_iters=10):
        self.n_grid_spaces = n_grid_spaces
        self.grid_padding = grid_padding
        self.max_iters = max_iters

    # Checks an id versus the list of component ids that exist and tells whether its unique (-Jason)
    def unique_component_id(self, id):
        if len(self.components) < 1:
            return True
        else:
            return not (id in [component_id for component_id in self.components])

    # Checks an id versus the list of comment ids that exist and tells whether its unique (-Jason)
    def unique_comment_id(self, id):
        if len(self.comments) < 1:
            return True
        else:
            return not (id in [comment_id for comment_id in self.comments])

    # I'm using this to set a new schematic to a loaded one (-Jason)
    def Schematic(self, schematic_dict):
        for component in schematic_dict["components"].values():
            self.add_component(component)

        for comment in schematic_dict["comments"].values():
            self.add_comment(comment)

        self.paths = schematic_dict["paths"]
        self.pin_placement_dict = schematic_dict["pin_placement_dict"]
        self.connections_list = schematic_dict["connections_list"]
        # self.connections_of_pins = schematic_dict["connections_of_pins"]
        self.iteration_num = schematic_dict["iteration_num"]
        self.connection_num = schematic_dict["connection_num"]
        self.last_runs_score = schematic_dict["last_runs_score"]
        self.curr_runs_score = schematic_dict["curr_runs_score"]
        self.set_monte_carlo_parameters(
            schematic_dict["n_grid_spaces"], schematic_dict["grid_padding"], schematic_dict["max_iters"])

    def add_component(self, component_dict):
        if self.unique_component_id(component_dict["id"]):
            if "connections" in component_dict:
                connections = component_dict.pop("connections")
            else:
                connections = {}

            component_type = component_dict["component_type"]
            component_dict.pop("component_type")
            component = self.COMPONENT_CLASSES[component_type](
                **component_dict)
            component.set_connections(connections)
            self.components[f"component_{component.id}"] = component
        else:
            raise ValueError("Component id not unique")

    def remove_component(self, component_id):
        self.components.pop(f"component_{component_id}")

    def get_component(self, component_id):
        return self.components[f"component_{component_id}"]

    def get_pin_position(self, pin_id):
        component_id, pin_num = pin_id.split('_')
        component_lookup_id = f"component_{component_id}"
        component = component.self.components[component_lookup_id]
        return component.get_pin_position()[int(pin_num)]

    def edit_label(self, component_id, new_text):
        self.components[f"component_{component_id}"].edit_label(new_text)

    def add_connection(self, component_1_pin_id, component_2_pin_id):
        component_1_id = int(component_1_pin_id.split("_")[0])
        component_2_id = int(component_2_pin_id.split("_")[0])
        self.components[f"component_{component_1_id}"].connect(
            component_1_pin_id, component_2_pin_id)
        self.components[f"component_{component_2_id}"].connect(
            component_2_pin_id, component_1_pin_id)

    def remove_connection(self, component_1_pin_id, component_2_pin_id):
        component_1_id = int(component_1_pin_id.split("_")[0])
        component_2_id = int(component_2_pin_id.split("_")[0])
        self.components[f"component_{component_1_id}"].disconnect(
            component_1_pin_id, component_2_pin_id)
        self.components[f"component_{component_2_id}"].disconnect(
            component_2_pin_id, component_1_pin_id)

    def set_component_schematic_pos(self, component_id, pos_x, pos_y):
        self.components[f"component_{component_id}"].set_schematic_pos(
            pos_x, pos_y)

    def print_all_components_strings(self):
        for component in self.components.values():
            print(component.to_string())

    def add_comment(self, comment_dict):
        if self.unique_comment_id(comment_dict["id"]):
            comment = Comment(**comment_dict)
            self.comments[f"comment_{comment.id}"] = comment
        else:
            raise ValueError("Comment id not unique")

    def edit_comment(self, comment_id, new_text):
        self.comments[f"comment_{comment_id}"].edit_text(new_text)

    def remove_comment(self, comment_id):
        self.comments.pop(f"comment_{comment_id}")

    def draw(self):
        for component in self.components.values():
            component.draw()
        for comment in self.comments.values():
            comment.draw()

    def to_dict(self):
        components = {}
        comments = {}
        schematic_dict = {}

        for component_id in self.components:
            components[component_id] = self.components[component_id].to_dict()

        for comment_id in self.comments:
            comments[comment_id] = self.comments[comment_id].to_dict()

        schematic_dict = {
            "components": components,
            "comments": comments,
            "paths": self.paths,
            "pin_placement_dict": self.pin_placement_dict,
            "connections_list": self.connections_list,
            # "connections_of_pins": self.connections_of_pins,
            "iteration_num": self.iteration_num,
            "connection_num": self.connection_num,
            "last_runs_score": self.last_runs_score,
            "curr_runs_score": self.curr_runs_score,
            "n_grid_spaces": self.n_grid_spaces,
            "grid_padding": self.grid_padding,
            "max_iters": self.max_iters
        }

        return schematic_dict

    def save(self, file_name):
        schematic_dict = self.to_dict()
        fn = f"{file_name}.json"
        if not os.path.exists(fn):
            with open(fn, 'x') as f:
                json.dump(schematic_dict, f)
        else:
            i = 0
            fn = f"{file_name}({i}).json"
            while os.path.exists(fn):
                if i > 254:
                    raise FileExistsError(
                        f"\"{file_name}.json\" exists and there are too many with its base name (255)")
                i += 1
                fn = f"{file_name}({i}).json"
            with open(fn, 'x') as f:
                json.dump(schematic_dict, f)

    def overwrite_save(self, file_name):
        schematic_dict = self.to_dict()
        fn = f"{file_name}.json"
        with open(fn, 'w') as f:
            json.dump(schematic_dict, f)

    def load(self, file_name):  # need to implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic) (-Jason)
        if os.path.exists(file_name):
            f = open(file_name, "r")
            schematic_dict = json.load(f)
            self.Schematic(schematic_dict)
        # notify user that file does not exist and ask if they want to reenter a filename (-Jason)
        else:
            raise FileNotFoundError(f"No file \"{file_name}\"")

    # LOOK AT force base graph layout algorithms as an alternative to this (-Jason)
    # Metropolis' Monte Carlo method. (-Jason)
    def monte_carlo(self, max_iters):
        # Might not need to do this first one - just set last run's score to infinity and this runs score to zero then do the loop? (-Jason)
        # Create backup just in case
        self.overwrite_save("tmp_monte_carlo.json")

        # run first iteration
        self.paths.clear()
        # First get random layout
        self.randomize_layout()
        # Next, setup a few lookup lists
        self.initialize_pin_placement_dict()
        self.initialize_connections_list()
        self.initialize_pcb_grid()
        # Lastly, get the paths.
        # paths will be a dict whos keys are "startId:goalId" and the values
        # correspond to dicts of info for that path (length; grid points;
        # and maybe max x, min x, max y, min y)
        paths = self.run_a_star()

        # Set the last run's score to inf
        self.last_runs_score = np.inf
        # Calculate this run's score based on average/total path length
        # and pcb surface area (obviously including the paths)
        self.curr_runs_score = self.calculate_score(
            paths)

        # run the subsequent iterations up until the score is high enough or we've reached the max_iters
        self.iteration_num = 1
        while np.subtract(self.curr_runs_score, self.last_runs_score) > .3 and self.iteration_num < max_iters:
            self.last_runs_score = self.curr_runs_score
            self.paths.clear()
            self.pin_placement_dict.clear()
            self.connections_list.clear()
            self.connections_of_pins.clear()

            self.randomize_layout()
            self.initialize_pin_placement_dict()
            self.initialize_connections_list()
            self.update_pcb_grid()
            paths = self.run_a_star()

            self.curr_runs_score = self.calculate_score(
                paths)
            self.iteration_num += 1

        self.paths = paths

    def not_allowed_pcb_spots(self):
        not_allowed = []

        # Append existing components to the not allowed list.
        for component in self.components.values():
            if component.pcb_position != []:
                not_allowed.append(component.pcb_position[0])
                not_allowed.append(component.pcb_position[1])

        # Append any path points to the not allowed list for use in
        # A*.
        if len(self.paths) > 0:
            for path in self.paths:
                if "grid_points" in path.keys():
                    for grid_point in path["grid_points"]:
                        not_allowed.append(grid_point)

        return not_allowed

    def get_pin1_pos(self):
        pin1_pos = [int(np.floor(np.random.rand() * self.n_grid_spaces)),
                    int(np.floor(np.random.rand() * self.n_grid_spaces))]
        return pin1_pos

    def get_pin2_pos(self, pin1_pos):
        global PCB_ORIENTATIONS
        possible_orientations = PCB_ORIENTATIONS.copy()
        rn_orient = int(np.floor(np.random.rand() * 4))

        # topleft corner
        if pin1_pos[0] == 0 and pin1_pos[1] == 0:
            rn_orient = int(np.floor(np.random.rand() * 2))
            possible_orientations.remove([-1, 0])
            possible_orientations.remove([0, -1])
        # topright corner
        elif pin1_pos[0] == 0 and pin1_pos[1] == self.n_grid_spaces - 1:
            rn_orient = int(np.floor(np.random.rand() * 2))
            possible_orientations.remove([0, 1])
            possible_orientations.remove([-1, 0])
        # bottomright corner
        elif pin1_pos[0] == self.n_grid_spaces - 1 and pin1_pos[1] == self.n_grid_spaces - 1:
            rn_orient = int(np.floor(np.random.rand() * 2))
            possible_orientations.remove([1, 0])
            possible_orientations.remove([0, 1])
        # bottomleft corner
        elif pin1_pos[0] == self.n_grid_spaces - 1 and pin1_pos[1] == 0:
            rn_orient = int(np.floor(np.random.rand() * 2))
            possible_orientations.remove([0, -1])
            possible_orientations.remove([1, 0])
        # left edge
        elif pin1_pos[0] * pin1_pos[1] == 0 and pin1_pos[1] == 0:
            rn_orient = int(np.floor(np.random.rand() * 3))
            possible_orientations.remove([0, -1])
        # top edge
        elif pin1_pos[0] * pin1_pos[1] == 0 and pin1_pos[0] == 0:
            rn_orient = int(np.floor(np.random.rand() * 3))
            possible_orientations.remove([-1, 0])
        # right edge
        elif pin1_pos[1] == self.n_grid_spaces - 1:
            rn_orient = int(np.floor(np.random.rand() * 3))
            possible_orientations.remove([0, 1])
        # bottom edge
        elif pin1_pos[0] == self.n_grid_spaces - 1:
            rn_orient = int(np.floor(np.random.rand() * 3))
            possible_orientations.remove([1, 0])
        pin2_pos = np.add(pin1_pos, possible_orientations[rn_orient]).tolist()

        return pin2_pos

    def get_valid_spot(self, not_allowed_pcb_spots):
        rn_pos_1 = self.get_pin1_pos()
        rn_pos_2 = self.get_pin2_pos(rn_pos_1)
        rn_pos = [rn_pos_1, rn_pos_2]

        i = 0
        while rn_pos[0] in not_allowed_pcb_spots or rn_pos[1] in not_allowed_pcb_spots:
            # print("redoing pin1 and pin2")
            rn_pos_1 = self.get_pin1_pos()
            rn_pos_2 = self.get_pin2_pos(rn_pos_1)
            rn_pos = [rn_pos_1, rn_pos_2]

            i += 1
        return rn_pos

    # Will make a layout where no pins overlap
    # and adjusted by some padding (-Jason)
    def randomize_layout(self):
        not_allowed_pcb_spots = []
        for component in self.components.values():
            rn_spot = self.get_valid_spot(not_allowed_pcb_spots)
            rn_spot = np.add(
                rn_spot, [int(self.grid_padding/2), int(self.grid_padding)]).tolist()
            component.pcb_position = rn_spot

    # This gets a position list for every pin
    def initialize_pin_placement_dict(self):
        pin_placement_dict = []
        for component in self.components.values():
            pin_ids = list(component.connections.keys())
            for pin_id, pos in zip(pin_ids, component.pcb_position):
                pin_placement_dict |= {pin_id: [pos, connection]}
        self.pin_placement_dict = pin_placement_dict

    def initialize_pcb_grid(self):
        self.pcb_grid = PcbGrid(
            self.n_grid_spaces + self.grid_padding, {}, self.pin_placement_dict)

    def update_pcb_grid(self):
        self.pcb_grid.update_nodes(self.pin_placement_dict)

    # This gets the connections into a single list
    def initialize_connections_list(self):
        connections_list = []
        for component in self.components.values():
            for pin_id, connections in component.connections.items():
                for connection in connections:
                    if len(connections_list) > 0:
                        if not [connection, pin_id] in connections_list:
                            connections_list.append([pin_id, connection])
                    else:
                        connections_list.append([pin_id, connection])

        self.connections_list = connections_list

    # # This creates the start/goal lists in one list
    # def initialize_connections_of_pins_list(self):
    #     pin_placements = self.pin_placement_dict
    #     connections = self.connections_list

    #     connections_of_pins = []

    #     for start_id, goal_id in connections:
    #         connections_of_pins[0].append({start_id: pin_placements[start_id]})
    #         connections_of_pins[1].append({goal_id: pin_placements[goal_id]})

    #     self.connections_of_pins = zip(
    #         connections_of_pins[0], connections_of_pins[1])

    # def calculate_score(self, paths):
    #     total_path_length = 0
    #     total_area = 1

    #     for path in paths:
    #         total_path_length += path["length"]

    #     total_area = abs(min_x - max_x) * abs(min_y - max_y)

    def run_a_star(self):
        paths = []

        # Terrible list comprehension that says get a list of the grid_nodes from pcb_grid that are at the locations denoted by each pair of connected pin_ids
        start_goal_node_list = [[self.pcb_grid.node_at(self.pin_placement_dict[id_1]), self.pcb_grid.node_at(
            self.pin_placement_dict[id_2])] for id_1, id_2 in self.connections_list]
        for start, goal in start_goal_node_list:
            path = self.a_star(start, goal)
            paths.append(path)

        return paths_dict

    def reconstruct_path(self, came_from, current):
        pass

    # A* as defined by Sebastian Lague (-Jason)
    # Pseudo-code:
    # OPEN //the set of nodes to be evaluated
    # CLOSED //the set of nodes already evaluated
    # add the start node to OPEN
    #
    # loop
    #   current = node in OPEN with the lowest f_cost
    #   remove current from OPEN
    #   add current to CLOSED
    #
    #   if current is the target node //path has been found
    #       return
    #
    #   foreach neighbour of the current node
    #       if neighbour is not traversable or neighbour is in CLOSED
    #           skip to the next neighbour
    #
    #       if new path to neighbour is shorter OR neighbour is not in OPEN
    #           set f_cost of neighbour
    #           set parent of neighbour to current
    #           if neighbour is not in OPEN
    #               add neighbour to OPEN

    # start and goal look like {"pin_id": [x, y]}
    def a_star(self, start, goal):
        # node_dict will have g_costs and h_costs for previously looked at nodes - for lookup if I use this...
        path_dict = {"path_id": f"{}:{}", "length": -1, "grid_nodes": []}
        open_nodes = [start]
        closed_nodes = []

        while len(open_nodes) > 0:
            this_node = open_nodes[0]
            for that_node in open_nodes[1:]:
                if (that_node.f_cost() < this_node.f_cost()) or (that_node.f_cost() == this_node.f_cost() and that_node.h_cost < this_node.h_cost):
                    this_node = that_node

            open_nodes.remove(this_node)
            closed_nodes.append(this_node)

            if this_node == goal:
                break

            for neighbor in PcbGrid.get_neighbors(this_node):
                if neighbor
