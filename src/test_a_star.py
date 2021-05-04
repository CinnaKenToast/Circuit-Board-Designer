from xml.dom import NO_DATA_ALLOWED_ERR
import classes
import numpy as np

if __name__ == "__main__":
    # Create a schematic object
    test_schematic_1 = classes.Schematic()

    # Setup the inital states of the components and add them to the schematic
    c1 = {"id": 0, "component_type": "Capacitor"}
    test_schematic_1.add_component(c1)
    c2 = {"id": 1, "component_type": "Capacitor"}
    test_schematic_1.add_component(c2)

    # Add connections between the 2 components
    test_schematic_1.add_connection("0_0", "1_1")
    test_schematic_1.add_connection("0_1", "1_0")

    # Setup a layout.
    test_schematic_1.set_monte_carlo_parameters(3, 2, 10)
    test_schematic_1.randomize_layout()
    test_schematic_1.initialize_pin_placement_dict()
    test_schematic_1.initialize_connections_list()

    # See where the components are.
    test_schematic_1.print_all_components_strings()

    # Do what A* should do
    not_allowed = test_schematic_1.not_allowed_pcb_spots()
    grid = classes.PcbGrid(test_schematic_1.n_grid_spaces +
                           test_schematic_1.grid_padding, not_allowed)

    start_pos = test_schematic_1.pin_placement_dict[test_schematic_1.connections_list[0][0]]
    goal_pos = test_schematic_1.pin_placement_dict[test_schematic_1.connections_list[0][1]]

    start_node = grid.node_at(start_pos)
    goal_node = grid.node_at(goal_pos)

    path = grid.a_star(start_node, goal_node)

    print(path)

    # # Run A* on the layout.
    # test_schematic_1.paths = test_schematic_1.run_a_star()

    # test_schematic_1.overwrite_save("a_star_test_out")
