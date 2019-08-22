'''
@uthor : Amit Nandi
Date : 15/11/2016

Multi Objective Optimization using - Genetic Algorithm 
'''

#Functions to minimized
def f1(x):
	return 4*x[0]**2+4*x[1]**2

def f2(x):
        return (x[0]-5)**2 + (x[1]-5)**2

#Function to compute Crowding distance
def crowdingDist(nonDominatedFront,tmp):
	import numpy as n
	if tmp==0 or tmp==nonDominatedFront.shape[0]-1:
		I = 10000
	else:
		a = nonDominatedFront[tmp]
		q=n.argsort(nonDominatedFront[:,0])
		sortedSol = nonDominatedFront[q]
		tmp1 = n.where(sortedSol[:,0]==a[0])
		if tmp1[0][0]==0 or tmp1[0][0]==sortedSol.shape[0]-1:
			I = 10000
		else:
			I = (sortedSol[tmp1[0][0]+1,0] - sortedSol[tmp1[0][0]-1,0]) + (sortedSol[tmp1[0][0]+1,1] - sortedSol[tmp1[0][0]-1,1])
	return I

#GA multiobjective function
def GA_multiObj(func,minRange,maxRange,noOfVariables,population=100,generation=1000,crossoverProb=0.8,mutationProb=0.03):
	import numpy as n
	trialSolution = n.empty([population,noOfVariables])
	for i in range(population):
		for j in range(noOfVariables):
			trialSolution[i][j] = n.array(n.random.uniform(minRange[j],maxRange[j]))

	for generations in range(generation):

		funValues = n.empty([population,len(func)])
		for i in range(population):
			for j in range(len(func)):
				funValues[i,j] = func[j](trialSolution[i])
		nonDominatedFront = n.empty([0,noOfVariables])
		front = n.empty([0,1])
		counter = 1
		i = 0
		while i<funValues.shape[0]:
			a = funValues[i,0]>funValues[:,0]
			b = funValues[i,1]>funValues[:,1]
			c = n.where((a & b)==True)
			if (len(c[0])!=0):
				nonDominatedFront = n.vstack((nonDominatedFront,funValues[c[0]]))
				tmp = n.repeat(counter,funValues[c[0]].shape[0])
				tmp.resize((len(tmp),1))
				front = n.vstack((front,tmp))
				counter = counter+1
			funValues = n.delete(funValues,c[0],0)
			i = i+1
		nonDominatedFront = n.vstack((nonDominatedFront,funValues))
		tmp = n.repeat(counter,funValues.shape[0])
		tmp.resize((len(tmp),1))
		front = n.vstack((front,tmp))
		nonDominatedFront = n.hstack((nonDominatedFront,front))

		#Natural Selection
		naturalSelection = []
		while len(naturalSelection)!=population:
			tmp = n.random.random_integers(population,size=2)-1
			if nonDominatedFront[tmp[0],nonDominatedFront.shape[1]-1] != nonDominatedFront[tmp[1],nonDominatedFront.shape[1]-1]:
				if nonDominatedFront[tmp[0],nonDominatedFront.shape[1]-1] < nonDominatedFront[tmp[1],nonDominatedFront.shape[1]-1]:
					naturalSelection.append(tmp[0])
				else:
					naturalSelection.append(tmp[1])
			else:
				a = crowdingDist(nonDominatedFront,tmp[0])
				b = crowdingDist(nonDominatedFront,tmp[1])
				if a<b:
					naturalSelection.append(tmp[1])
				else:
					naturalSelection.append(tmp[0])		
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
			trialSolution[tmp[0]][tmp1[0]] = n.random.uniform(minRange[tmp1[0]],maxRange[tmp1[0]])

	return list((trialSolution,nonDominatedFront))

#Main
noOfVariables = 2
minRange = [0,0]
maxRange = [5,3]
func = [f1,f2]
a = GA_multiObj(func,minRange,maxRange,noOfVariables)
