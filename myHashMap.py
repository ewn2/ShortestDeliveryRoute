# Hashmap for the storage of Package data entries, including insert and lookup functions for operational access to
# the map. The Map currently ACCOUNTS for key collisions, but is designed expecting packageID values to be unique due
# to the low amount of packages currently being processed
class HMap:
    def __init__(self):
        self.size = 1024
        self.map = []
        for i in range(self.size):
            self.map.append([])

# Custom hash function implementation that serves to provide key values that are one-to-one
    def __hash__(self):
        return hash(id(self))

# Hashmap insert function designed to take in Package entries and incorporate them as paired entries between a hashed
# key value based on their Package ID and a list entry of all of their associated data as the value
    def insert(self, key, value):
        packageKey = hash(key)
        packageInventory = self.map[packageKey]
        packageDetails = [packageKey, value]
        for pair in packageInventory:
            if pair[0] == packageKey:
                pair[1] = value
                return True
        packageInventory.append(packageDetails)
        return True

# Hashmap lookup function designed to accept a package ID value and return the value portion associated with the pair of
# a stored key and value
    def lookup(self, key):
        packageKey = hash(key)
        if self.map[packageKey] is not None:
            for pair in self.map[packageKey]:
                if pair[0] == packageKey:
                    return pair[1]
        return None

    def print(self):
        i = 0
        for item in self.map:
            if item is not None:
                for subitem in item:
                    if subitem is not None:
                        for subsubitem in subitem:
                            if subsubitem is not None:
                                i += 1
                                if (i % 2) == 0:  # so only package Details are printed, not keys
                                    print(subsubitem)
