import classes
import numpy as np

# If you ever need to know how to add and remove stuff from a schematic
# look in here.

if __name__ == "__main__":
    # Create a schematic
    test_schematic_1 = classes.Schematic()

    # Setup the inital states of the components and test adding them to the schematic
    c1 = {"id": 0, "component_type": "Capacitor"}
    test_schematic_1.add_component(c1)
    c2 = {"id": 1, "component_type": "Capacitor"}
    test_schematic_1.add_component(c2)
    c3 = {'id': 2, 'component_type': "Capacitor"}
    test_schematic_1.add_component(c3)
    # d1 = {'id': 3, 'label': 'D1', 'component_type': 'Diode'}
    # test_schematic_1.add_component(d1)

    # Test removing a component
    # test_schematic_1.remove_component(c1['id'])

    # # Test adding a label to components
    # test_schematic_1.edit_label(0, "C1")
    # test_schematic_1.edit_label(1, "C2")
    # # test_schematic_1.edit_label(2, "C3")

    # Test adding connections between some components
    test_schematic_1.add_connection("0_0", "1_1")
    test_schematic_1.add_connection("0_1", "2_0")
    test_schematic_1.add_connection("1_0", "2_1")

    # # Test adding connections between 2 components
    # test_schematic_1.add_connection("0_0", "1_1")
    # test_schematic_1.add_connection("0_1", "1_0")

    # test_schematic_1.get_component("0").print_svg("cap1.svg")
    # test_schematic_1.get_component("1").print_svg("cap2.svg")

    # # Test setting the schematic position
    # test_schematic_1.set_component_schematic_pos("0", 200, 200)
    # test_schematic_1.set_component_schematic_pos("1", 100, 200)

    # # Short out a component and then unshort its pins (test removing a connection)
    # test_schematic_1.add_connection("0_1", "0_0")
    # test_schematic_1.remove_connection("0_1", "0_0")

    # # Setup the initial states of the comments and test adding them to the schematic
    # comm1_kwargs = {"id": 0, "text": "Hello, world!", "position": [10, 0]}
    # test_schematic_1.add_comment(comm1_kwargs)
    # comm2_kwargs = {"id": 1, "text": "Hello, 2nd world!", "position": [10, 5]}
    # test_schematic_1.add_comment(comm2_kwargs)

    # Testing randomize_layout
    test_schematic_1.set_monte_carlo_parameters(3, 10, 2)
    not_allowed_spots = []
    test_schematic_1.randomize_layout(not_allowed_spots)

    # Print out the contents of each component
    test_schematic_1.print_all_components_strings()

    # Test initialization of pin_placement_dict, connection list, and connections_of_pins list
    test_schematic_1.initialize_pin_placement_dict()
    test_schematic_1.initialize_connections_list()
    test_schematic_1.initialize_connections_of_pins_list()

    print(test_schematic_1.connections_of_pins)

    # # Test the save function (output to test1.json)
    # file_name_1 = input("Filename:   ") + ".json"
    file_name_1 = "test_classes.json"
    test_schematic_1.save(file_name_1)

    # delete the schematic
    del test_schematic_1

    # # Test the load function (from test1.json) into a new schematic
    # test_schematic_2 = classes.Schematic()
    # test_schematic_2.load(file_name_1)

    # # To see how everything worked (save as test2.json)
    # file_name_2 = input("Filename:   ") + ".json"
    # test_schematic_2.save(file_name_2)
