
def main():
    # read all the data in the file map.ex
    # and convert to a dictionatry list
    '''
    print('Enter a file for your map: ')
    fileName = input()
    '''
    f = open('ex1.map')
    mapData = ' '.join(f.readlines())
    mapData = eval(mapData)
    f.close()
    
    height = mapData['height']
    width = mapData['width']
    envMap = mapData['envMap']
    
    # at this point, mapData is a Python
    # data structure
    for rowIdx in range(height):
        for colIdx in range(width):
            print(envMap[rowIdx][colIdx], end=' ')
        print()
    print('----------------')
    print(envMap[0][4])
    '''
    start = [0][0]
    map = {}
    map[start] = 1
    print(map[start])

    print(len(envMap[0]))
    print(len(envMap))
    '''

    cameFrom = {}
    '''
    node = '0,0'
    row, col = node.split(',')
    cameFrom[node] = 15
    print(cameFrom[node])
    print(row, col)
    '''
    nodeMap = {}
    for col in range(4):
        for row in range(5):
            location = str(col)+','+str(row)
            nodeMap[location] = col + row
            print(location, nodeMap[location])

    print(len(nodeMap))


    arr = [[0 for col in range(4)] for row in range(5)]
if __name__ == '__main__':
    main()



