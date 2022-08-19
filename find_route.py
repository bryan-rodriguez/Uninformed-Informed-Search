import sys

#initialization of global variables
originCityArr = []
destCityArr = []
lengKiloArr = []
lengKiloArr2 = []
heuristic = {}
nodesExpan = 0
nodesGen = 0

# node class
class node:
    def __init__(self,cityName,pathCost=0,depth=0):
        self.cityName = cityName
        self.depth = depth
        self.pathCost = pathCost
        self.parentNode = None
        
# successor function, 
# parameter: cityName, string city name to generated successors
# returns a string list of city names
def successorFun(cityName):
    successors = []
    index = 0
    for x in range(0, len(originCityArr)):
        if(cityName == originCityArr[x]):
            successors.append(destCityArr[x])
        if(cityName == destCityArr[x]):
            successors.append(originCityArr[x])
        index+=1

    return successors

# expand function
# parameters:
# parentNode, a parent node to expand its successors
# isHeuristic, a boolean value to determine if a heursitic file was used.
# returns a list of nodes to be added to the fringe
def expand(parentNode, isHeuristic):
    successors = []
    for successor in successorFun(parentNode.cityName):
        tmpNode = node(successor)
        tmpNode.depth = parentNode.depth + 1
        if(isHeuristic == True):
            tmpNode.pathCost = getPathCost(parentNode.cityName, successor) + heuristic.get(successor)
        else:
            tmpNode.pathCost = parentNode.pathCost + getPathCost(parentNode.cityName, successor)
        tmpNode.parentNode = parentNode
        successors.append(tmpNode)
    return successors

# a get cost function to find the path cost of a node.
# used by fringe.sort() to organize the nodes by shortest path cost to longest
def getCost(tempNode):
    return tempNode.pathCost


# the uniform cost search algorithm with if/else modifications for A* search
# parameters:
# initial, a city string name of the origin city
# goal, a city string name of the destination city
# isHeuristic, a boolean value to determine if to use UCS or A*
# returns a node with the shortest distance 
def search(initial, goal, isHeuristic):
    closed = []
    fringe = []
    global nodesExpan
    global nodesGen
    if(isHeuristic == True):
        startNode = node(initial,pathCost=heuristic.get(initial))
    else:
        startNode = node(initial)
    nodesGen+=1
    fringe.append(startNode)
    while len(fringe) > 0:
        fringe.sort(key=getCost)
        nodesExpan+=1
        currNode = fringe.pop(0)
        if (currNode.cityName == goal):
            return currNode
        if currNode.cityName not in closed:
            closed.append(currNode.cityName)
            successors = expand(currNode, isHeuristic)
            for child in successors:
                nodesGen +=1
                fringe.append(child)
    if len(fringe) == 0:
        return None


# getPathCost function gets the path cost between two nodes
# parameters:
# fromNode, a string origin city
# toNode, a string destination city
# return, a number of the path cost between the cities
def getPathCost(fromNode, toNode):
    weight = 0
    index = 0
    for city in originCityArr:
        if(fromNode == city):
            if(destCityArr[index] == toNode):
                weight = lengKiloArr[index]
        if(toNode == city):
            if(destCityArr[index] == fromNode):
                weight = lengKiloArr[index]
        index+=1
    return weight


# printNode function prints the nodes generated, expanded, total distance, and the route
# parameters:
# goalNode, the goal node that contains the destination city
# nodesEx, global int variable to print how many nodes were expanded
# nodesGener, global int variable to print how many nodes were generated 
def printNode(goalNode, nodesEx, nodesGener):
    pathCost = 0
    print("nodes expanded: ", nodesEx)
    print("nodes generated: ", nodesGener)
    if(goalNode!= None):
        head = goalNode
        cities = []
        while head:
            cities.append(head.cityName)
            head = head.parentNode
        for x in range(0,len(cities) - 1):
            pathCost+=getPathCost(cities[x],cities[x+1])
        print("distance: %1.1f km" % pathCost)
        print("route:")
        cities.reverse()
        for x in range(0,len(cities) - 1):
            print('{0} to {1}, {2}.0 km'.format(cities[x],cities[x+1], getPathCost(cities[x],cities[x+1])))
    else:
        print("distance: infinity")
        print("route:")
        print("none")
    
        
        
# main funtion
def main(argv):
    # checkig if the number of arguments provided, if it is not 4 or 5 than exit
    arguLen = len(sys.argv)
    if (arguLen >= 6 or arguLen <= 3):
        print("not enough or too many arguments")
        print("please enter in the form of: find_route input_filename origin_city destination_city heuristic_filename")
        sys.exit(0)

    # getting variables from command line
    inputFileName = argv[1]
    origin_city = argv[2]
    destination_city = argv[3]
    isHeuristic = False

    # if a heuristic is provided than open file and process the data.
    # sets isHeuristic to true to 'turn on' A* search
    if(arguLen == 5):
        heuristic_filename = argv[4]
        try:
            heuristicFile = open(heuristic_filename, "r")
        except:
            print("couldn't open heuristic file")
            sys.exit(0)
        for line in heuristicFile:
            if(line != 'END OF INPUT'):
                key, value = line.split()
                heuristic[key] = int(value)
        isHeuristic = True

    # opens input file, if fails than exit
    try:
        inputFile = open(inputFileName, "r")
    except:
        print("couldn't open input file")
        sys.exit(0)
    
    # processing data to be used to create nodes
    for line in inputFile:
        if(line != 'END OF INPUT'):
            data = line.split(' ')
            originCityArr.append(data[0])
            destCityArr.append(data[1])
            lengKiloArr2.append(data[2])
    for dist in lengKiloArr2:
        lengKiloArr.append(int(dist.strip()))

    
    
    # start search for goal node, if isHeuristic is true than use A*
    # else use uniform cost search
    goal = search(origin_city,destination_city, isHeuristic)

    # print in the format used in mini project 1
    printNode(goal, nodesExpan, nodesGen)

if __name__ == '__main__':
    main(sys.argv)
