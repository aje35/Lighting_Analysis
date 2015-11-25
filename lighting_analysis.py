import matplotlib.pyplot as plt
import numpy as np
import random
#from deap import base, creator, tools

# import required lighting array and lamp array
requiredLighting = np.genfromtxt('Test_LightData2.csv', delimiter=',')
lamp = np.genfromtxt('Lamp01.csv', delimiter=',')

# fitness function that compares two arrays and scores with an under- or over-penalty
def fitness(inputArray,compareArray):
	underPenalty = -3
	overPenalty = -1
	totalScore = 0
	evalArray = np.subtract(inputArray, compareArray)
	for elements in evalArray.flat:
		if elements < 0:
			totalScore += elements*underPenalty
		if elements > 0:
			totalScore += elements*overPenalty
	return totalScore

# function to add sub-array (mat2) at a specific location (xycoor) in main array (mat1)
def addAtPos(mat1, mat2, xycoor):
    size_x, size_y = np.shape(mat2)
    coor_x, coor_y = xycoor
    end_x, end_y   = (coor_x + size_x), (coor_y + size_y)
    mat1[coor_x:end_x, coor_y:end_y] = mat1[coor_x:end_x, coor_y:end_y] + mat2
    return mat1

# heat map visualization of array
def plotHeatmap(array):
	im = plt.imshow(array, cmap='hot',  vmin = 0, vmax = 200)
	plt.axis('off')
	plt.colorbar(im, orientation='horizontal').set_label('Footcandles (fc)')
	plt.show()

# initialize achieved lighting array at same size of input array for lamps to be added to
achievedLighting = np.zeros((requiredLighting.shape[0],requiredLighting.shape[1]))

# design boundaries for lamp placement
xmin = 0
xmax = requiredLighting.shape[1] - lamp.shape[0]
ymin = 0
ymax = requiredLighting.shape[0] - lamp.shape[1]

# very basic randomized optimization (that's not working well)
first=1
for individual in range(0,100):
	for x in range(0,50):
		xrand = random.randint(xmin, xmax)
		yrand = random.randint(ymin, ymax)
		addAtPos(achievedLighting,lamp,(yrand,xrand))
	if first:
		highScore = fitness(requiredLighting,achievedLighting)
		bestOf = achievedLighting
		first=0
	if fitness(requiredLighting,achievedLighting) > highScore:
		bestOf = achievedLighting
		highScore = fitness(requiredLighting,achievedLighting)
	print highScore
	achievedLighting = np.zeros((requiredLighting.shape[0],requiredLighting.shape[1]))

plotHeatmap(requiredLighting)
plotHeatmap(bestOf)
