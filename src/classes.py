class Component:
    def __init__(self):
        self.label = str()
        self.id = int
        self.s_pos = (int,int)
        self.s_orient = [int][int]
        self.p_pos = (int, int)
        self.p_orirent = [int][int]
        self.connections: {int:int}
        self.path = [int][int][int]
        self.schematic = Schematic
    
       
    def Component(self, id, s_pos, s_oreint, schematic):
        self.label = str()
        self.id = id
        self.s_pos = s_pos
        self.s_orient = s_orient
        self.p_pos = (int, int)
        self.p_orirent = [int][int]
        self.connections: {int:int}
        self.path = [int][int][int]
        self.schematic = schematic
    
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
    
    def addWire(self, component1, component2):
        index1 = self.components.index(component1)
        index2 = self.components.index(component2)

    def snipWire(self, component1, component2):
        pass

    def addComponent(self, component):
        self.components.append(component)

    def deleteComponent(self, component):
        self.components.remove(component)

    def addLabel(self, component, label):
        index = self.components.index(component)
        self.components[index].addLabel(label)

    def save(self):
        pass

    def load(self):
        pass

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