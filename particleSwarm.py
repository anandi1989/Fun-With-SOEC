'''
@uthor : Amit Nandi
Date : 29/11/2016

Particle swarm optimization Algorithm
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#PSO function
def PSO(f,minRange,maxRange,nParticles=100,maxItr=1000,c1=2,c2=2,w=0.5):
	import numpy as n
	trialSolution = n.empty([nParticles,len(minRange)])
	for i in range(nParticles):
		for j in range(len(minRange)):
			trialSolution[i][j] = n.random.uniform(minRange[j],maxRange[j])
	#bsttrialSolution = trialSolution
	bsttrialSolution = n.empty([nParticles,len(minRange)])
	for i in range(nParticles):
		for j in range(len(minRange)):
                	bsttrialSolution[i][j] = n.random.uniform(minRange[j],maxRange[j])

	velocity = n.empty([nParticles,len(minRange)])
	for i in range(nParticles):
		for j in range(len(minRange)):
			velocity[i][j] = n.random.uniform()
	itr = 0
	while itr!=maxItr:
		funValues = n.empty(nParticles)
		for i in range(nParticles):
			funValues[i] = f(trialSolution[i])

		for i in range(nParticles):
			best = min(funValues)
			tmp = n.where(funValues==min(funValues))
			pBest = bsttrialSolution[i]
			if funValues[i] < f(bsttrialSolution[i]):
				bsttrialSolution[i] = trialSolution[i]
				pBest = bsttrialSolution[i]
			gBest = trialSolution[tmp]
			velocity[i] = n.add(w*velocity[i], c1*n.random.uniform()*(n.subtract(pBest,trialSolution[i])),c2*n.random.uniform()*(n.subtract(gBest,trialSolution[i])))
			trialSolution[i] = n.add(trialSolution[i],velocity[i])
		itr = itr + 1
	bstValue = min(funValues)
	bstSolution = trialSolution[n.where(funValues==bstValue)]
	return list((bstValue,bstSolution))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
a = PSO(f,minRange,maxRange,nParticles=100,maxItr=1000,c1=2,c2=2,w=0.5)
