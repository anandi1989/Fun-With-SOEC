'''
@uthor : Amit Nandi
Date : 28/10/2016

Function Optimizaton using - Ant-Colony Optimization 
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#ACO for function optimization
def ACO_functionOpti(f,minRange,maxRange,archiveSize=100,nAnts=100,maxItr=1000,t=0.005,rho=0.9):
	import numpy as n
	trialSolution = n.empty([archiveSize,len(maxRange)])
	for i in range(archiveSize):
		for j in range(len(maxRange)):
			trialSolution[i][j] = n.array(n.random.uniform(minRange[j],maxRange[j]))
	funValues = n.empty(archiveSize)
	for i in range(archiveSize):
		funValues[i] = f(trialSolution[i]) 

	bstValue = min(funValues)
	bstSolution = trialSolution[n.where(funValues==min(funValues))]

	pheromone = n.empty(archiveSize)
	for i in range(archiveSize):
		D = f(trialSolution[i]) - bstValue
		pheromone[i] = n.exp(-(D**2)/(2*t))
	pheromone = pheromone/sum(pheromone)

	itr = 0
	while itr!=maxItr:
		for ants in range(nAnts):
			dx = n.random.uniform(-pheromone[i],pheromone[i],size=len(maxRange))
			for i in range(archiveSize):
				trialSolution[i] = n.add(trialSolution[i],dx)
				funValues[i] = f(trialSolution[i])
			if min(funValues) < bstValue:
				bstValue = min(funValues)
				bstSolution = trialSolution[n.where(funValues==min(funValues))]
			else:
				bstValue = bstValue
				bstSolution = bstSolution
			pheromone = rho*pheromone
		itr = itr + 1 
	return list((bstValue,bstSolution))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
a = ACO_functionOpti(f,minRange,maxRange,archiveSize=100,nAnts=100,maxItr=1000,t=0.005,rho=0.9)
