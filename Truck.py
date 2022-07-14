from myHashMap import HMap
from Package import Package


# Checks if any remaining packages still remain at the hub, to avoid attempting to load packages already in transit or
# delivered
def emptyCheck(providedHMap):
    for i in range(1, 41):
        if providedHMap.lookup(i).packageCurrentStatus == 'AT THE HUB':
            return False
    return True


# List of packages in a set order ensuring loading and deliveries align with restrictions provided in package manifest
packageList = [13, 14, 15, 16, 19, 20, 1, 29, 30, 31, 34, 37, 40, 2, 4, 21, 18, 36, 38, 3, 6, 28, 32, 25, 5, 7, 8, 39, 10, 11, 12, 17, 22, 23, 24, 26, 27, 33, 35, 9]
# List to record already taken packages for truck loading restriction reference
takenPackages = []


# Loading packages into instances of Truck with capacity limitations and package information manifest updates for
# pickup and current status data
def pickupPackages(providedHMap, truck):

    while len(truck.table) < 16 and not emptyCheck(providedHMap):
        for i in packageList:
            package = providedHMap.lookup(i)
            if package.packageTruckID == truck.truckID and len(truck.table) < 16 and package.packageID not in truck.table and package.packageID not in takenPackages:
                package.packageOutForDeliveryAt = truck.timeLog
                package.packageCurrentStatus = 'EN ROUTE'
                truck.insert(package.packageID)
                takenPackages.append(package.packageID)
            if package.packageTruckID == 0 and len(truck.table) < 16 and package.packageID not in truck.table and package.packageID not in takenPackages:
                package.packageOutForDeliveryAt = truck.timeLog
                package.packageCurrentStatus = 'EN ROUTE'
                truck.insert(package.packageID)
                takenPackages.append(package.packageID)
    print('Truck ' + str(truck.truckID) + ' packages: ' + str(truck.table))
    print('Truck ' + str(truck.truckID) + ' left at ' + str(truck.timeLog))


# Truck Class, data structure and associated functions for the usage of each instance of Truck, including necessary
# clerical details such as timelogs, miles travelled, packages on board, and current location for usage with delivery
# algorithm route progress
class Truck:
    def __init__(self, truckID, distanceDriven, timeLog, hub):
        self.truckID = truckID
        self.distanceDriven = distanceDriven
        self.timeLog = timeLog
        self.table = []
        self.at16 = False
        self.location = hub

    def insert(self, package):
        package_id = package
        self.table.append(package_id)
        return True

    def set(self, key):
        self.location = key

    def distanceLog(self, legOfJourney):
        self.distanceDriven += legOfJourney

    def getDistanceLog(self):
        return self.distanceDriven

    def timestamp(self, logEntry):
        self.timeLog = logEntry
