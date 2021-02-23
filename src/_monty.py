import json


# Metropolis' Monte Carlo method. I need to put "from ._monty import monte_carlo" to Component class
def monte_carlo(self, filename):
    component_list = {}
    if not self.imported_components:
        component_list = json.loads(filename)
        imported_components = True



# A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm
def a_star():
