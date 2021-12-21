from Graph import *
import sys
import random

class ISPNetwork:

    def __init__(self):
        self.network = Graph()
        self.MST = Graph()

    def reset(self): # resets the color, distance, and predecessor in network
        for i in self.network:
            i.color = 'white'
            i.dist = 0
            i.pred = None

    def resetNetwork(self): # resets the color, distance, and predecessor in network
        for i in self.network:
            i.color = 'white'
            i.dist = sys.maxsize
            i.pred = None

    def resetMST(self): # resets the color, distance, and predecessor in MST
        for i in self.MST:
            i.color = 'white'
            i.dist = sys.maxsize
            i.pred = None

    def buildGraph(self, filename):
        lines = open(filename, 'r') # reads each line
        for line in lines:
            data = line.split(",") # splits into three objects, seperated by the comma
            self.network.addEdge(data[0], data[1], float(data[2]))
        pass

    def pathExist(self, router1, router2):
        ISPNetwork.reset(self) # calls reset function
        a = self.network.getVertex(router1) # sets the vertex of router1 to a
        vertQueue = Queue()
        vertQueue.enqueue(a)
        found = False # initialize found variable
        while (vertQueue.size() > 0):
            currentVert = vertQueue.dequeue()
            if currentVert != None: # Vert has to exist to continue
                for nbr in currentVert.getConnections(): # scans through all connections
                    if nbr.id == router2: # checks if connection matches router2
                        found = True # path exist so found is equal to true
                        break # breaks while loop

                    elif (nbr.getColor() == 'white'):
                        nbr.setColor('gray')
                        nbr.setDistance(currentVert.getDistance() + 1)
                        nbr.setPred(currentVert)
                        vertQueue.enqueue(nbr)
                currentVert.setColor('black')
            else:
                return False # if Vert does not exist, returns false
        return found # returns found variable, if no path exist will return false

    def buildMST(self):
        ISPNetwork.reset(self) # calls reset function
        start = self.network.getVertex(random)
        G = self.network # sets G variable to network
        pq = PriorityQueue()
        for v in G:
            v.setDistance(sys.maxsize)
            v.setPred(None)
        pq.buildHeap([(v.getDistance(), v) for v in G]) # builds heap
        while not pq.isEmpty():
            currentVert = pq.delMin()
            for nextVert in currentVert.getConnections(): # scans through connections
                newCost = currentVert.getWeight(nextVert)
                if nextVert in pq and newCost < nextVert.getDistance():
                    nextVert.setPred(currentVert)
                    nextVert.setDistance(newCost)
                    pq.decreaseKey(nextVert, newCost)

        for i in self.network: # iterates through every router
            for j in i.getConnections(): # iterates through every connection
                if j.getPred() == i: # if they are connected
                    self.MST.addEdge(i.getId(), j.getId(), i.getWeight(j)) # creates edge
                    self.MST.addEdge(j.getId(), i.getId(), i.getWeight(j))
        pass

    def findPath(self, router1, router2):
        ISPNetwork.resetMST(self) # calls reset function for MST
        start = self.MST.getVertex(router1) # sets starting point
        b = self.MST.getVertex(router2) # vertex for router2
        aGraph = self.MST
        path = [] # initialize list
        pq = PriorityQueue()
        if start == None or b == None: # if it does not exist return path not exist
            return "path not exist"

        else: # if it does exist
            start.setDistance(0)
            pq.buildHeap([(v.getDistance(), v) for v in aGraph]) # builds heap
            while not pq.isEmpty():
                currentVert = pq.delMin()
                for nextVert in currentVert.getConnections(): # scans through connections
                    newDist = currentVert.getDistance() \
                              + currentVert.getWeight(nextVert)
                    if newDist < nextVert.getDistance():
                        nextVert.setDistance(newDist)
                        nextVert.setPred(currentVert)
                        pq.decreaseKey(nextVert, newDist)

            while b is not None: # stops when b is None
                path.append(b.id) # appends b to path list
                b = b.getPred()
            path = path.__reversed__() # reverses list
            return " -> ".join(path) # creates a string of list objects with -> in-between
        pass

    def findForwardingPath(self, router1, router2):
        ISPNetwork.resetNetwork(self) # calls reset function for network
        start = self.network.getVertex(router1) # sets starting  point
        b = self.network.getVertex(router2) # vertex for router2
        aGraph = self.network
        path = [] # initialize list
        pq = PriorityQueue()
        if start == None or b == None: # if it does not exist returns path not exist
            return "path not exist"

        else:
            start.setDistance(0)
            pq.buildHeap([(v.getDistance(), v) for v in aGraph]) # builds heap
            while not pq.isEmpty():
                currentVert = pq.delMin()
                for nextVert in currentVert.getConnections(): # scans through connections
                    newDist = currentVert.getDistance() \
                              + currentVert.getWeight(nextVert)
                    if newDist < nextVert.getDistance():
                        nextVert.setDistance(newDist)
                        nextVert.setPred(currentVert)
                        pq.decreaseKey(nextVert, newDist)

            while b is not None: # continues till b is None
                path.append(b.id) # appends to the list path
                b = b.getPred()

            cost = 0 # initialize cost to zero
            i = len(path) - 1 # sets to last index in list
            while i > 0: # i has to be greater than zero
                x = self.network.getVertex(path[i]) # finds vertex of string
                y = self.network.getVertex(path[i-1])
                cost = cost + x.getWeight(y) # adds weight to cost variable
                i = i - 1 # sets i to i minus 1

            path = path.__reversed__() # reverses the path
            return " -> ".join(path) + " (" + str(cost) + ")" # returns the string and the cost of the path
        pass

    def findPathMaxWeight(self, router1, router2):
        ISPNetwork.resetNetwork(self) # calls reset function for network
        start = self.network.getVertex(router1) # sets starting point
        b = self.network.getVertex(router2) # vertex of router2
        aGraph = self.network
        path = [] # initializes list
        pq = PriorityQueue()
        if start == None or b == None: # if they do not exist return path not exist
            return "path not exist"

        else:
            start.setDistance(0)
            pq.buildHeap([(v.getDistance(), v) for v in aGraph]) # builds heap
            while not pq.isEmpty():
                currentVert = pq.delMin()
                for nextVert in currentVert.getConnections(): # scans through connections
                    weight = currentVert.getWeight(nextVert) # sets the weight for all the connections
                    newDist = max(currentVert.getDistance(), weight) # picks the max value
                    if newDist < nextVert.getDistance() and nextVert.getPred() is not currentVert:
                        nextVert.setDistance(newDist)
                        nextVert.setPred(currentVert)
                        pq.decreaseKey(nextVert, newDist)

            while b is not None: # continues till b is not none
                path.append(b.id) # appends b to path list
                b = b.getPred()
            path = path.__reversed__() # reverses the list

            return " -> ".join(path) # returns path list to a string
        pass

    @staticmethod
    def nodeEdgeWeight(v):
        return sum([w for w in v.connectedTo.values()])

    @staticmethod
    def totalEdgeWeight(g):
        return sum([ISPNetwork.nodeEdgeWeight(v) for v in g]) // 2


if __name__ == '__main__':
    print("--------- Task1 build graph ---------")
    # Note: You should try all six dataset. This is just a example using 1221.csv
    net = ISPNetwork()
    net.buildGraph('1221.csv')

    print("--------- Task2 check if path exists ---------")
    routers = [v.id for v in random.sample(list(net.network.vertList.values()), 5)]
    for i in range(4):
        print('Router1:', routers[i], ', Router2:', routers[i+1], 'path exist?:', net.pathExist(routers[i], routers[i+1]))

    print("--------- Task3 build MST ---------")
    net.buildMST()
    print('graph node size', net.MST.numVertices)
    print('graph total edge weights', net.totalEdgeWeight(net.MST))

    print("--------- Task4 find shortest path in MST ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPath(routers[i], routers[i+1]))

    print("--------- Task5 find shortest path in original graph ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findForwardingPath(routers[i], routers[i+1]))

    print("--------- Task6 find path in LowestMaxWeightFirst algorithm ---------")
    for i in range(4):
        print(routers[i], routers[i+1], 'Path:', net.findPathMaxWeight(routers[i], routers[i+1]))
