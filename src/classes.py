class Component:
    def __init__(self):
        self.label = str()
        self.id = int
        self.sPos = (int,int)
        self.sOrient = [int][int]
        self.pPos = (int, int)
        self.pOrient = [int][int]
        self.connections: {int:int}
        self.path = [int][int][int]
        self.schematic = Schematic
       
    def Component(self, id, sPos, sOreint, schematic):
        self.label = str()
        self.id = id
        self.sPos = sPos
        self.sOrient = sOrient
        self.pPos = (int, int)
        self.pOrient = [int][int]
        self.connections: {int:int}
        self.path = [int][int][int]
        self.schematic = Schematic

    def addLabel(self, label):
        raise NotImplementedError("Abstract method")

    def draw(self):
        raise NotImplementedError("Abstract method")

class Comment:
    def __init__(self):
        self.comment = str()
        self.location = (int,int)
        self.schematic = Schematic

    def Comment(self, comment, schematic):
        self.comment = comment
        self.location = (int, int)
        self.schematic = schematic
        self.schematic.draw()

    def editComment(self, comment):
        self.comment = comment
        self.schematic.draw()

class Schematic:
    def __init__(self):
        self.components = [Component()]
        self.comments = [Comment()]
        self.importedComponentsForMonteCarlo = False
    
    from ._monty import monteCarlo, checkGood, aStar

    def addWire(self, component1, component2):
        index1 = self.components.index(component1)
        index2 = self.components.index(component2)
        # UNSURE HOW TO IMPLEMENT CONNECTIONS


    def snipWire(self, component1, component2):
        pass

    def addComponent(self, id, sPos, sOrient):
        self.components.append(Component(id, sPos, sOrient))            

    def deleteComponent(self, component):
        self.components.remove(component)

    def addLabel(self, component, label):
        index = self.components.index(component)
        self.components[index].addLabel(label)

    def save(self, filename):
        schematic = vars(self)
        json_object = json.dumps(schematic, indent = 4)
        with open(filename) as saveFile:
            saveFile.write(json_object)

    def load(self, filename):
        with open(filename) as loadFile:
            json_object = json.load(filename)

    def draw(self):
        for component in self.components:
            component.draw()
        for comment in self.comments:
            comment.draw()

class Resistor(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class Capacitor(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class Inductor(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class NpnTransistor(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class PnpTransistor(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class Switch(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class Diode(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class LED(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class Ground(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass

class VoltageSource(Component):
    def addLabel(self, label):
        self.label = label

    def draw(self):
        pass