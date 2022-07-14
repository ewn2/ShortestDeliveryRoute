import Truck
from Truck import *
from myHashMap import *
from Location import *
from datetime import *
from math import *
import sys

# Floyd-Warshall Algorithm has a time complexity of O(n^3) as it traverses and compares each pair of nodes
# within the matrix (Space complexity O(n^2) in regard to the matrix)
def floydWarshall(graph):
    vertices = len(graph)
    distance = list(map(lambda i: list(map(lambda j: j, i)), graph))
    for h in range(vertices):
        for i in range(vertices):
            for j in range(vertices):
                distance[i][j] = min(float(distance[i][j]), float(distance[i][h]) + float(distance[h][j]))
    return distance

# Delivery Function calls the Floyd-Warshall Algorithm to find the shortest paths between all pairs of locations
# and then uses a quick nearest-neighbor algorithm to take those newfound shortest paths, time complexity O(n^2) from
# needing to go through all paths per each location within the route
def goDeliver(HMap, addressConversion, mileData, deliveringTruck):
    reducedGraph = []  # Reduces the Graph to only distances relevant to packages on the Truck

    for r in range(0, len(deliveringTruck.table)):
        reducedGraph.append(mileData[addressConversion[HMap.lookup(deliveringTruck.table[r]).packageAddress]])

    floydWarshall(reducedGraph)
    mileData = floydWarshall(mileData)

    while len(deliveringTruck.table) > 0:

        shortestPathStep = float(HMap.lookup(deliveringTruck.table[0]).packageDistanceTravelled)
        for i in range(len(deliveringTruck.table)):
            if float(HMap.lookup(deliveringTruck.table[i]).packageDistanceTravelled) <= shortestPathStep:
                shortestPathStep = float(HMap.lookup(deliveringTruck.table[i]).packageDistanceTravelled)
                packageID = deliveringTruck.table[i]

        for i in range(len(deliveringTruck.table)):
            distanceToDrive = float(mileData[addressConversion[HMap.lookup(packageID).packageAddress]][addressConversion[HMap.lookup(deliveringTruck.table[i]).packageAddress]])
            HMap.lookup(deliveringTruck.table[i]).packageDistanceTravelled = distanceToDrive

        alreadyDriven = float(mileData[addressConversion[deliveringTruck.location]][addressConversion[HMap.lookup(packageID).packageAddress]])

        truckTime = deliveringTruck.timeLog
        minutesToAdd = (alreadyDriven * (60/18))
        currentTime = (truckTime + timedelta(minutes=minutesToAdd))

        HMap.lookup(packageID).packageDeliveredAt = currentTime
        deliveringTruck.timeLog = currentTime
        HMap.lookup(packageID).packageCurrentStatus = ('DELIVERED AS OF ' + str(HMap.lookup(packageID).packageDeliveredAt))

        deliveringTruck.distanceLog(alreadyDriven)
        deliveringTruck.location = HMap.lookup(packageID).packageAddress
        deliveringTruck.table.remove(packageID)

    distanceBack = float(mileData[addressConversion[deliveringTruck.location]][addressConversion['4001 South 700 East']])
    deliveringTruck.distanceLog(distanceBack)
    deliveringTruck.timeLog = deliveringTruck.timeLog + timedelta(minutes=(distanceBack * (60 / 18)))
    print('Truck ' + str(deliveringTruck.truckID) + ' finished and returned to Hub at: ' + str(deliveringTruck.timeLog + timedelta(minutes=(distanceBack * (60 / 18)))))
    deliveringTruck.location = '4100 South 700 East'
