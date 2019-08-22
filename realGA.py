'''
@uthor : Amit Nandi
Date : 6/12/2016

Real coded Genetic Algorithm Algorithm
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#Fitness function
def fitnessValues(f,trialSolution,minRange,maxRange):
        import numpy as n
        funValues = n.empty(trialSolution.shape[0])
        for i in range(trialSolution.shape[0]):
                funValues[i] = f(trialSolution[i])
        return funValues

#Real coded GA function
def realGA(f,minRange,maxRange,noOfVariables,population=50,generation=1000,crossoverProb=0.8,mutationProb=0.03):
	import numpy as n
	trialSolution = n.empty([population,noOfVariables])
	for i in range(population):
		for j in range(noOfVariables):
			trialSolution[i][j] = n.array(n.random.uniform(minRange[j],maxRange[j]))

	for generations in range(generation):
		#Natural Selection using tournament selection
		naturalSelection = []
		funValues = fitnessValues(f,trialSolution,minRange,maxRange)
		while len(naturalSelection)!=population:
			tmp = n.random.random_integers(population,size=2)-1
			if funValues[tmp[0]] < funValues[tmp[1]]:
				naturalSelection.append(tmp[0])
			else:
				naturalSelection.append(tmp[1])
		trialSolution = trialSolution[naturalSelection]

		#Crossover using whole arithmetical crossover
		if n.random.uniform(0,1) < crossoverProb:
			tmp = n.random.random_integers(population,size=2)-1
			alpha = n.random.uniform(0,1)
			a = alpha*trialSolution[tmp[0]] + (1-alpha)*trialSolution[tmp[1]]
			b = alpha*trialSolution[tmp[1]] + (1-alpha)*trialSolution[tmp[0]]
			trialSolution[tmp[0]] = a
			trialSolution[tmp[1]] = b

		#Mutation using uniform mutation
		if n.random.uniform(0,1) < mutationProb:
			tmp = n.random.random_integers(population,size=1)-1
			tmp1 = n.random.random_integers(noOfVariables,size=1)-1
			trialSolution[tmp][tmp1] = n.random.uniform(minRange[tmp1],maxRange[tmp1])
		
		funValues = fitnessValues(f,trialSolution,minRange,maxRange)
        	bstValue = funValues.min()
		bstIndex = n.where(funValues==funValues.min())
		bstSolution = trialSolution[bstIndex[0][0]]

		return list((bstSolution,bstValue))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
noOfVariables = 2
a = realGA(f,minRange,maxRange,noOfVariables) 
