# -*- coding: utf-8 -*-
'''
Ken Shipley
'''
def h(start, goal):
    rowStart, colStart = start.split(',')
    rowGoal, colGoal = goal.split(',')
    #print('start', rowStart,colStart, 'goal', rowGoal, colGoal)
    return abs(int(rowGoal) - int(rowStart)) + abs(int(colGoal) + int(rowStart))

def reconstructPath(cameFrom, current):
    totalPath = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        totalPath.insert(0, current)
    
    return totalPath

# A* finds a path from start to goal
# h is the heuristic function. h(n) estimates the cost to reach goal from node n
def aStar(start, goal, h, envMap, height, width):
    '''
    start = 'row,col'
    goal = 'row,col'
    '''
    # The set of discovered nodes that may need to be (re-)expanded
    # Initially, only the start node
    # This is usually implemented as a min-heap or priority queue rather than a hash-set
    openSet = [start]

    # List of nodes already discovered and explored
    # Starts off empty
    # Once a node has been 'current it then goes here
    closeSet = []

    # For node n, cameFrom[n] is the node immediately preceding it on the cheapest path from start 
    # to n currently known
    cameFrom = {}

    # For node n, gScpre[n] is the cost of the cheapest path from start to n currently known
    gScore = {}
    for col in range(width):
        for row in range(height):
            location = str(row)+","+str(col)
            gScore[location] = -1 # Using -1 to represent infinity
    gScore[start] = 0



    # for node n, fScore[n] = gScore[n] + h(n). fScore[n] represents our current best guess as to 
    # how short a path from start to finish can be if it goes through n.
    fScore = {}
    for col in range(width):
        for row in range(height):
            location = str(col)+","+str(row)
            fScore[location] = -1 # Using -1 to represent infinity
    fScore[start] = h(start, goal)


    while len(openSet) is not 0:
        #print('------------CHECK NEW NODE-------------')
        # This operation can occue in O(n) time if openSet is a minHeap or a priority queue
        current = None # None for no node with lowest fScore
        for node in openSet:
            #print(openSet)
            if current is None:
                current = node
            else:
                #print(node, 'has fscore', fScore[node], current, 'has fscore', fScore[current])
                if fScore[node] < fScore[current]:
                    current = node
        #print("current is", current)
        if current == goal:
            #print(cameFrom)
            return reconstructPath(cameFrom, current)

        # Current node goes into the closed set
        closeSet.append(current)
        #print("closeSet is", closeSet)
        openSet.remove(current)
        #print("openSet is", openSet)


        row, col = current.split(',')
        row = int(row)
        col = int(col)
        neighbor1 = str(row + 1) + ',' + str(col)
        neighbor2 = str(row - 1) + ',' + str(col)
        neighbor3 = str(row) + ',' + str(col + 1)
        neighbor4 = str(row) + ',' + str(col - 1)
        neighbors = [neighbor1, neighbor2, neighbor3, neighbor4]

        
        for neighbor in neighbors:
                #print()
                #print('++++++++++++++++++++++++++++++')
                row, col = neighbor.split(',')
                row = int(row)
                col = int(col)
                #print("current is", current, "checking neighbor",neighbor)
                if row < 0 or row > height-1 or col < 0 or col > width-1:
                    #print("Skipped neighbor", neighbor, "OUT OF RANGE")
                    continue
                elif envMap[row][col] is 1:
                    #print("Skipped neighbor", neighbor, "NEIGHBOR IS OBSTACLE")
                    continue
                # tentaiveGScore is the distance from start to the neighbor through current
                tentativeGScore = gScore[current] + 1
                #print(neighbor, "has gScore of", gScore[neighbor])
                #print(neighbor, "has tentativeGScore of", tentativeGScore)
                if gScore[neighbor] is -1 or tentativeGScore < gScore[neighbor]:
                    # This path to neighbor is better than any previous one. Record it!
                    cameFrom[neighbor] = current
                    gScore[neighbor] = tentativeGScore
                    fScore[neighbor] = gScore[neighbor] + h(neighbor, goal)
                    #print(current, 'neighbor', neighbor, 'has gscore', gScore[neighbor], 'and hscore', h(neighbor, goal))
                    if neighbor not in closeSet:
                        #print(neighbor,'Added to openSet')
                        openSet.append(neighbor)
                        #print("closeSet is", closeSet)
                        #print("openSet is", openSet)
                        #print()


        # open set is empty but goal was never reached
    return None # Return None if path not found
def main():
    # read all the data in the file map.ex
    # and convert to a dictionatry list
    
    print('Enter a file for your map: ')
    fileName = input()
    f = open(fileName)
    mapData = ' '.join(f.readlines())
    mapData = eval(mapData)
    f.close()
    
    height = mapData['height']
    width = mapData['width']
    envMap = mapData['envMap']
    
    start = None
    goal = None

    # at this point, mapData is a Python
    # data structure
    for rowIdx in range(height):
        for colIdx in range(width):
            print(envMap[rowIdx][colIdx], end=' ')
            if envMap[rowIdx][colIdx] is 's':
                start = str(rowIdx)+','+str(colIdx)
            if envMap[rowIdx][colIdx] is 'g':
                goal = str(rowIdx)+','+str(colIdx)
        print()
    print('---------------------------')
    print('Start is', start, 'Goal is', goal)
    print('---------------------------')

    path = aStar(start, goal, h, envMap, height, width)
    if path is not None:
        for node in path:
            col, row = node.split(',')
            col = int(col)
            row = int(row)
            if envMap[col][row] is 's' or envMap[col][row] is 'g':
                continue
            else:
                envMap[col][row] = '+'
        for rowIdx in range(height):
            for colIdx in range(width):
                print(envMap[rowIdx][colIdx], end=' ')
                if envMap[rowIdx][colIdx] is 's':
                    start = str(rowIdx)+','+str(colIdx)
                if envMap[rowIdx][colIdx] is 'g':
                    goal = str(rowIdx)+','+str(colIdx)
            print()
        print('Path taken',path)

    else:
        print("Could not print path")

if __name__ == '__main__':
    main()