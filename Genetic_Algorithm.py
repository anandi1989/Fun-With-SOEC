'''
@uthor : Amit Nandi
Date : 28/10/2016

Genetic Algorithm
'''

#Rosenbrock function
def f(x,a=1,b=100):
        return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#Mapping function to convert binary to decimals
def map(lower,upper,trialSolution):
	lower = float(lower)
	upper = float(upper)
	tmp = 0
	for i in range(len(trialSolution)):
		tmp = tmp + 2**i*trialSolution[i]
	return lower + ((upper - lower)/(2**len(trialSolution)-1))*tmp

#Fitness function
def fitnessValues(f,trialSolution,minRange,maxRange):
	import numpy as n
	funValues = n.empty(trialSolution.shape[0])
	for i in range(trialSolution.shape[0]):
		x = n.empty(trialSolution.shape[1])
		for j in range(trialSolution.shape[1]):
			x[j] = map(minRange[j],maxRange[j],trialSolution[i][j])
		funValues[i] = f(x)
	return funValues 

#GA function
def GA(f,minRange,maxRange,noOfVariables,byte=4,generation=100000,population=50,crossoverProb=0.8,mutationProb=0.03):
	import numpy as n
	trialSolution = n.empty([population,noOfVariables,byte])
	for i in range(population):
		for j in range(noOfVariables):
			trialSolution[i][j] = n.random.choice([0,1],size=byte)

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

		#Crossover using one point
		tmp = n.random.random_integers(population,size=2)-1
		tmp1 = n.random.random_integers(noOfVariables)-1
		tmp2 = n.random.random_integers(byte)-1
		if n.random.uniform(0,1) < crossoverProb:
			a = trialSolution[tmp[0]][tmp1][range(tmp2)]
			b = trialSolution[tmp[1]][tmp1][range(tmp2,byte,1)]
			c = trialSolution[tmp[1]][tmp1][range(tmp2)]
			d = trialSolution[tmp[0]][tmp1][range(tmp2,byte,1)]
			trialSolution[tmp[0]][tmp1] = n.append(a,b)
			trialSolution[tmp[1]][tmp1] = n.append(c,d)

		#Mutation using bit-flip
		tmp = n.random.random_integers(population)-1
		tmp1 = n.random.random_integers(noOfVariables)-1
		tmp2 = n.random.random_integers(byte)-1
		if n.random.uniform(0,1) < mutationProb:
			if trialSolution[tmp][tmp1][tmp2] == 0:
				trialSolution[tmp][tmp1][tmp2] = 1
			else:
				trialSolution[tmp][tmp1][tmp2] = 0

	funValues = fitnessValues(f,trialSolution,minRange,maxRange)
	bstValue = funValues.min()
	bstIndex = n.where(funValues==funValues.min())
	bstSolution = n.empty(noOfVariables)
	for i in range(noOfVariables):
		bstSolution[i] = map(minRange[i],maxRange[i],trialSolution[bstIndex[0][0]][i])

	return list((bstSolution,bstValue))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
noOfVariables = 2
a = GA(f,minRange,maxRange,noOfVariables)
print a
