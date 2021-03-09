import numpy as np
import json
import os.path


class Component:
    # The component type field is what determines which sprite will be used
    # and what component fields to pull from the .json database. As long as the
    # database has the dimensions corresponding to type: component type,
    # and the spritesheet has a picture for it, the component can be used.
    # This is very important for any amount of scalability (we don't have to
    # make a load of classes for each specific type)
    def __init__(self, label, schem_position, schem_orientation, pcb_position, pcb_orientation):
        if self.valid_input({"schem_position": schem_position, "schem_orientation": schem_orientation, "pcb_position": pcb_position, "pcb_orientation": pcb_orientation}):
            self.label = label
            # will be used as a vector to hold the x and y coordinate of the component's sprite (-Jason)
            self.schem_position = schem_position
            # rotated clockwise, counterclockwise, etc. (-Jason)
            self.schem_orientation = schem_orientation
            # for gridspace in pcb layout generation (-Jason)
            self.pcb_position = pcb_position
            # rotate clockwise or counterclockwise using [[0, 1], [1, 0]] and [[0, -1], [1, 0]] respectively (you multiply the pcb_position vector with this to rotate it) (-Jason)
            self.pcb_orientation = pcb_orientation
            self.physical_dimensions = {"central_position_sprite": [], "pin_positions_sprite": [], "sprite_index": -1, "solder_pad_positions": [
            ], "solder_pad_dim": 1}  # pulled from the .json database (pin/solder pad postions are relative to a central position) (-Jason)
            # self.sprite # eventually a png once I figure it out (-Jason)

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
                if input_kwargs[key] == "":
                    raise ValueError("Invalid label text")
            elif key == "schem_position":
                if type(input_kwargs[key]) != list:
                    raise TypeError("Invalid position type")
                if np.shape(input_kwargs[key]) != (2,):
                    raise ValueError(
                        "Invalid shape for schematic position vector")
            elif key == "schem_orientation":
                if type(input_kwargs[key]) != np.ndarray:
                    raise TypeError("Invalid orientation type")
                if np.shape(input_kwargs[key]) != (2, 2):
                    raise ValueError(
                        f"Invalid shape for schematic orientation matrix: {np.shape(input_kwargs[key])}")
            elif key == "pcb_position":
                if type(input_kwargs[key]) != np.ndarray:
                    raise TypeError("Invalid position type")
                if np.shape(input_kwargs[key]) != (2,):
                    raise ValueError("Invalid shape for pcb position vector")
            elif key == "pcb_orientation":
                if type(input_kwargs[key]) != np.ndarray:
                    raise TypeError("Invalid orientation type")
                if np.shape(input_kwargs[key]) != (2, 2):
                    raise ValueError(
                        "Invalid shape for pcb orientation matrix")
        return True

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

    def to_dict(self):
        if type(self.schem_orientation) == np.ndarray:
            schem_orientation = self.schem_orientation.tolist()
        else:
            schem_orientation = self.schem_orientation

        if type(self.pcb_position) == np.ndarray:
            pcb_position = self.pcb_position.tolist()
        else:
            pcb_position = self.pcb_position

        if type(self.pcb_orientation) == np.ndarray:
            pcb_orientation = self.pcb_orientation.tolist()
        else:
            pcb_orientation = self.pcb_orientation

        component_dict = {
            "id": self.id,
            "component_type": self.__class__.__name__,
            "label": self.label,
            "schem_position": self.schem_position,
            "schem_orientation": schem_orientation,
            "pcb_position": pcb_position,
            "pcb_orientation": pcb_orientation,
            "connections": self.connections
        }
        return component_dict


class Resistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Capacitor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Inductor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class NpnTransistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 3
            self.connections = {f"{self.id}_0": [],
                                f"{self.id}_1": [], f"{self.id}_2": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [],
                                f"{self.id}_1": [], f"{self.id}_2": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class PnpTransistor(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 3
            self.connections = {f"{self.id}_0": [],
                                f"{self.id}_1": [], f"{self.id}_2": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [],
                                f"{self.id}_1": [], f"{self.id}_2": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Diode(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Led(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Switch(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class VoltageSource(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 2
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": [], f"{self.id}_1": []}
        else:
            self.connections = connections

    def draw(self):
        pass


class Ground(Component):
    def __init__(self, id=-1, label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2)):
        if self.valid_input({"id": id}):
            super().__init__(label, schem_position,
                             schem_orientation, pcb_position, pcb_orientation)
            self.id = id
            self.num_pins = 1
            self.connections = {f"{self.id}_0": []}

    def set_connections(self, connections={}):
        if len(connections) == 0:
            self.connections = {f"{self.id}_0": []}
        else:
            self.connections = connections

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
    MAX_ITER = 10
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
        self.paths = []
        self.iteration_num = 0
        self.h = []
        self.g = []
        self.f = []
        self.last_run_score = 1.0
        self.this_run_score = 0.0
        self.n_grid_spaces = 5

    # Checks an id versus the list of component ids that exist and tells whether its unique
    def unique_component_id(self, id):
        if len(self.components) < 1:
            return True
        else:
            return not (id in [component_id for component_id in self.components])

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
        self.h = schematic_dict["h"]
        self.g = schematic_dict["g"]
        self.f = schematic_dict["f"]
        self.last_run_score = schematic_dict["last_run_score"]
        self.this_run_score = schematic_dict["this_run_score"]
        self.n_grid_spaces = schematic_dict["n_grid_spaces"]

    def add_component(self, component_dict):
        if self.unique_component_id(component_dict["id"]):
            if "connections" in component_dict:
                connections = component_dict.pop("connections")
            else:
                connections = {}

            if "schem_orientation" in component_dict and type(component_dict["schem_position"]) == list:
                component_dict["schem_orientation"] = np.array(
                    component_dict["schem_orientation"])

            if "pcb_position" in component_dict and type(component_dict["pcb_position"]) == list:
                component_dict["pcb_position"] = np.array(
                    component_dict["pcb_position"])

            if "pcb_orientation" in component_dict and type(component_dict["pcb_orientation"]) == list:
                component_dict["pcb_orientation"] = np.array(
                    component_dict["pcb_orientation"])

            component_type = component_dict["component_type"]
            component_dict.pop("component_type")
            component = self.COMPONENT_CLASSES[component_type](
                **component_dict)
            component.set_connections(connections)
            self.components[f"component_{component.id}"] = (component)
        else:
            raise ValueError("Component id not unique")

    def delete_component(self, id):
        self.components.pop(f"component_{id}")

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

    def change_label(self, component_id, text):
        self.components[f"component_{component_id}"].change_label(text)

    def add_comment(self, comment_dict):
        if self.unique_comment_id(comment_dict["id"]):
            comment = Comment(**comment_dict)
            self.comments[f"comment_{comment.id}"] = comment
        else:
            raise ValueError("Comment id not unique")

    def remove_comment(self, id):
        self.comments.pop(f"comment_{id}")

    def draw(self):
        for component in self.components:
            component.draw()
        for comment in self.comments:
            comment.draw()

    def to_dict(self):
        components = {}
        comments = {}
        schematic_dict = {}

        for component_id in self.components:
            components[component_id] = self.components[component_id].to_dict(
            )

        for comment_id in self.comments:
            comments[comment_id] = self.comments[comment_id].to_dict(
            )

        schematic_dict = {
            "components": components,
            "comments": comments,
            "paths": self.paths,
            "iteration_num": self.iteration_num,
            "h": self.h,
            "g": self.g,
            "f": self.f,
            "last_run_score": self.last_run_score,
            "this_run_score": self.this_run_score,
            "n_grid_spaces": self.n_grid_spaces
        }

        return schematic_dict

    def save(self, file_name):  # need to implement some safegard to be sure that the user wants to save over something (in case the file already exists) (-Jason)
        if not os.path.exists(file_name):
            schematic_dict = self.to_dict()
            with open(file_name, 'x') as f:
                json.dump(schematic_dict, f)
        else:  # notify user that file exists and ask if they want to overwrite it/choose a different name
            raise FileExistsError(f"\"{file_name}\" already exists")

    def load(self, file_name):  # need to implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic) (-Jason)
        if os.path.exists(file_name):
            f = open(file_name, "r")
            schematic_dict = json.load(f)
            self.Schematic(schematic_dict)
        else:  # notify user that file does not exist and ask if they want to reenter a filename
            raise FileNotFoundError(f"No file \"{file_name}\"")

    # # Metropolis' Monte Carlo method. (-Jason)
    # def monte_carlo(self):
    #     connections = self.initialize_connections_array()

    #     i = 0
    #     while i < self.MAX_ITER:
    #         rn = np.ceil(np.random.rand() * self.n_grid_spaces)
    #         i += 1

    # def initialize_connections_array(self):
    #     conns = []
    #     for component in self.components:
    #         # conns.append(component.)
    #         pass

    #     return {}

    # def calculate_score(self):
    #     pass

    # # A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm (-Jason)
    # def a_star(self):
    #     h = [[],[]]
    #     g = [[],[]]
    #     f = [[],[]]
