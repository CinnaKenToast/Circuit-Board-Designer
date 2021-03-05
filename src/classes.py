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
    def __init__(self, id=-1, component_type="", label="", schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2), connections={}):
        self.id = id # >= 0 and unique
        self.component_type = component_type
        self.label = label
        self.schem_position = schem_position # will be used as a vector to hold the x and y coordinate of the component's sprite (-Jason)
        self.schem_orientation = schem_orientation # rotated clockwise, counterclockwise, etc.
        self.pcb_position = pcb_position # for gridspace in pcb layout generation
        self.pcb_orientation = pcb_orientation # rotate clockwise or counterclockwise using [[0, 1], [1, 0]] and [[0, -1], [1, 0]] respectively (you multiply the pcb_position vector with this to rotate it)
        self.connections = connections # dictionary whose keys are the pin ids for each pin and whose values are a list of pin_ids that they're connected to. (-Jason)
        self.physical_dimenstions = {"central_position_sprite": [], "pin_positions_sprite": [], "sprite_index": -1, "solder_pad_positions": [], "solder_pad_dim": 1} # pulled from the .json database (pin/solder pad postions are relative to a central position)
        # self.sprite # eventually a png once I figure it out

    def connect(self, this_pin_id, that_pin_id):
        if this_pin_id in self.connections:
            self.connections[this_pin_id].append(that_pin_id)
        else:
            self.connections[this_pin_id] = [that_pin_id]
    
    def disconnect(self, this_pin_id, that_pin_id):
        self.connections[this_pin_id].remove(that_pin_id)

    def change_label(self, text=""):
        self.label = text

    def draw(self):
        pass

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
            "component_type": self.component_type,
            "label": self.label,
            "schem_position": self.schem_position,
            "schem_orientation": schem_orientation,
            "pcb_position": pcb_position,
            "pcb_orientation": pcb_orientation,
            "connections": self.connections
            }
        return component_dict

class Comment:
    def __init__(self, id, text="Type something here", position=[0, 0]):
        self.id = id
        self.text = text
        self.position = position

    def edit_text(self, text):
        self.text = text

    def set_position(self, position):
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
    
    # I'm using this to set a new schematic to a loaded one (-Jason)
    def Schematic(self, schematic_dict):
        components_dict = schematic_dict["components"]
        for component in components_dict:
            self.add_component(**component)

        comments_dict = schematic_dict["comments"]
        for comment in comments_dict:
            self.add_comment(**comment)

        self.paths = schematic_dict["paths"]
        self.iteration_num = schematic_dict["iteration_num"]
        self.h = schematic_dict["h"]
        self.g = schematic_dict["g"]
        self.f = schematic_dict["f"]
        self.last_run_score = schematic_dict["last_run_score"]
        self.this_run_score = schematic_dict["this_run_score"]
        self.n_grid_spaces = schematic_dict["n_grid_spaces"]
    
    def add_component(self, component_type="", label="", id=-1, schem_position=[0, 0], schem_orientation=np.identity(2), pcb_position=np.array([1, 0]), pcb_orientation=np.identity(2), connections={}):
        kwargs = {
            'id': id,
            'component_type': component_type,
            'label': label,
            'schem_position': schem_position,
            'schem_orientation': schem_orientation,
            'pcb_position': pcb_position,
            'pcb_orientation': pcb_orientation,
            'connections': connections
            }
        component = Component(**kwargs)
        self.components[component.id] = (component)

    def delete_component(self, id):
        self.components.pop(id)

    def add_connection(self, component_1_pin_id, component_2_pin_id):
        component_1_id = int(component_1_pin_id.split("_")[0])
        component_2_id = int(component_2_pin_id.split("_")[0])
        self.components[component_1_id].connect(component_1_pin_id, component_2_pin_id)
        self.components[component_2_id].connect(component_2_pin_id, component_1_pin_id)
        
    def remove_connection(self, component_1_pin_id, component_2_pin_id):
        component_1_id = int(component_1_pin_id.split("_")[0])
        component_2_id = int(component_2_pin_id.split("_")[0])
        self.components[component_1_id].disconnect(component_1_pin_id, component_2_pin_id)
        self.components[component_2_id].disconnect(component_2_pin_id, component_1_pin_id)

    def change_label(self, component_id, text):
        self.components[component_id].change_label(text)

    def add_comment(self, id, text, position=[0, 0]):
        kwargs = {
            "id": id,
            "text": text,
            "position": position
            }
        self.comments[id](Comment(**kwargs))

    def remove_comment(self, id):
        self.comments.pop(id)

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
            components[component_id] = self.components[component_id].to_dict()

        for comment_id in self.comments:
            comments[comment_id] = self.comments[comment_id].to_dict()

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