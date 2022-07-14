# Erwin Uppal
import copy
import time
import myHashMap
import Package
from Package import add
from Truck import Truck
from Truck import pickupPackages
from datetime import datetime
from Location import *
from algorithm import *


# Erwin Uppal
# Program first reads in delivery location information including distances as a graph, then constructs "Trucks" that
# load up on up to 16 packages (with varying start times to account for delayed or incorrect delivery information) and
# proceeds to "Deliver" those packages through the goDeliver function, only allowing the third truck with the final few
# packages to leave once both a driver from Truck 1 or 2 has returned and the incorrectly labelled package 9 has its
# delivery location corrected.
# Afterwards, the program displays information on Truck travel times and the total mileage of the Trucks combined, and
# offers a menu to the user to display information including the status of specific or all packages at specific times.
# Flow: Location and Package information is loaded into the program, a package is loaded into a truck, either to a
# specifically required one or subject to availability based on requirements of other packages and capacity availability.
# Destination data for all packages loaded into a specific truck is passed through the Floyd-Warshall algorithm and the
# shortest route is selected for the order of deliveries to make, Truck proceeds to follow that route and then return
# to the hub after delivering all packages, whereupon it loads more if available or simply ends for the day.
# The total travelled miles of each truck for the day once package delivery has been concluded is added and saved
# for display to User.
# Run with main.py
if __name__ == '__main__':

    mileData = cacheLocations('LocationDistances.csv')
    addressConversion = cacheDistances('LocationDistances.csv')

    packageHMap = myHashMap.HMap()
    add('Packages.csv', packageHMap, mileData, addressConversion)

    truck1 = Truck(1, 0.0, datetime.strptime(str(datetime.today().date()) + ' 08:00 AM', "%Y-%m-%d %I:%M %p"), '4001 South 700 East')
    truck2 = Truck(2, 0.0, datetime.strptime(str(datetime.today().date()) + ' 09:05 AM', "%Y-%m-%d %I:%M %p"), '4001 South 700 East')

    pickupPackages(packageHMap, truck1)
    goDeliver(packageHMap, addressConversion, mileData, truck1)
    print('')
    pickupPackages(packageHMap, truck2)
    goDeliver(packageHMap, addressConversion, mileData, truck2)
    print('')

    driverAvailableTime = ' 10:20 AM'
    availableTruckDriver = truck1
    if truck2.timeLog < truck1.timeLog:
        availableTruckDriver = truck2
    defaultTime = True
    if availableTruckDriver.timeLog >= (datetime.strptime(str(datetime.today().date()) + driverAvailableTime, "%Y-%m-%d %I:%M %p")):
        driverAvailableTime = str(availableTruckDriver.timeLog)
        defaultTime = False

    if defaultTime:
        truck3 = Truck(3, 0.0, datetime.strptime(str(datetime.today().date()) + driverAvailableTime, "%Y-%m-%d %I:%M %p"), '4001 South 700 East')
    else:
        truck3 = Truck(3, 0.0, datetime.strptime(driverAvailableTime, "%Y-%m-%d %I:%M:%S"), '4001 South 700 East')
    pickupPackages(packageHMap, truck3)
    goDeliver(packageHMap, addressConversion, mileData, truck3)
    print('')

    TMD = truck1.distanceDriven + truck2.distanceDriven + truck3.distanceDriven
    print('Total Miles Driven: ' + str(TMD) + '\n')

    EndProgram = False
    while EndProgram is not True:
        userinput = 0
        print('Please make a selection')
        print('1. Check status of all packages\n2. Check status of all packages at specific time\n3. Check status of specific package\n4. Check status of specific package at specific time\n5. Show Total Miles Driven again\n6. Exit program')
        userinput = input('Select Option: ')
        if userinput == str(1):
            packageHMap.print()
        elif userinput == str(2):
            tempInput = None
            chosenTime = None
            tempID = 1
            tempPackageHMap = myHashMap.HMap()
            validInput = True

            tempInput = input('Enter time in 24-hour format (ex. 13:45) to check for status of packages\n')
            try:
                chosenTime = datetime.strptime(str(datetime.today().date()) + ' ' + tempInput, "%Y-%m-%d %H:%M")
            except ValueError:
                print('Not a properly formatted time entry')
                validInput = False

            if validInput:
                chosenTime = datetime.strptime(str(datetime.today().date()) + ' ' + tempInput, "%Y-%m-%d %H:%M")
                tempPackageHMap = copy.deepcopy(packageHMap)
                while tempID <= 40:
                    if chosenTime < tempPackageHMap.lookup(int(tempID)).packageOutForDeliveryAt:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('AT THE HUB AS OF ' + str(chosenTime))
                    elif tempPackageHMap.lookup(int(tempID)).packageOutForDeliveryAt <= chosenTime < packageHMap.lookup(int(tempID)).packageDeliveredAt:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('EN ROUTE AS OF ' + str(chosenTime))
                    elif tempPackageHMap.lookup(int(tempID)).packageDeliveredAt <= chosenTime:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('DELIVERED AS OF ' + str(tempPackageHMap.lookup(int(tempID)).packageDeliveredAt))
                    tempID = tempID + 1
                tempPackageHMap.print()

            try:
                input('Press Enter to return to menu')
            except SyntaxError:
                pass
        elif userinput == str(3):
            tempID = input('Enter ID # of package to view\n')
            if tempID.isnumeric() is False:
                print('Not a valid package ID #')
            elif int(tempID) in range(1, 41):
                print('Package ' + str(packageHMap.lookup(int(tempID)).packageID) + ' was delivered at ' + str(packageHMap.lookup(int(tempID)).packageDeliveredAt))
                print('Package ID: ' + str(packageHMap.lookup(int(tempID))))
            else:
                print('Not a valid package ID #')
            try:
                input('Press Enter to return to menu')
            except SyntaxError:
                pass

        elif userinput == str(4):
            tempID = input('Enter ID # of package to view\n')
            if tempID.isnumeric() is False:
                print('Not a valid package ID #')
            elif int(tempID) in range(1, 41):

                tempInput = input('Enter time in 24-hour clock format (ex. 13:45, 09:00, 08:30) to check for status of packages\n')
                validInput = True
                try:
                    chosenTime = datetime.strptime(str(datetime.today().date()) + ' ' + tempInput, "%Y-%m-%d %H:%M")
                except ValueError:
                    print('Not a properly formatted time entry')
                    validInput = False
                if validInput:
                    chosenTime = datetime.strptime(str(datetime.today().date()) + ' ' + tempInput, "%Y-%m-%d %H:%M")
                    tempPackageHMap = copy.deepcopy(packageHMap)

                    if tempPackageHMap.lookup(int(tempID)).packageOutForDeliveryAt > chosenTime:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('AT THE HUB AS OF ' + str(chosenTime))
                    elif tempPackageHMap.lookup(int(tempID)).packageOutForDeliveryAt <= chosenTime < tempPackageHMap.lookup(int(tempID)).packageDeliveredAt:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('EN ROUTE AS OF ' + str(chosenTime))
                    elif tempPackageHMap.lookup(int(tempID)).packageDeliveredAt <= chosenTime:
                        tempPackageHMap.lookup(int(tempID)).packageCurrentStatus = ('DELIVERED AS OF ' + str(tempPackageHMap.lookup(int(tempID)).packageDeliveredAt))

                    print('Package ID: ' + str(tempPackageHMap.lookup(int(tempID))))

            else:
                print('Not a valid package ID #')
            try:
                input('Press Enter to return to menu')
            except SyntaxError:
                pass

        elif userinput == str(5):
            print('Total Miles Driven: ' + str(TMD))
            try:
                input('Press Enter to return to menu')
            except SyntaxError:
                pass
        elif userinput == str(6):
            EndProgram = True
        else:
            print('Please make a valid selection')

    print('Goodbye!')