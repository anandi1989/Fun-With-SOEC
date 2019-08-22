'''
@uthor : Amit Nandi
Date : 20/11/2016

Travelling Salesman Problem using - Genetic Algorithm 
'''

nCities = 6
import numpy as n
distanceMatrix = n.random.random_integers(36,size=36)
distanceMatrix = distanceMatrix.reshape((nCities,nCities))

for i in range(nCities):
        for j in range(nCities):
                distanceMatrix[i,j] = distanceMatrix[j,i]

n.fill_diagonal(distanceMatrix,0)
population = 10
generations = 10
crossoverProb = 0.8
mutationProb = 0.03

trialSolution = n.empty([population,nCities])
for i in range(population):
	trialSolution[i] = n.random.choice(nCities,nCities,replace=False)

def pathDistance(distanceMatrix,path):
        d = 0
        for i in range(len(path)-1):
                d = d + distanceMatrix[int(path[i]),int(path[i+1])]
        return d


for generation in range(generations):

	#Natural Selection using tournament selection
	naturalSelection = []
	while len(naturalSelection)!=population:
		tmp = n.random.random_integers(population,size=2)-1
		funValues = []
		funValues.append(pathDistance(distanceMatrix,trialSolution[tmp[0]]))
		funValues.append(pathDistance(distanceMatrix,trialSolution[tmp[1]]))
		if funValues[0] < funValues[1]:
			naturalSelection.append(tmp[0])
		else:
			naturalSelection.append(tmp[1])
	trialSolution = trialSolution[naturalSelection]

	#Crossover
	tmp = n.random.random_integers(population,size=2)-1
	if n.random.uniform(0,1) < crossoverProb:
		a = trialSolution[tmp[0]]
		b = trialSolution[tmp[1]]
		tmp1 = n.random.random_integers(trialSolution.shape[1],size=2)-1 
		c = n.empty(trialSolution.shape[1])
		c[tmp1[0]] = a[tmp1[0]]
		c[tmp1[1]] = a[tmp1[1]]
		tmp2 = n.delete(b,[n.where(b==a[tmp1[0]])[0][0],n.where(b==a[tmp1[1]])[0][0]])
		count = 0
		for i in range(trialSolution.shape[1]):
			if i!=tmp1[0] or i!=tmp1[1]:
				c[i] = b[count]
				count = count+1
		trialSolution[tmp[0]] = c
       		c = n.empty(trialSolution.shape[1])
	        c[tmp1[0]] = b[tmp1[0]]
	        c[tmp1[1]] = b[tmp1[1]]
	       	tmp2 = n.delete(a,[n.where(a==b[tmp1[0]])[0][0],n.where(a==b[tmp1[1]])[0][0]])
        	count = 0
        	for i in range(trialSolution.shape[1]):
                	if i!=tmp1[0] or i!=tmp1[1]:
                        	c[i] = a[count]
                        	count = count+1
        	trialSolution[tmp[1]] = c
	
	#Mutation
	tmp = n.random.random_integers(population)-1
	if n.random.uniform(0,1) < mutationProb:
		trialSolution[tmp] = n.random.choice(range(trialSolution.shape[1]),size=trialSolution.shape[1],replace=False)

	distance = n.empty(trialSolution.shape[0])
	for j in range(trialSolution.shape[0]):
		distance[j] = pathDistance(distanceMatrix,trialSolution[j])

	minDist = distance.min()
	optPath = trialSolution[n.where(distance==minDist)]
