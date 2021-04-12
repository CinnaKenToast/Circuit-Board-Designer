import numpy as np
import json
import os.path

# set the transform.rotate(...) to one of these --- flip does not mirror, it just rotates by 180 degrees. (-Jason)
SCHEM_ORIENTATIONS = {'upright': 0, 'CW1': 90, 'CCW1': -90, 'flip': 180}
# add the one that sets the second pin whichever direction you want the component to go. (-Jason)
PCB_ORIENTATIONS = [[1, 0], [0, 1], [-1, 0], [0, -1]]


class Component:
    global SCHEM_ORIENTATIONS
    # The component type field is what determines which sprite will be used
    # and what component fields to pull from the .json database. As long as the
    # database has the dimensions corresponding to type: component type,
    # and the spritesheet has a picture for it, the component can be used. (-Jason)

    def __init__(self, id, label, num_pins, schem_position, schem_orientation, pcb_position, connections):
        if self.valid_input({"id": id, "label": label, "schem_position": schem_position, "schem_orientation": schem_orientation}):
            self.id = id
            self.label = label
            self.num_pins = num_pins
            self.schem_position = schem_position
            self.schem_orientation = schem_orientation
            self.pcb_position = pcb_position
            self.connections = self.set_connections(connections)

            # self.pin_positions_svg = [] # the position data of the circles in the svg
            # self.solder_pad_dim = 1 # Our solder pads are squares, so only one dim is needed (-Jason)
            # self.svg_image_name # eventually an svg once I finish them (-Jason)
            # self.xml_svg # for manipulating the svg

    def valid_input(self, input_kwargs):
        global SCHEM_ORIENTATIONS

        for key in input_kwargs:
            if key == "id":
                if type(input_kwargs[key]) != int:
                    raise TypeError("Invalid id type")
                if input_kwargs[key] < 0:
                    raise ValueError("Invalid id value")
            elif key == "label":
                if type(input_kwargs[key]) != str:
                    raise TypeError("Invalid label type")
                if input_kwargs[key] == "":
                    raise ValueError("Invalid label text")
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
            self.connections = connections

    def connect(self, this_pin_id, that_pin_id):
        if this_pin_id in self.connections:
            self.connections[this_pin_id].append(that_pin_id)
        else:
            raise ValueError("Invalid pin id")

    def disconnect(self, this_pin_id, that_pin_id):
        self.connections[this_pin_id].remove(that_pin_id)

    def change_label(self, text=""):
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
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Capacitor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Inductor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class NpnTransistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 3, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class PnpTransistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 3, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Diode(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Led(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Switch(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class VoltageSource(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

    def draw(self):
        pass


class Ground(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=SCHEM_ORIENTATIONS['upright'], pcb_position=[], connections={}):
        super().__init__(id, label, 2, schem_position,
                         schem_orientation, pcb_position, connections)

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


class Schematic:
    COMPONENT_CLASSES = {
        "Resistor": Resistor,
        "Capacitor": Capacitor,
        "Inductor": Inductor,
        "NpnTransistor": NpnTransistor,
        "PnpTransistor": PnpTransistor,
        "Diode": Diode,
        "Led": Led,
        "Switch": Switch,
        "VoltageSource": VoltageSource,
        "Ground": Ground
    }

    def __init__(self):
        self.components = {}
        self.comments = {}
        self.paths = {}
        self.iteration_num = -1
        self.connection_num = -1
        self.H = []
        self.G = []
        self.F = []
        self.last_runs_score = 1.0
        self.curr_runs_score = 0.0
        self.n_grid_spaces = 5
        self.max_iters = 10

    # Allows for setting the monte carlo params so it can continue (-Jason)
    def set_monte_carlo_parameters(self, n_grid_spaces=5, max_iters=10):
        self.n_grid_spaces = n_grid_spaces
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
        self.iteration_num = schematic_dict["iteration_num"]
        self.connection_num = schematic_dict["connection_num"]
        self.H = schematic_dict["H"]
        self.G = schematic_dict["G"]
        self.F = schematic_dict["F"]
        self.last_run_score = schematic_dict["last_runs_score"]
        self.curr_run_score = schematic_dict["curr_runs_score"]
        self.set_monte_carlo_parameters(
            schematic_dict["n_grid_spaces"], schematic_dict["max_iters"])

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

    def edit_label(self, component_id, new_text):
        self.components[f"component_{component_id}"].change_label(new_text)

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
            "iteration_num": self.iteration_num,
            "connection_num": self.connection_num,
            "H": self.H,
            "G": self.G,
            "F": self.F,
            "last_runs_score": self.last_runs_score,
            "curr_runs_score": self.curr_runs_score,
            "n_grid_spaces": self.n_grid_spaces,
            "max_iters": self.max_iters
        }

        return schematic_dict

    def save(self, file_name):  # need to implement some safegard to be sure that the user wants to save over something (in case the file already exists) (-Jason)
        if not os.path.exists(file_name):
            schematic_dict = self.to_dict()
            with open(file_name, 'x') as f:
                json.dump(schematic_dict, f)
        # notify user that file exists and ask if they want to overwrite it/choose a different name (-Jason)
        else:
            raise FileExistsError(f"\"{file_name}\" already exists")

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

    def monte_carlo(self):
        for self.iteration_num in range(0, self.max_iters):
            not_allowed_pcb_spots = self.not_allowed_pcb_spots()
            self.randomize_layout(not_allowed_pcb_spots)
            adj = self.initialize_adjacency_array()
            self.run_a_star()

    # Having issues with iterating over dict values... (-Jason)
    def not_allowed_pcb_spots(self):
        not_allowed = []
        for component in self.components.values():
            if component.pcb_position != []:
                not_allowed.append(component.pcb_position[0])
                not_allowed.append(component.pcb_position[1])
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

    # will make a layout where no pins overlap (-Jason)
    def randomize_layout(self, not_allowed_pcb_spots):
        for component in self.components.values():
            rn_spot = self.get_valid_spot(not_allowed_pcb_spots)
            component.pcb_position = rn_spot
            not_allowed_pcb_spots.append(rn_spot[0])
            not_allowed_pcb_spots.append(rn_spot[1])

    def initialize_adjacency_array(self):
        for component in self.components.values():
            for pin, connection in component.connections:
                pass

    def initialize_paths(self):
        pass

    def calculate_score(self):
        pass

    def run_a_star(self):
        for self.connection_num in range(0, len(self.components)):
            self.a_star(self.H(self.connection_num), self.G(
                self.connection_num), self.F(self.connection_num))

    # A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm (-Jason)
    def a_star(self, h, g, f):
        pass
