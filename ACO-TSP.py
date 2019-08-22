'''
@uthor : Amit Nandi
Date : 1/11/2016

Travelling Salesman Problem using - Ant-Colony Optimization 
'''

#Function to compute Path distance
def pathDistance(distanceMatrix,path):
        d = 0
        for i in range(len(path)-1):
                d = d + distanceMatrix[path[i],path[i+1]]
        return d

#ACO function
def ACO_TSP(distanceMatrix,pheromoneMatrix,nCities,nAnts=100,maxItr=1000,q0=0.8,deltaIncrease=0.7):
	closenessMatrix = distanceMatrix*pheromoneMatrix

	for itr in range(maxItr):
		minDist = 10e10
		for ants in range(nAnts):
			cities = range(nCities)
			path = [n.random.random_integers(nCities)-1]
			cities.remove(path[len(path)-1])
			for city in range(nCities-1):
				if n.random.uniform(0,1,size=1) < q0:
					tmp = n.where(closenessMatrix[path[len(path)-1]][cities]==min(closenessMatrix[path[len(path)-1]][cities]))
					path.append(cities[tmp[0][0]])
					cities.remove(cities[tmp[0][0]])
				else:
					prob = closenessMatrix[path[len(path)-1]][cities]/sum(closenessMatrix[path[len(path)-1]][cities])
					tmp = n.random.choice(cities,p=prob)			
       		                        path.append(tmp)
        	                        cities.remove(tmp)
			if pathDistance(closenessMatrix,path) < minDist:
				minDist = pathDistance(closenessMatrix,path)
				minPath = path
		for j in range(nCities-1):
			pheromoneMatrix[path[j]][path[j+1]] = pheromoneMatrix[path[j]][path[j+1]] + deltaIncrease*pheromoneMatrix[path[j]][path[j+1]]
	return list((minPath,minDist))

#Main
nCities = 6
import numpy as n
distanceMatrix = n.random.random_integers(36,size=36)
distanceMatrix = distanceMatrix.reshape((nCities,nCities))
for i in range(nCities):
	for j in range(nCities):
		distanceMatrix[i,j] = distanceMatrix[j,i]
n.fill_diagonal(distanceMatrix,0)
pheromoneMatrix = n.empty((nCities,nCities))
pheromoneMatrix.fill(1)
a = ACO_TSP(distanceMatrix,pheromoneMatrix,nCities)
print a
