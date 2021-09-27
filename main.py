# Maybe do a city object with an ID and an array that has the distances to every other city?
# Need to read in the file and put it in an adjacency matrix

CityData = open("Sample Cities (Size 15).txt", "r")
TestMatrix = [[0 for x in range(15)] for y in range(15)]
print(TestMatrix)
