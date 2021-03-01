import numpy as np
import json


class Component:
    def __init__(self):
        self.label = str()
        self.id = int
        # will be used as a vector to hold the x and y coordinate of the component
        self.sPos = [int]
        self.sOrient = np.ndarray
        # will be used as a vector to hold the x and y coordinate of the component
        self.pPos = [int]
        self.pOrient = np.ndarray
        # list of a list of strings: the first dim will be the pin, the second is the pinID that the pin the first dim corresponds to connects to
        self.connections = [[str]]
        self.schematic = Schematic
        self.path = [int][int][int]

    def Component(self, schematic, id, sPos, sOrient=np.identity(2)):
        self.label = str()
        self.id = id
        self.sPos = sPos
        self.sOrient = sOrient
        self.pPos = [int]
        # list of a list of strings: the first dim will be the pin, the second is the pinID that the pin the first dim corresponds to connects to
        self.connections = [[str]]
        self.schematic = schematic
        self.path = [int][int][int]

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
    def __init__(self):
        self.comment = str()
        self.location = [int]
        self.schematic = Schematic

    def Comment(self, comment, schematic):
        self.comment = comment
        self.location = [int]
        self.schematic = schematic

    def editComment(self, comment):
        self.comment = comment
        self.schematic.draw()

    def setLocation(self, location):
        self.location = location

    def draw(self):
        pass

class Schematic:
    COMPONENT_TYPES = {'Resistor': Resistor, 'Capacitor': Capacitor, 'Inductor': Inductor,
                       'NpnTransistor': NpnTransistor, 'PnpTransistor': PnpTransistor, 'Switch': Switch, 'Diode': Diode, 'LED': LED, 'Ground': Ground, 'VoltageSource': VoltageSource}

    def __init__(self):
        self.components = [Component()]
        self.comments = [Comment()]
        self.importedComponentsForMonteCarlo = False

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

    def addComponent(self, typeOfComponent, id, sPos, sOrient):
        self.components.append(self.COMPONENT_TYPES[typeOfComponent](id, sPos, sOrient))

    def deleteComponent(self, component):
        self.components.remove(component)

    def addLabel(self, component, label):
        index = self.components.index(component)
        self.components[index].addLabel(label)

    def save(self, filename):
        schematic = vars(self)
        json_object = json.dumps(schematic, indent=4)
        with open(filename) as saveFile:
            saveFile.write(json_object)

    def load(self, filename):  # implement some safegard to be sure that the user wants to load in something (in case they had not saved the current schematic)
        with open(filename) as loadFile:
            json_object = json.load(filename)

    def draw(self):
        for component in self.components:
            component.draw()
        for comment in self.comments:
            comment.draw()

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
