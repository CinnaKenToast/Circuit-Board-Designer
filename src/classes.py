import numpy as np
import json

class Component:
    def __init__(self, schematic, id, sPos, sOrient=np.identity(2)):
        self.label = ""
        self.id = id
        self.sPos = sPos # will be used as a vector to hold the x and y coordinate of the component
        self.sOrient = sOrient
        self.pPos = []
        self.pOrient = np.identity(2)
        self.connections = [[]] # list of a list of strings: the first dim will be the pin, the second is the pinID that the pin the first dim corresponds to connects to
        self.schematic = schematic

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
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class Capacitor(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class Inductor(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class NpnTransistor(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class PnpTransistor(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class Switch(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class Diode(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class LED(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class Ground(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass


class VoltageSource(Component):
    # def addLabel(self, label):
    #     self.label = label

    def draw(self):
        pass

class Comment:
    def __init__(self, comment, schematic):
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
    COMPONENT_TYPES = {'Resistor': Resistor, 'Capacitor': Capacitor, 'Inductor': Inductor,
                       'NpnTransistor': NpnTransistor, 'PnpTransistor': PnpTransistor, 'Switch': Switch, 'Diode': Diode, 'LED': LED, 'Ground': Ground, 'VoltageSource': VoltageSource}

    def __init__(self):
        self.components = []
        self.comments = []
    
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
        component = self.COMPONENT_TYPES[typeOfComponent](schematic, id, sPos, sOrient)
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

        return {"Components": { k:v.toDict() for (k,v) in zip(["Component{}".format(key) for key in range(numComponents)], self.components)}, "Comments": { k:v.toDict() for (k,v) in zip(["Comment{}".format(key) for key in range(numComments)], self.comments)}}
    
    def save(self, filename):
        schematic = self.toDict()
        json_object = json.dumps(schematic, indent=4)

        f = open(filename, "x")
        f.write(json_object)
        f.close()

    # def load(self, filename):  # implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic)
        # f = open(filename, "r")
        # json_object = json.load(filename)

# This class will hold the Monte Carlo, A*, and toImage methods
class PCB(Schematic):
    MAX_ITER = 10

    def __init__(self):
        self.connections = []
        self.paths = [[int]]
        self.lastRun = np.inf
        self.thisRun = float

    # Metropolis' Monte Carlo method.
    def monteCarloMaster(self, filename):

        # Example of how to get a random number:
        # ran.seed(dt.now())
        # rn = ran.random() # rn is now a random number between 0 and 1

        connectionList = self.connections
        self.initializeConnectionsArray(connectionList)

        i = 0
        while i < self.MAX_ITER:
            i += 1
            pass

    def initializeConnectionsArray(self, connectionList): # for A*
        print("Hi!")
    
    def monteCarlo(self): # the actual algorithm
        print("Hello, friend!")

    # A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm
    def aStar(self):
        print("What's up?")
