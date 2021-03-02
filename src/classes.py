import numpy as np
import json
import os.path

class Component:
    def __init__(self, schematic, label="", id=-1, sPos=[0, 0], sOrient=np.identity(2), pPos=[], pOrient=np.identity(2), connections=[[]]):
        self.schematic = schematic
        self.label = label
        self.id = id
        self.sPos = sPos # will be used as a vector to hold the x and y coordinate of the component
        self.sOrient = sOrient
        self.pPos = pPos
        self.pOrient = pOrient
        self.connections = connections # list of a list of strings: the first dim will be the pin, the second is the pinID that the pin the first dim corresponds to connects to

    def getID(self):
        return self.id

    def getConnections(self):
        return self.connections

    def connect(self, thisPinNumber, thatPinId):
        self.connections[thisPinNumber].append(thatPinId)

    def disconnect(self, thisPinNumber, thatPinId):
        self.connections[thisPinNumber].remove(thatPinId)

    def addLabel(self, label):
        # raise NotImplementedError("Abstract method") # I think since every one of the labels will be drawn the same, we should be able to implement this here in the parent class.
        self.label = label

    def draw(self):
        raise NotImplementedError("Abstract method")

    def toDict(self):
        return {"label": self.label, "id": self.id, "sPos": self.sPos, "sOrient": self.sOrient.tolist(), "pPos": self.pPos, "pOrient": self.pOrient.tolist(), "connections": self.connections}

class Resistor(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class Capacitor(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class Inductor(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class NpnTransistor(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class PnpTransistor(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class Switch(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class Diode(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class LED(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class Ground(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass


class VoltageSource(Component):
    # def addLabel(self, label): See comment on this function in the Component class (-Jason)
    #     self.label = label

    def draw(self):
        pass

class Comment:
    def __init__(self, schematic, comment="Type something here", location=[0, 0]):
        self.comment = comment
        self.location = []
        self.schematic = schematic

    def editComment(self, comment):
        self.comment = comment
        self.schematic.draw()

    def setLocation(self, location):
        self.location = location

    def draw(self):
        pass

    def toDict(self):
        return {"comment": self.comment, "location": self.location}

class Schematic:
    COMPONENT_TYPES = {'Resistor': Resistor, 'Capacitor': Capacitor, 'Inductor': Inductor, 'NpnTransistor': NpnTransistor, 'PnpTransistor': PnpTransistor, 'Switch': Switch, 'Diode': Diode, 'LED': LED, 'Ground': Ground, 'VoltageSource': VoltageSource}
    MAX_ITER = 10

    def __init__(self):
        self.components = []
        self.comments = []
        self.paths = [[]]
        self.iterationNum = 0
        self.lastRunScore = 1.0
        self.thisRunScore = 0.0
        self.nGridSpaces = 5
    
    # I'm using this to set a new schematic to a loaded one (-Jason)
    def Schematic(self, schematicDict):
        pass
        # self.components = components
        # self.comments = comments
        # self.paths = paths
        # self.iterationNum = iterationNum
        # self.lastRunScore = lastRunScore
        # self.thisRunScore = thisRunScore
        # self.nGridSpaces = nGridSpaces
    
    def addWire(self, component1, component1PinNumber, component2, component2PinNumber):
        component1PinId = "{0}_{1}".format(component1.id, component1PinNumber)
        component2PinId = "{0}_{1}".format(component2.id, component2PinNumber)

        component1.connect(component1PinNumber, component2PinId)
        component2.connect(component2PinNumber, component1PinId)

    def snipWire(self, component1, component1PinNumber, component2, component2PinNumber):
        component1PinId = "{0}_{1}".format(component1.id, component1PinNumber)
        component2PinId = "{0}_{1}".format(component2.id, component2PinNumber)
        component1.disconnect(component1PinNumber, component2PinId)
        component2.disconnect(component2PinNumber, component1PinId)

    def addComponent(self, schematic, typeOfComponent, id, sPos, sOrient = np.identity(2)):
        kwargs = {'schematic': schematic, 'id': id, 'sPos': sPos, 'sOrient': sOrient}
        component = self.COMPONENT_TYPES[typeOfComponent](**kwargs)
        self.components.append(component)

    def deleteComponent(self, component):
        self.components.remove(component)

    def addLabel(self, component, label):
        index = self.components.index(component)
        self.components[index].addLabel(label)

    def draw(self):
        for component in self.components:
            component.draw()
        for comment in self.comments:
            comment.draw()

    def toDict(self):
        numComponents = len(self.components)
        numComments = len(self.comments)
        components = []
        comments = []
        schematicDict = {}

        for component in self.components:
            components.append(component.toDict())

        for comment in self.comments:
            comments.append(comment.toDict())

        schematic = {
            "components": components,
            "comments": comments,
            "paths": self.paths,
            "iterationNum": self.iterationNum,
            "lastRunScore": self.lastRunScore,
            "thisRunScore": self.thisRunScore,
            "nGridSpaces": self.nGridSpaces
            }

        return schematic

    def save(self, filename): # need to implement some safegard to be sure that the user wants to save over something (in case the file already exists) (-Jason)
        if not os.path.exists(filename):
            schematicDict = self.toDict()
            with open(filename, 'x') as f:
                json.dump(schematicDict, f)
        else: # notify user that file exists and ask if they want to overwrite it/choose a different name
             pass

    def load(self, filename):  # need to implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic) (-Jason)
        f = open(filename, "r")
        schematicDict = json.load(f)
        Schematic(schematicDict)

    # Metropolis' Monte Carlo method. (-Jason)
    def monteCarloMaster(self, filename):
        connections = self.initializeMonteArray()

        i = 0
        while i < self.MAX_ITER:
            i += 1
            pass
    
    def initializeMonteArray(self):
        allPinIds = []
        return {}

    def monteCarlo(self): # the helper function for Monte Carlo (-Jason)
        rn = np.ceil(np.random.rand() * self.nGridSpaces)

    # A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm (-Jason)
    def aStar(self):
        print("What's up?")