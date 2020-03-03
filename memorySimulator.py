import sys
import os
import random

class job:

    def calcRunTime(self, minTime, maxTime):
        #Calculate the run time for each job randomly based on the parameters of min-max run time
        return random.randint(minTime, maxTime)
    
    def calcMemSize(self, minMemory, maxMemory):
        #Calculate memory needs based on parameters of min-max memory size
        return random.randint(minMemory, maxMemory)

    def __init__(self, minTime, maxTime, minMemory, maxMemory):
        self.runTime = self.calcRunTime(minTime, maxTime)
        self.memSize = self.calcMemSize(minMemory, maxMemory)
        self.remainingTime = self.runTime


    def __str__(self):
        #Quick and dirty
        return (str(self.runTime) + "\t\t" + str(self.memSize))

#Method to determine if there are still jobs that have not finished.
#Small amount of testing has shown that it does work
def hasTime(jobList):
    for job in jobList:
        if(job.remainingTime > 0):
            return True
        else:
            return False
        

def main():
    #For testing purposes, the args supplemented to the program have been what are in the project
    #For Linux, running "python3 memorySimulator.py 48000 1000 3 2 15 5000 25000" should terminate
    argv = sys.argv
    totalMemory = int(argv[1])
    memoryPartition = int(argv[2])
    numSlots = totalMemory // memoryPartition
    numJobs = int(argv[3])
    i = 0
    randomSeed = 13
    random.seed(randomSeed)
    minTimeSlice = int(argv[4])
    maxTimeSlice = int(argv[5])
    minMemorySlice = int(argv[6])
    maxMemorySlice = int(argv[7])
    jobList = []
    #Could probably be a for loop but it works
    while(i < numJobs):
        jobList.append(job(minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))
        i += 1
    
    #Super ugly print statement but it shows the starting state of the simulator
    print("Simulator Parameters:\nMemory Size: %d\nPage Size: %d\nRandom Seed: %d\nNumber of Jobs: %d\nRuntime (min-max) timesteps: %d-%d\nMemory (min-max): %d-%d" % (totalMemory, memoryPartition, randomSeed, numJobs, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))

    print("Job Queue:\nJob #\t Runtime\tMemory")
    for k in range(len(jobList)):
        print(str(k + 1) + "\t" + str(jobList[k]))
    print("Simulator Starting:")
    #This shows the page table, rudimentary right now
    #TODO: implement the pageTable data structure, print should show how it should look
    pageTable = []
    for i in range(numSlots + 1):
        if(i % 16 == 0 and i != 0):
            print(".")
        if(i % 4 == 0 and i != 0 and i % 16 != 0):
            print(".", end="\t")
        else:
            print(".", end="")
    timeStep = 0
    print("")
    #Jobs that have finished are not terminating as expected
    #Possibly an error in the hasTime function
    #Does need a control to only select jobs that have enough memory/have not terminated
    while(hasTime(jobList)):
        print("Time Step " + str(timeStep))        
        print("Job " + str(timeStep % len(jobList) + 1) + " running.")
        jobList[timeStep % len(jobList)].remainingTime -= 1
        timeStep += 1


main()
