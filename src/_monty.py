import json

# Metropolis' Monte Carlo method.
def monteCarlo(self, filename):
    componentList = [Component()]
    # if we haven't imported the components from the json input file, do that
    if not self.importedComponentsForMonteCarlo:
        componentList = json.loads(filename)
        self.importedComponentsForMonteCarlo = True
    
    
def checkGood(self):
    aStar(self.componentList)


# A* as defined on https://en.wikipedia.org/wiki/A*_search_algorithm
def aStar(self):
    print("What's up?")
