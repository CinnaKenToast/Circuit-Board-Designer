import classes

if __name__ = "__main__":
    testSchematic1 = classes.Schematic()
    kwargs = {'id': 42, 'sPos': [0, 0], 'schematic': testSchematic1}
    testSchematic1.addComponent(**kwargs)
    testSchematic1.save('test.json')
