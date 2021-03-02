import classes

if __name__ == "__main__":
    testSchematic1 = classes.Schematic()
    kwargs = {'schematic': testSchematic1, 'typeOfComponent': "VoltageSource", 'id': 84, 'sPos': [0, 4]}
    testSchematic1.addComponent(**kwargs)
    kwargs = {'schematic': testSchematic1, 'typeOfComponent': "Resistor", 'id': 42, 'sPos': [0, 0]}
    testSchematic1.addComponent(**kwargs)
    kwargs = {'schematic': testSchematic1, 'typeOfComponent': "Capacitor", 'id': 21, 'sPos': [0, 2]}
    testSchematic1.addComponent(**kwargs)
    testSchematic1.save('test.json')