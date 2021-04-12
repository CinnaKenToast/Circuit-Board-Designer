import classes
import numpy as np

# If you ever need to know how to add and remove stuff from a schematic
# look in here.

if __name__ == "__main__":
    # Create a schematic
    test_schematic_1 = classes.Schematic()

    # Setup the inital states of the components and test adding them to the schematic
    vs1_kwargs = {"id": 84, "label": "v1", "component_type": "VoltageSource"}
    test_schematic_1.add_component(vs1_kwargs)
    r1_kwargs = {"id": 42, "label": "r1", "component_type": "Resistor"}
    test_schematic_1.add_component(r1_kwargs)
    # c1_kwargs = {'id': 21, "label": "c1", 'component_type': "Capacitor"}
    # test_schematic_1.add_component(c1_kwargs)

    # # Test adding a label to components
    # test_schematic_1.change_label(84, "V1")
    # test_schematic_1.change_label(42, "R1")
    # test_schematic_1.change_label(21, "C1")

    # # Test adding connections between 3 components
    # test_schematic_1.add_connection("84_0", "21_1")
    # test_schematic_1.add_connection("84_1", "42_0")
    # test_schematic_1.add_connection("21_0", "42_1")

    # Test adding connections between 2 components
    test_schematic_1.add_connection("84_0", "42_1")
    test_schematic_1.add_connection("84_1", "42_0")

    # # Short out voltage source and then unshort its pins
    # test_schematic_1.add_connection("84_1", "84_0")
    # test_schematic_1.remove_connection("84_1", "84_0")

    # # Setup the initial states of the comments and test adding them to the schematic
    # comm1_kwargs = {"id": 0, "text": "Hello, world!", "position": [10, 0]}
    # test_schematic_1.add_comment(comm1_kwargs)
    # comm2_kwargs = {"id": 1, "text": "Hello, 2nd world!", "position": [10, 5]}
    # test_schematic_1.add_comment(comm2_kwargs)

    # # Testing randomize_layout
    test_schematic_1.set_monte_carlo_parameters(3, 10)
    not_allowed_spots = test_schematic_1.not_allowed_pcb_spots()
    test_schematic_1.randomize_layout(not_allowed_spots)

    # # Print out the contents of each component
    # for component in test_schematic_1.components.values():
    #     print(component.to_string())

    # # Test the save function (output to test1.json)
    # file_name_1 = input("Filename:   ") + ".json"
    # file_name_1 = "test_output1.json"
    # test_schematic_1.save(file_name_1)

    # delete the schematic
    del test_schematic_1

    # # Test the load function (from test1.json) into a new schematic
    # test_schematic_2 = classes.Schematic()
    # test_schematic_2.load(file_name_1)

    # # To see how everything worked (save as test2.json)
    # file_name_2 = input("Filename:   ") + ".json"
    # test_schematic_2.save(file_name_2)
