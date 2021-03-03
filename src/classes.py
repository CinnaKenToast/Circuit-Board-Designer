import numpy as np
import json
import os.path

class Component:
    def __init__(self, schematic, label="", id=-1, schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=[], pcb_orientation=np.identity(2), connections=[[]]):
        self.schematic = schematic # Why does a component need a schematic? Doesn't this copy the entire schematic object? (-Jason)
        self.label = label
        self.id = id # >= 0 and unique
        self.schem_position = schem_position # will be used as a vector to hold the x and y coordinate of the component (-Jason)
        self.schem_orientation = schem_orientation
        self.pcb_position = pcb_position
        self.pcb_orientation = pcb_orientation
        self.connections = connections # list of a list of strings: the first dim will be the pin, the second is the pinID that the pin the first dim corresponds to connects to (-Jason)

    def connect(self, this_pin_number, that_pin_id):
        if len(self.connections)-1 >= this_pin_number:
            self.connections[this_pin_number].append(that_pin_id)
        else:
            self.connections.append([that_pin_id])

    def disconnect(self, this_pin_number, that_pin_id):
        self.connections[this_pin_number].remove(that_pin_id)

    def change_label(self, text=""):
        # raise NotImplementedError("Abstract method") # I think since every one of the labels will be drawn the same, we should be able to implement this here in the parent class. (-Jason)
        self.label = text

    def draw(self):
        raise NotImplementedError("Abstract method")

    def to_dict(self):
        component_dict = {
            "type": self.__class__.__name__,
            "label": self.label,
            "id": self.id,
            "schem_position": self.schem_position,
            "schem_orientation": self.schem_orientation.tolist(),
            "pcb_position": self.pcb_position,
            "pcb_orientation": self.pcb_orientation.tolist(),
            "connections": self.connections
            }
        return component_dict
    
class Resistor(Component):
    def draw(self):
        pass

class Capacitor(Component):
    def draw(self):
        pass

class Inductor(Component):
    def draw(self):
        pass

class NpnTransistor(Component):
    def draw(self):
        pass

class PnpTransistor(Component):
    def draw(self):
        pass

class Switch(Component):
    def draw(self):
        pass

class Diode(Component):
    def draw(self):
        pass

class LED(Component):
    def draw(self):
        pass

class Ground(Component):
    def draw(self):
        pass

class VoltageSource(Component):
    def draw(self):
        pass

class Comment:
    def __init__(self, schematic, id, text="Type something here", position=[0, 0]):
        self.schematic = schematic # Why does a comment need a copy of the schematic? (-Jason)
        self.id = id
        self.text = text
        self.position = position

    def edit_text(self, text):
        self.text = text
        self.schematic.draw()

    def set_position(self, position):
        self.location = position
        self.schematic.draw()

    def draw(self):
        pass

    def to_dict(self):
        comment_dict = {"text": self.text, "position": self.position}
        return comment_dict

class Schematic:
    COMPONENT_TYPES = {'Resistor': Resistor, 'Capacitor': Capacitor, 'Inductor': Inductor, 'NpnTransistor': NpnTransistor, 'PnpTransistor': PnpTransistor, 'Switch': Switch, 'Diode': Diode, 'LED': LED, 'Ground': Ground, 'VoltageSource': VoltageSource}
    MAX_ITER = 10

    def __init__(self):
        self.components = []
        self.comments = []
        self.paths = [[]]
        self.iteration_num = 0
        self.last_run_score = 1.0
        self.this_run_score = 0.0
        self.n_grid_spaces = 5
    
    # I'm using this to set a new schematic to a loaded one (-Jason)
    def Schematic(self, schematic_dict):
        components_dict = schematic_dict["components"]
        comments_dict = schematic_dict["comments"]

        for component in components_dict:
            kwargs = {"schematic": self} | component
            self.add_component(**kwargs)

        for comment in comments_dict:
            kwargs = {"schematic": self} | comment
            self.add_comment(**kwargs)

        self.paths = schematic_dict["paths"]
        self.iteration_num = schematic_dict["iteration_num"]
        self.last_run_score = schematic_dict["last_run_score"]
        self.this_run_score = schematic_dict["this_run_score"]
        self.n_grid_spaces = schematic_dict["n_grid_spaces"]
    
    def find_component(self, id):
        for component in self.components:
            if component.id == id:
                return component
        else:
            raise RuntimeError("Component not found") # if the components were not found

    def add_component(self, schematic, component_type, label="", id=-1, schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=[], pcb_orientation=np.identity(2), connections=[[]]):
        kwargs = {'schematic': schematic, 'label': label, 'id': id, 'schem_position': schem_position, 'schem_orientation': schem_orientation, 'pcb_position': pcb_position, 'pcb_orientation': pcb_orientation, 'connections': connections}
        component = self.COMPONENT_TYPES[component_type](**kwargs)
        self.components.append(component)

    def delete_component(self, id):
        component_to_remove = self.find_component(id)
        self.components.remove(component_to_remove)

    def add_connection(self, component_1_id, component_1_pin_number, component_2_id, component_2_pin_number): # should only need the pin_id since it holds the component id in it. (-Jason)
        component_1 = self.find_component(component_1_id)
        component_2 = self.find_component(component_2_id)
        component_1_pin_id = "{0}_{1}".format(component_1_id, component_1_pin_number)
        component_2_pin_id = "{0}_{1}".format(component_2_id, component_2_pin_number)
        component_1_index = self.components.index(component_1)
        component_2_index = self.components.index(component_2)
        self.components[component_1_index].connect(component_1_pin_number, component_2_pin_id)
        self.components[component_2_index].connect(component_2_pin_number, component_1_pin_id)

    def remove_connection(self, component_1_id, component_1_pin_number, component_2_id, component_2_pin_number):
        component_1 = self.find_component(component_1_id)
        component_2 = self.find_component(component_2_id)
        component_1_pin_id = "{0}_{1}".format(component_1_id, component_1_pin_number)
        component_2_pin_id = "{0}_{1}".format(component_2_id, component_2_pin_number)
        component_1_index = self.components.index(component_1)
        component_2_index = self.components.index(component_2)
        self.components[component_1_index].disconnect(component_1_pin_number, component_2_pin_id)
        self.components[component_2_index].disconnect(component_2_pin_number, component_1_pin_id)

    def change_label(self, component_id, text):
        component = self.find_component(component_id)
        component_index = self.components.index(component)
        self.components[component_index].change_label(text)

    def find_comment(self, id):
        for comment in self.comments:
            if comment.id == id:
                return comment
        else:
            raise RuntimeError("Comment not found") # if the comment was not found

    def add_comment(self, schematic, id, text, position=[0, 0]):
        kwargs = {"schematic": self, "id": id, "text": text, "position": position}
        self.comments.append(Comment(**kwargs))

    def remove_comment(self, id):
        comment_to_remove = self.find_comment(id)
        self.comments.remove(comment_to_remove)

    def draw(self):
        for component in self.components:
            component.draw()
        for comment in self.comments:
            comment.draw()

    def to_dict(self):
        components = []
        comments = []
        schematic_dict = {}

        for component in self.components:
            components.append(component.to_dict())

        for comment in self.comments:
            comments.append(comment.to_dict())

        schematic_dict = {
            "components": components,
            "comments": comments,
            "paths": self.paths,
            "iteration_num": self.iteration_num,
            "last_run_score": self.last_run_score,
            "this_run_score": self.this_run_score,
            "n_grid_spaces": self.n_grid_spaces
            }

        return schematic_dict

    def save(self, file_name): # need to implement some safegard to be sure that the user wants to save over something (in case the file already exists) (-Jason)
        if not os.path.exists(file_name):
            schematic_dict = self.to_dict()
            with open(file_name, 'x') as f:
                json.dump(schematic_dict, f)
        else: # notify user that file exists and ask if they want to overwrite it/choose a different name
             pass
    
    def load(self, file_name):  # need to implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic) (-Jason)
        if os.path.exists(file_name):
            f = open(file_name, "r")
            schematic_dict = json.load(f)
            self.Schematic(schematic_dict)
        else: # notify user that file does not exist and ask if they want to reenter a filename
            pass

    # Metropolis' Monte Carlo method. (-Jason)
    def monte_carlo(self):
        connections = self.initialize_connections_array()

        i = 0
        while i < self.MAX_ITER:
            rn = np.ceil(np.random.rand() * self.n_grid_spaces)
            i += 1
    
    def initialize_connections_array(self):
        conns = []
        for component in self.components:
            # conns.append(component.)
            pass
        
        return {}        

    def calculate_score(self):
        pass

    # A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm (-Jason)
    def a_star(self):
        h = [[],[]]
        g = [[],[]]
        f = [[],[]]