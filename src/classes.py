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
    
       
    def Component(self, id, s_pos, s_oreint):
        self.label = str()
        self.id = id
        self.s_pos = s_pos
        self.s_orient = s_orient
        self.p_pos = (int, int)
        self.p_orirent = [int][int]
        self.connections: {int:int}
        self.path = [int][int][int]
    
    def addLabel(self, label):
         raise NotImplementedError("Abstract method")

    def draw(self):
        raise NotImplementedError("Abstract method")

class Comment:
    def __init__(self):
        self.comment = str()
        self.location = (int,int)

    def Comment(self, comment):
        self.comment = comment
        self.location = (int, int)

    def editComment(self, comment):
        self.comment = comment

class Schematic:
    def __init__(self):
        self.components = [Component()]
        self.comments = [Comment()]
    
    def addWire(self, component1, component2):
        pass
    def snipWire(self, component1, component2):
        pass
    def addComponent(self, component):
        pass
    def deleteComponent(self, component):
        pass
    def addLabel(self, component, label):
        pass
    def save(self):
        pass
    def load(self):
        pass

class Resistor(Component):
    pass