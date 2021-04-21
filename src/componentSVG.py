from xml.dom import minidom

# function returns an xmldoc (can be converted/shown as svg) of a
# component with one of the pins toggled (filled in or not).
# For toggling pin within an xml version.


class ComponentSVG:
    def __init__(self, base_file_name="", base_xml=None):
        if not base_file_name == "" and base_xml == None:
            self.base_xml = minidom.parse(base_file_name)
        else:
            self.base_xml = minidom.parseString(base_xml.toxml())
        self.active_xml = self.base_xml

    # For filling in the pin to make it obvious it has been connected to.
    def change_pin_state(self, pin_number, new_state):
        # These are the two options: transparent or black - disconnected or connected.
        fill_options = ["none", "#000000"]
        fill = fill_options[new_state]

        # Get a searchable xml from the svg file and find the circle (pin) objects
        new_xml = self.active_xml
        pins = new_xml.getElementsByTagName("circle")

        # Split the style line into two sections: the fill section and the rest.
        # Then get the current fill
        style_line = pins[pin_number].attributes["style"].value
        current_fill = style_line.split(';', 1)[0].split(':')[1]

        # # This decides which element the new_fill will be based on the current_fill
        # current_state = not current_fill == fill_options[0]
        # new_fill = fill_options[not current_state]
        # new_state = not current_state

        style = f"fill:{fill};{style_line.split(';', 1)[1]}"
        pins[pin_number].attributes["style"].value = style

        # Update the active xml
        self.active_xml = new_xml

    # For debugging the xml output.
    def print_svg_file(self, file_name):
        with open(file_name, 'w') as f:
            self.active_xml.writexml(f)
