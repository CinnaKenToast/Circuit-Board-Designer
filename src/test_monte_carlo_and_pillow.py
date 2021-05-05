from os import terminal_size
from xml.dom import NO_DATA_ALLOWED_ERR
import classes
import numpy as np
from PIL import Image, ImageDraw


def main():
    # Create a schematic object:
    sch = classes.Schematic()
    # Use gui generated schematic:
    sch.load("jason_test_monte_through_gui.circ")

    do_monte_carlo(sch)
    convert_to_pcb_image(sch, "test_layout_conversion.png")
    # sch.update_all_pin_positions_to_trimmed_layout()

    sch.overwrite_save("test_conversion.json")


def do_monte_carlo(sch):
    # Monte_carlo w/ output:
    sch.set_monte_carlo_parameters(3, 0, .99)
    sch.monte_carlo(300)


def convert_to_pcb_image(sch, file_name):
    sch.convert_to_pcb_image()
    im = sch.converted_image
    im.save(file_name)


if __name__ == "__main__":
    main()
