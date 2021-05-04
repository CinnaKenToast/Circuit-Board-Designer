import classes
import numpy as np

if __name__ == "__main__":
    # Create a schematic
    test_schematic_1 = classes.Schematic()

    # Setup the inital states of the components and
    # add them to the schematic
    c1 = {"id": 0, "component_type": "Capacitor"}
    test_schematic_1.add_component(c1)
    c2 = {"id": 1, "component_type": "Capacitor"}
    test_schematic_1.add_component(c2)

    # Connect the components
    test_schematic_1.add_connection("0_0", "1_1")
    test_schematic_1.add_connection("0_1", "1_0")

    # Try one iteration of Monte Carlo
    test_schematic_1.monte_carlo(1)

    test_schematic_1.overwrite_save("monte_carlo_test_out")
