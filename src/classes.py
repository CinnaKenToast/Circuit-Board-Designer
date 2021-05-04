import numpy as np
import json
from PyQt5 import QtWidgets, QtGui
import os.path
from xml.dom import minidom

# set the transform.rotate(...) to one of these --- flip does not mirror, it just rotates by 180 degrees. (-Jason)
SCHEM_ORIENTATIONS = {'upright': 0, 'CW1': 90, 'CCW1': -90, 'flip': 180}
# add the one that sets the second pin whichever direction you want the component to go. (-Jason)
PCB_ORIENTATIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


class ComponentSVG:
    def __init__(self, base_file_name="", base_xml=None, active_xml=None):
        if active_xml == None:
            if base_xml == None:
                self.active_xml = minidom.parse(base_file_name)
            else:
                self.active_xml = base_xml
        else:
            self.active_xml = active_xml

    # For filling in the pin to make it obvious it has been connected to.
    def change_pin_state(self, pin_number, new_state):
        # These are the two options: transparent or black - disconnected or connected.
        fill_options = ["none", "#000000"]
        fill = fill_options[new_state]

        # Get a searchable xml from the svg file and find the circle (pin) objects
        new_xml = self.active_xml
        pins = new_xml.getElementsByTagName("circle")

        # Split the style line into two sections: the fill section and the rest.
        # Then get the current fill
        style_line = pins[pin_number].attributes["style"].value
        current_fill = style_line.split(';', 1)[0].split(':')[1]

        # # This decides which element the new_fill will be based on the current_fill
        # current_state = not current_fill == fill_options[0]
        # new_fill = fill_options[not current_state]
        # new_state = not current_state

        style = f"fill:{fill};{style_line.split(';', 1)[1]}"
        pins[pin_number].attributes["style"].value = style

        # Update the active xml
        self.active_xml = new_xml

    # For debugging the xml output.
    def print_svg_file(self, file_name):
        with open(file_name, 'w') as f:
            self.active_xml.writexml(f)

    def to_dict(self):
        svg_dict = {"active_xml": self.active_xml.toxml()}
        return svg_dict


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
            self.svg_obj = ComponentSVG(
                base_file_name=svg_file_name)

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
                self.active_svg_xml, self.pin_states[this_pin_num] = self.svg_obj.change_pin_state(
                    this_pin_num, True)
                self.pin_states[this_pin_num] = True
        else:
            raise ValueError("Invalid pin id")

    def disconnect(self, this_pin_id, that_pin_id):
        if this_pin_id in self.connections:
            self.connections[this_pin_id].remove(that_pin_id)

            # If there aren't any more connections, update the image
            if len(self.connections) == 0:
                this_pin_num = this_pin_id.split("_")
                self.active_svg_xml, self.pin_states[this_pin_num] = self.svg_obj.change_pin_state(
                    this_pin_num, False)
                self.pin_states[this_pin_num] = False
        else:
            raise ValueError("Invalid pin id")

    def get_svg_pin_position(self):
        raise NotImplementedError("Abstract method")

    def get_svg_xml(self):
        return self.svg_obj.active_xml

    def print_svg(self, file_name):
        self.svg_obj.print_svg_file(file_name)

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
            "connections": self.connections
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

    def to_string(self):
        return (f"id: {self.id}\n"
                "text: {self.text}\n"
                "position: {self.position}\n")


class GridNode:
    def __init__(self, pos, taken):
        self.pos = pos
        self.taken = taken
        self.g_cost = -1
        self.h_cost = -1
        self.parent = None

    def f_cost(self):
        return self.g_cost + self.h_cost


class PcbGrid:
    def __init__(self, dims, obstructions):
        self.dims = dims
        self.obstructions = obstructions
        self.nodes = self.initialize_grid(obstructions)

    def initialize_grid(self, obstructions):
        nodes = {}

        for i in range(0, self.dims):
            for j in range(0, self.dims):
                pos = [i, j]
                if not (pos in obstructions):
                    nodes[str(pos)] = GridNode(pos, False)
                else:
                    nodes[str(pos)] = GridNode(pos, True)

        return nodes

    def node_at(self, pos):
        if str(pos) in self.nodes.keys():
            return self.nodes[str(pos)]

    def get_neighbors(self, node):
        neighbors = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                neighbor_node_pos = [node.pos[0] + i, node.pos[1] + j]
                if neighbor_node_pos[0] >= 0 and neighbor_node_pos[0] < self.dims and neighbor_node_pos[1] >= 0 and neighbor_node_pos[1] < self.dims:
                    neighbor_node = self.node_at(neighbor_node_pos)
                    neighbors.append(neighbor_node)

        return neighbors

    # The heuristic from Sebastian Lague (i is for rows (y), j is for columns (x))
    def get_distance(self, from_node, goal_node):
        di = abs(goal_node[0] - from_node[0])
        dj = abs(goal_node[1] - from_node[1])

        if dj > di:
            return 14 * di + 10 * (dj - di)
        return 14 * dj + 10 * (di - dj)

    def remake_path(self, start_node, goal_node):
        path = []
        this_node = goal_node

        while this_node != start_node:
            path.append(this_node)
            this_node = this_node.parent
        path = path.reverse()

        return path

    # A* as defined by Sebastian Lague (-Jason)
    def a_star(self, start_node, goal_node):
        path_dict = {}
        open_nodes = [start_node]
        closed_nodes = []

        while len(open_nodes) > 0:
            # find node with lowest f_cost
            this_node = open_nodes[0]
            for that_node in open_nodes[1:]:
                if (that_node.f_cost() < this_node.f_cost()) or (that_node.f_cost() == this_node.f_cost() and that_node.h_cost < this_node.h_cost):
                    this_node = that_node

            # place node in closed list
            open_nodes.remove(this_node)
            closed_nodes.append(this_node)

            test1 = start_node in closed_nodes
            test2 = goal_node in closed_nodes

            if this_node == goal_node:
                break

            for neighbor in self.get_neighbors(this_node):
                if (not neighbor.taken) or (neighbor in closed_nodes):
                    continue

                tentative_g_cost = this_node.g_cost + \
                    self.get_distance(this_node.pos, neighbor.pos)
                if (tentative_g_cost < neighbor.g_cost) or not (neighbor in open_nodes):
                    neighbor.g_cost = tentative_g_cost
                    neighbor.h_cost = self.get_distance(
                        neighbor.pos, goal_node.pos)
                    neighbor.parent = this_node

                    if not(neighbor in open_nodes):
                        open_nodes.append(neighbor)

        start_node = closed_nodes[closed_nodes.index(start_node)]
        goal_node = closed_nodes[closed_nodes.index(start_node)]
        path_dict["grid_nodes"] = self.remake_path(start_node, goal_node)
        path_dict["length"] = goal_node.g_cost

        return path_dict


class Schematic:
    COMPONENT_CLASSES = {
        "Resistor": Resistor,
        "Capacitor": Capacitor,
        "Inductor": Inductor,
        "Diode": Diode,
        "Led": Led,
        "Switch": Switch,
        "VoltageSource": VoltageSource
    }

    def __init__(self):
        self.components = {}
        self.comments = {}
        self.paths = []
        self.pin_placement_dict = {}
        self.connections_list = []
        self.iteration_num = -1
        self.connection_num = -1
        self.area_weight = .5
        self.path_length_weight = .5
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
        self.pcb_grid = schematic_dict["pcb_grid"]
        self.iteration_num = schematic_dict["iteration_num"]
        self.connection_num = schematic_dict["connection_num"]
        self.last_runs_score = schematic_dict["last_runs_score"]
        self.curr_runs_score = schematic_dict["curr_runs_score"]
        self.area_weight = schematic_dict["area_weight"]
        self.path_length_weight = schematic_dict["path_length_weight"]
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
        component = self.components[component_lookup_id]
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

    def set_component_schematic_pos(self, component_id, pos):
        self.components[f"component_{component_id}"].set_schematic_pos(
            pos)

    def print_all_components_strings(self):
        for component in self.components.values():
            print(component.to_string())

    def print_all_comments_strings(self):
        for comment in self.comments.values():
            print(comment.to_string())

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
            "iteration_num": self.iteration_num,
            "connection_num": self.connection_num,
            "last_runs_score": self.last_runs_score,
            "curr_runs_score": self.curr_runs_score,
            "area_weight": self.area_weight,
            "path_length_weight": self.path_length_weight,
            "n_grid_spaces": self.n_grid_spaces,
            "grid_padding": self.grid_padding,
            "max_iters": self.max_iters
        }

        return schematic_dict

    def save(self, file_name):
        schematic_dict = self.to_dict()
        fn = f"{file_name}"
        if not os.path.exists(fn):
            with open(fn, 'x') as f:
                json.dump(schematic_dict, f)
        else:
            i = 0
            fn = f"{file_name}({i})"
            while os.path.exists(fn):
                if i > 254:
                    raise FileExistsError(
                        f"\"{file_name}\" exists and there are too many with its base name (255)")
                i += 1
                fn = f"{file_name}({i})"
            with open(fn, 'x') as f:
                json.dump(schematic_dict, f)

    def overwrite_save(self, file_name):
        schematic_dict = self.to_dict()
        fn = f"{file_name}"
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
    # def monte_carlo(self, max_iters):
    #     # Might not need to do this first one - just set last run's score to infinity and this runs score to zero then do the loop? (-Jason)
    #     # Create backup just in case
    #     self.overwrite_save("tmp_monte_carlo.json")

    #     # run first iteration
    #     self.paths.clear()
    #     # First get random layout
    #     self.randomize_layout()
    #     # Next, setup a few lookup lists
    #     self.initialize_pin_placement_dict()
    #     self.initialize_connections_list()
    #     # Lastly, get the paths.
    #     # paths will be a dict whos keys are "startId:goalId" and the values
    #     # correspond to dicts of info for that path (length; grid points;
    #     # and maybe max x, min x, max y, min y)
    #     paths = self.run_a_star()

    #     # Set the last run's score to inf
    #     self.last_runs_score = np.inf
    #     # Calculate this run's score based on average/total path length
    #     # and pcb surface area (obviously including the paths)
    #     self.curr_runs_score = self.calculate_score(
    #         paths)

    #     # run the subsequent iterations up until the score is high enough or we've reached the max_iters
    #     self.iteration_num = 1
    #     while np.subtract(self.curr_runs_score, self.last_runs_score) > .3 and self.iteration_num < max_iters:
    #         self.last_runs_score = self.curr_runs_score
    #         self.paths.clear()
    #         self.pin_placement_dict.clear()
    #         self.connections_list.clear()

    #         self.randomize_layout()
    #         self.initialize_pin_placement_dict()
    #         self.initialize_connections_list()
    #         paths = self.run_a_star()

    #         self.curr_runs_score = self.calculate_score(
    #             paths)
    #         self.iteration_num += 1

    #     self.paths = paths

    # def not_allowed_pcb_spots(self):
    #     not_allowed = []

    #     # Append existing components to the not allowed list.
    #     for component in self.components.values():
    #         if component.pcb_position != []:
    #             not_allowed.append(component.pcb_position[0])
    #             not_allowed.append(component.pcb_position[1])

    #     return not_allowed

    # def get_pin1_pos(self):
    #     pin1_pos = [int(np.floor(np.random.rand() * self.n_grid_spaces)),
    #                 int(np.floor(np.random.rand() * self.n_grid_spaces))]
    #     return pin1_pos

    # def get_pin2_pos(self, pin1_pos):
    #     global PCB_ORIENTATIONS
    #     possible_orientations = PCB_ORIENTATIONS.copy()
    #     rn_orient = int(np.floor(np.random.rand() * 4))

    #     # topleft corner
    #     if pin1_pos[0] == 0 and pin1_pos[1] == 0:
    #         rn_orient = int(np.floor(np.random.rand() * 2))
    #         possible_orientations.remove([-1, 0])
    #         possible_orientations.remove([0, -1])
    #     # topright corner
    #     elif pin1_pos[0] == 0 and pin1_pos[1] == self.n_grid_spaces - 1:
    #         rn_orient = int(np.floor(np.random.rand() * 2))
    #         possible_orientations.remove([0, 1])
    #         possible_orientations.remove([-1, 0])
    #     # bottomright corner
    #     elif pin1_pos[0] == self.n_grid_spaces - 1 and pin1_pos[1] == self.n_grid_spaces - 1:
    #         rn_orient = int(np.floor(np.random.rand() * 2))
    #         possible_orientations.remove([1, 0])
    #         possible_orientations.remove([0, 1])
    #     # bottomleft corner
    #     elif pin1_pos[0] == self.n_grid_spaces - 1 and pin1_pos[1] == 0:
    #         rn_orient = int(np.floor(np.random.rand() * 2))
    #         possible_orientations.remove([0, -1])
    #         possible_orientations.remove([1, 0])
    #     # left edge
    #     elif pin1_pos[0] * pin1_pos[1] == 0 and pin1_pos[1] == 0:
    #         rn_orient = int(np.floor(np.random.rand() * 3))
    #         possible_orientations.remove([0, -1])
    #     # top edge
    #     elif pin1_pos[0] * pin1_pos[1] == 0 and pin1_pos[0] == 0:
    #         rn_orient = int(np.floor(np.random.rand() * 3))
    #         possible_orientations.remove([-1, 0])
    #     # right edge
    #     elif pin1_pos[1] == self.n_grid_spaces - 1:
    #         rn_orient = int(np.floor(np.random.rand() * 3))
    #         possible_orientations.remove([0, 1])
    #     # bottom edge
    #     elif pin1_pos[0] == self.n_grid_spaces - 1:
    #         rn_orient = int(np.floor(np.random.rand() * 3))
    #         possible_orientations.remove([1, 0])
    #     pin2_pos = np.add(pin1_pos, possible_orientations[rn_orient]).tolist()

    #     return pin2_pos

    # def get_valid_spot(self, not_allowed_pcb_spots):
    #     rn_pos_1 = self.get_pin1_pos()
    #     rn_pos_2 = self.get_pin2_pos(rn_pos_1)
    #     rn_pos = [rn_pos_1, rn_pos_2]

    #     i = 0
    #     while rn_pos[0] in not_allowed_pcb_spots or rn_pos[1] in not_allowed_pcb_spots:
    #         # print("redoing pin1 and pin2")
    #         rn_pos_1 = self.get_pin1_pos()
    #         rn_pos_2 = self.get_pin2_pos(rn_pos_1)
    #         rn_pos = [rn_pos_1, rn_pos_2]

    #         i += 1
    #     return rn_pos

    # # Will make a layout where no pins overlap
    # # and are adjusted by some padding (-Jason)
    # def randomize_layout(self):
    #     not_allowed_pcb_spots = []
    #     for component in self.components.values():
    #         rn_spot = self.get_valid_spot(not_allowed_pcb_spots)
    #         rn_spot = np.add(
    #             rn_spot, [int(self.grid_padding/2), int(self.grid_padding)]).tolist()
    #         component.pcb_position = rn_spot

    # # This gets a list for the position for every pin
    # def initialize_pin_placement_dict(self):
    #     pin_placement_dict = {}
    #     for component in self.components.values():
    #         pin_ids = list(component.connections.keys())
    #         for pin_id, pos in zip(pin_ids, component.pcb_position):
    #             pin_placement_dict |= {pin_id: pos}
    #     self.pin_placement_dict = pin_placement_dict

    # # This gets the connections into a single list
    # def initialize_connections_list(self):
    #     connections_list = []
    #     for component in self.components.values():
    #         for pin_id, connections in component.connections.items():
    #             for connection in connections:
    #                 if len(connections_list) > 0:
    #                     if not [connection, pin_id] in connections_list:
    #                         connections_list.append([pin_id, connection])
    #                 else:
    #                     connections_list.append([pin_id, connection])

    #     self.connections_list = connections_list

    # def pcb_area(self, paths):
    #     min_x = 0
    #     max_x = self.n_grid_spaces + self.grid_padding
    #     min_y = 0
    #     max_y = self.n_grid_spaces + self.grid_padding

    #     for path in paths:
    #         for grid_node in path:
    #             grid_x = grid_node[0]
    #             grid_y = grid_node[1]

    #             min_x = min(grid_x, min_x)
    #             max_x = max(grid_x, max_x)
    #             min_y = min(grid_y, min_y)
    #             max_y = max(grid_y, max_y)

    #     return (max_x - min_x) * (max_y - min_y)

    # # For calculating how good a set of paths (pcb layout) is.
    # # It is based on total path length and total area (including paths)
    # def calculate_score(self, paths):
    #     total_path_length = 0
    #     for path in paths:
    #         total_path_length += path["length"]

    #     total_area = self.pcb_area(paths)

    #     score_non_normalized = (total_area * self.area_weight) + \
    #         (total_path_length * self.path_length_weight)
    #     score_normalized = score_non_normalized / \
    #         (self.area_weight + self.path_length_weight)

    #     return score_normalized

    # def run_a_star(self):
    #     paths = []
    #     not_allowed = self.not_allowed_pcb_spots()
    #     grid = PcbGrid(self.n_grid_spaces + self.grid_padding, not_allowed)

    #     for start_id, goal_id in self.connections_list:
    #         start_pos = self.pin_placement_dict[start_id]
    #         goal_pos = self.pin_placement_dict[goal_id]

    #         start_node = grid.node_at(start_pos)
    #         goal_node = grid.node_at(goal_pos)

    #         path = grid.a_star(start_node, start_id, goal_node, goal_id)
    #         not_allowed += path["grid_nodes"]
    #         path["path_id"] = f"{start_id}->{goal_id}"
    #         paths.append(path)
    #         grid = PcbGrid(self.n_grid_spaces + self.grid_padding, not_allowed)

    #     return paths
