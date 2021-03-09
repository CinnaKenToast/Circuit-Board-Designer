import classes

if __name__ == "__main__":
    # Create a schematic
    test_schematic_1 = classes.Schematic()

    # Setup the inital states of the components and test adding them to the schematic
    vs1_kwargs = {"id": 84, "component_type": "VoltageSource",
                  "schem_position": [0, 0]}
    test_schematic_1.add_component(vs1_kwargs)
    r1_kwargs = {"id": 42, "component_type": "Resistor",
                 "schem_position": [0, 0]}
    test_schematic_1.add_component(r1_kwargs)
    c1_kwargs = {'id': 21, 'component_type': "Capacitor",
                 'schem_position': [0, 2]}
    test_schematic_1.add_component(c1_kwargs)

    # Test adding a label to components
    test_schematic_1.change_label(84, "V1")
    test_schematic_1.change_label(42, "R1")
    test_schematic_1.change_label(21, "C1")

    # Test adding connections to components
    test_schematic_1.add_connection("84_0", "21_1")
    test_schematic_1.add_connection("84_1", "42_0")
    test_schematic_1.add_connection("21_0", "42_1")

    # Short out voltage source and then unshort its pins
    test_schematic_1.add_connection("84_1", "84_0")
    test_schematic_1.remove_connection("84_1", "84_0")

    # Setup the initial states of the comments and test adding them to the schematic
    comm1_kwargs = {"id": 0, "text": "Hello, world!", "position": [10, 0]}
    test_schematic_1.add_comment(comm1_kwargs)
    comm2_kwargs = {"id": 1, "text": "Hello, 2nd world!", "position": [10, 5]}
    test_schematic_1.add_comment(comm2_kwargs)

    # Test the save function (output to test1.json)
    test_schematic_1.save("test_in.json")

    # delete the schematic
    del test_schematic_1

    # Test the load function (from test1.json) into a new schematic
    test_schematic_2 = classes.Schematic()
    test_schematic_2.load("test_in.json")

    # To see how everything worked (save as test2.json)
    test_schematic_2.save("test_out.json")
