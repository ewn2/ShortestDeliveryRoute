import re
from datetime import datetime
import csv


# Add function for processing new Packages that also accounts for known restrictions to the packages and translates
# information to usable values (i.e. EOD delivery to 5pm, package MUST be on Truck 2, etc.)
def add(csvFileName, anHMap, mileData, addressConversion):
    with open(csvFileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            packageID = int(row[0])
            regexEdit = re.sub(r'\([^)]*\)||\n', '', row[1])
            packageAddress = regexEdit
            packageCity = row[2]
            packageState = row[3]
            packageZip = row[4]
            if row[5] == 'EOD':
                row[5] = '5:00 PM'  # Assuming business hours 8am-5pm
            packageDeadline = datetime.strptime(str(datetime.today().date()) + ' ' + row[5], "%Y-%m-%d %I:%M %p")
            packageKgMass = row[6]
            packageNotes = row[7]
            packageDistanceTravelled = mileData[0][addressConversion.get(packageAddress)]
            packageCurrentStatus = 'AT THE HUB'
            package = Package(packageID, packageAddress, packageCity, packageState, packageZip, packageDeadline,
                              packageKgMass, packageNotes, packageDistanceTravelled, packageCurrentStatus)

            def clericalUpdates(readPackageID):
                match readPackageID:
                    case 13 | 14 | 15 | 16 | 19 | 20:
                        package.packageTruckID = 1
                    case 3 | 18 | 36 | 38:
                        package.packageTruckID = 2
                    case 6 | 25 | 28 | 32:
                        package.packageDelayedShipping = True
                    case 9:
                        package.address = '410 South State St'
                        package.zip = '84111'
                        package.packageDelayedShipping = True

            clericalUpdates(packageID)
            anHMap.insert(packageID, package)

# Package data structure, accounts for all required details as well as a redefinition of the string call to ensure actual
# values are passed instead of memory references
class Package:
    def __init__(self, packageID, packageAddress, packageCity, packageState, packageZip, packageDeadline, packageKgMass, packageNotes, packageDistanceTravelled, packageCurrentStatus):
        self.packageID = packageID
        self.packageAddress = packageAddress
        self.packageCity = packageCity
        self.packageState = packageState
        self.packageZip = packageZip
        self.packageDeadline = packageDeadline
        self.packageKgMass = packageKgMass
        self.packageNotes = packageNotes
        self.packageDistanceTravelled = packageDistanceTravelled
        self.packageCurrentStatus = packageCurrentStatus
        self.packageTruckID = 0
        self.packageDelayedShipping = False
        self.packageOutForDeliveryAt = 'AT THE HUB'
        self.packageDeliveredAt = "Not Yet Delivered"

    def __str__(self):
        return "%s, %s, %s, %s, %s,%s, %s, %s, %s, %s" % (self.packageID, self.packageAddress, self.packageCity, self.packageState, self.packageZip, self.packageDeadline, self.packageKgMass, self.packageNotes, self.packageDistanceTravelled, self.packageCurrentStatus)


