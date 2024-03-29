import time
import random
import numpy as np
from random import shuffle
from random import randrange

def calculateNumberOfConflicts(position): # returns number of conflicts
    numberOfConflicts = 0  

    for i in range(0, len(position)):
        for j in range(i + 1, len(position)):
            if position[i] == position[j]:
                numberOfConflicts += 1
            elif abs(i - j) == abs(position[i] - position[j]):
                numberOfConflicts += 1  

    return numberOfConflicts

def bestNeighbor(position): # returns the best neighbor - shd be best neighbor
    
    min_numberOfConflicts = calculateNumberOfConflicts(position) # define current position's number of conflict as the min number of conflict

    
    best_position = position # define best position as current position
    for i in range(0, len(position)):
        for j in range(0, len(position)):
            if j != position[i]:
                temp = position.copy()
                temp[i] = j
                temp_numberOfConflicts = calculateNumberOfConflicts(temp)
                if temp_numberOfConflicts <= min_numberOfConflicts:
                    min_numberOfConflicts = temp_numberOfConflicts 
                    best_position = temp 
    return best_position

def randomNeighbor(position): # returns a random neighbor which is better than the current position
    
    candidate_positions = []
    current_numberOfConflicts = calculateNumberOfConflicts(position)

    for i in range(0, len(position)):
      for j in range(0, len(position)):
        if j != position[i]:
          temp = position.copy()
          temp[i] = j
          temp_numberOfConflicts = calculateNumberOfConflicts(temp)
          if temp_numberOfConflicts < current_numberOfConflicts:
            candidate_positions.append(temp) 
    
    if len(candidate_positions) != 0:
      sample_index =  randrange(len(candidate_positions))
      return candidate_positions[sample_index]
    else:
      return position

def printSolutionT(position): #You can use it if you need
    N = len(position)

    for i in range(N):
        row = ""
        for j in range(N):
            if position[i] == j:
                row += "X "
            else:
                row += "O "
        print(row)

def NQueen(N, randomRestart, stochastic, upperBound=np.inf):
    if N in [2, 3]:
        raise ValueError("Failure, no solution exists for given N.")

    solved = False
    current_position = list(np.zeros(N))
    count = 0
    while (calculateNumberOfConflicts(current_position) > 0) and count < upperBound:
        initial_position = [randrange(N) for _ in range(N)]
        current_position = initial_position
        while True:        
            if stochastic:
                neighbor = randomNeighbor(current_position) 
            else:
                neighbor = bestNeighbor(current_position)

            if calculateNumberOfConflicts(neighbor) >= calculateNumberOfConflicts(current_position):
                if randomRestart: 
                    break
                else:
                    if calculateNumberOfConflicts(current_position) != 0:
                        return solved, count
                    else:
                        return True, count #line to be filled
            
            current_position = neighbor 
        count += 1

    if count < upperBound:
        solved = True

    return solved, count

NUM_SIMULATIONS = 100
N = 10
K_values = [10, 100, 1000]

"""## Basic Hill Climbing"""

num_successes = 0
total_time = 0
for i in range(NUM_SIMULATIONS):
  start = time.time()
  success, restart_count = NQueen(N=N, randomRestart=False, stochastic=False, upperBound=np.inf)
  end = time.time()
  total_time += (end - start)
    
  if success:
    num_successes += 1

print(f"Elapsed time: {total_time}, with {num_successes} successes in {NUM_SIMULATIONS} simulations for N={N}.")

"""# Hill Climbing With Random Restarts"""

for K in K_values:
  num_successes = 0
  total_time = 0
  total_successful_restart_count = 0

  for i in range(NUM_SIMULATIONS):
    start = time.time()
    success, restart_count = NQueen(N=N, randomRestart=True, stochastic=False, upperBound=K)
    end = time.time()
    total_time += (end - start)
      
    if success:
      num_successes += 1
      total_successful_restart_count += restart_count

  print(f"Elapsed time: {total_time}, with {num_successes} successes in {NUM_SIMULATIONS} simulations. Average # restarts per successful run : {(total_successful_restart_count * 1.0) / num_successes}. N={N}, K={K}")

"""# Stochastic Hill Climbing"""

num_successes = 0
total_time = 0

for i in range(NUM_SIMULATIONS):
  start = time.time()
  success, restart_count = NQueen(N=N, randomRestart=False, stochastic=True, upperBound=np.inf)
  end = time.time()
  total_time += (end - start)
    
  if success:
    num_successes += 1

print(f"Elapsed time: {total_time}, with {num_successes} successes in {NUM_SIMULATIONS} simulations for N={N}.")