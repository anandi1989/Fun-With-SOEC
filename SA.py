'''
@uthor : Amit Nandi
Date : 10/12/2016

simulated annealing 
'''

#Rosebrock function
def f(x,a=1,b=100):
	return (a-x[0])**2+b*(x[1]-x[0]**2)**2

#SA function
def SA(f,minRange,maxRange,stepSize=0.01,max_itr=50000,initialT=1000,updates=10,zeta=0.9):
	import numpy as n
	trialSolution = [0]*2
	trialSolution[0] = n.random.uniform(minRange[0],maxRange[0],size=1)	
	trialSolution[1] = n.random.uniform(minRange[1],maxRange[1],size=1)
	tmp = trialSolution
	T = initialT
	e1 = f(trialSolution)
	energyValue = []
	solution = []
	for i in range(updates):
		for itr in range(max_itr):
			trialSolution = [0]*2
       	        	trialSolution[0] = tmp[0]+n.random.uniform(-1,1,size=1)*stepSize
                	trialSolution[1] = tmp[1]+n.random.uniform(-1,1,size=1)*stepSize
			e2 = f(trialSolution)
			deltaE = e2-e1
			if ( n.random.uniform(0,1,size=1)<n.exp(-deltaE/T) or e2<e1 ):
				tmp = trialSolution
				energyValue.append(e2)
				solution.append(tmp)
		T = zeta*T
	energyValue = n.array(energyValue)
	index = energyValue.argmin()
	finalSolution = solution[index]
	return list((finalSolution,energyValue[index]))

#Main
minRange = [0.5,0.5]
maxRange = [1.5,1.5]
a = SA(f,minRange,maxRange)
print a
