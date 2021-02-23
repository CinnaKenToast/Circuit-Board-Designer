import json


# Metropolis' Monte Carlo method.
def monte_carlo(self, filename):
    component_list = {}
    if not self.imported_components:
        component_list = json.loads(filename)
        self.imported_components = True
    



# A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm
def a_star(self, component_list):
    print("What's up?")
