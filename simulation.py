import networkx as nx
import functions as func
import numpy as np
import random as rnd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from collections import namedtuple

def createRoutingTable(lg):
    routingTable = []
    for road in lg.nodes:
        routingTable.append(dijkstra(lg, road))
    return routingTable

def dijkstra(lg, start):
    visited = []
    paths = []
    distances = []
    queue = []
    roads = []
    for road in lg.nodes:
        roads.append(road)
    for i in range(len(roads)):
        if roads[i] == start:
            distances.insert(i, 0)
            paths.insert(i, [])
            continue
        distances.insert(i, 1000)
        paths.insert(i, [])
    #visited.append(start)
    queue.append(start)
    while len(queue) > 0:
        current = queue.pop(0)
        visited.append(current)
        for adjacent in lg[current]:
            if func.isThere(visited, adjacent) == False:
                roadNumber = getRoadNumber(lg, adjacent)
                if distances[getRoadNumber(lg,current)] + 1 < distances[roadNumber]:
                    distances[roadNumber] = distances[getRoadNumber(lg,current)] + 1
                    path = paths[getRoadNumber(lg, current)][:]
                    path.append(adjacent)
                    paths[roadNumber] = path
                queue.append(adjacent)
    return paths

    
def getRoadNumber(lg, road):
    count = 0
    for node in lg.nodes:
        if node == road:
            return count
        count = count + 1
    return -1

def randomLocation(lg, exceptRoad):
    roads = list(lg.nodes)
    numberOfRoads = len(roads)
    random = None
    while True:
        random = rnd.randint(0,numberOfRoads-1)
        if roads[random] == exceptRoad:
            continue
        break
    return roads[random]

def getRoute(routingTable, lg, origin, destination):
    originNumber = getRoadNumber(lg, origin)
    destinationNumber = getRoadNumber(lg, destination)
    return routingTable[originNumber][destinationNumber]

def generateTrip(routingTable, lg, roadNetwork, i):
    trips = []
    route = []
    randInLocation = randomInLocation(roadNetwork)
    randLocation = randomLocation(lg, randInLocation)
    while len(getRoute(routingTable, lg, randInLocation, randLocation)) == 0:
        randLocation = randomLocation(lg, randInLocation)
    route = getRoute(routingTable, lg, randInLocation, randLocation)
    routeNew = []
    routeNew.append(randInLocation)
    for road in route:
        routeNew.append(road)
    trips.append(routeNew)
    randOutLocation = randomOutLocation(roadNetwork)
    while len(getRoute(routingTable, lg, randLocation, randOutLocation)) == 0:
        randOutLocation = randomOutLocation(roadNetwork)
    trips.append(getRoute(routingTable, lg, randLocation, randOutLocation))
    return trips

def analyzeResults(carsNumber, catchT, catchR, catchE, catchedCarsT, catchedCarsR, catchedCarsE):
    averageDegreeT = catchT / len(catchedCarsT)
    averageDegreeR = catchR / len(catchedCarsR)
    averageDegreeE = catchE / len(catchedCarsE)
    chart1(carsNumber, catchT, catchR, catchE, catchedCarsT, catchedCarsR, catchedCarsE)
    chart2(averageDegreeT, averageDegreeR, averageDegreeE)
    plt.show()

def randomInLocation(roadNetwork):
    inLocations = []
    if roadNetwork == 1:
        inLocations = [(1,2),(3,6)]
    elif roadNetwork == 2:
        inLocations = [(1,4),(3,4),(3,10),(10,3),(10,11)]
    elif roadNetwork == 3:
        inLocations = [(1,2),(1,7),(13,14),(13,18),(23,24),(24,25),(24,19),(26,27),(26,21),(22,21),(22,27),(12,11),(12,17),(6,12)]
    rand = rnd.randint(0,len(inLocations)-1)
    return inLocations[rand]

def randomOutLocation(roadNetwork):
    outLocations = []
    if roadNetwork == 1:
        outLocations = [(5,4),(3,6)]
    elif roadNetwork == 2:
        outLocations = [(5,2),(9,6),(5,6),(6,9),(13,9),(12,13),(9,13)]
    elif roadNetwork == 3:
        outLocations = [(1,7),(8,7),(13,18),(19,18),(18,23),(20,25),(24,25),(22,27),(26,27),(12,17),(16,17),(5,6)]
    rand = rnd.randint(0,len(outLocations)-1)
    return outLocations[rand]

def chart1(carsNumber, catchT, catchR, catchE, catchedCarsT, catchedCarsR, catchedCarsE):
    catchNumbers = (catchT, catchR, catchE)
    catchedCars = (len(catchedCarsT), len(catchedCarsR), len(catchedCarsE))
    n_groups = 3

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, catchNumbers, bar_width,
                    alpha=opacity, color='b',
                    yerr=(0,0,0), error_kw=error_config,
                    label='Yakalanma Sayısı')

    rects2 = ax.bar(index + bar_width, catchedCars, bar_width,
                    alpha=opacity, color='r',
                    yerr=(0,0,0), error_kw=error_config,
                    label='Yakalanan Araç Sayısı')

    ax.set_xlabel('')
    ax.set_ylabel('Skor')
    ax.set_title('Simülasyon Sonuçları')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(('Minimum Kesişim Kümesi', 'Rastgele', 'Deneyim Bazlı'))
    ax.legend()

    fig.tight_layout()

def chart2(averageDegreeT, averageDegreeR, averageDegreeE):
    averageDegrees = (averageDegreeT, averageDegreeR, averageDegreeE)
    n_groups = 3

    fig, ax = plt.subplots()

    index = np.arange(n_groups)
    bar_width = 0.35

    opacity = 0.4
    error_config = {'ecolor': '0.3'}

    rects1 = ax.bar(index, averageDegrees, bar_width,
                    alpha=opacity, color='g',
                    yerr=(0,0,0), error_kw=error_config,
                    label='Ortalama Değer')

    ax.set_xlabel('')
    ax.set_ylabel('Skor')
    ax.set_title('Simülasyon Sonuçları')
    ax.set_xticks(index)
    ax.set_xticklabels(('Minimum Kesişim Kümesi', 'Rastgele', 'Deneyim Bazlı'))
    ax.legend()

    fig.tight_layout()
