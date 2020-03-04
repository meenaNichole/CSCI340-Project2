import sys
import os
import random

# Short README:
# To run this program:
# Using the terminal, navigate to directory containing the program.
# Run: python3 memorySimulator.py <totalMemory><memoryPartition><numJobs><minTime><maxTime><minMemory><maxMemory>
#	example: python3 memorySimulator.py 48000 1000 3 2 15 5000 25000
#


#This method makes the memory values multiples of the page size
def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier



class job:

    def calcRunTime(self, minTime, maxTime):
        #Calculate the run time for each job randomly based on the parameters of min-max run time
        return random.randint(minTime, maxTime)
    
    def calcMemSize(self, minMemory, maxMemory):
        #Calculate memory needs based on parameters of min-max memory size
        return int(truncate(random.randint(minMemory, maxMemory), -3))

    def __init__(self, jobNum, minTime, maxTime, minMemory, maxMemory):
        self.jobNum = jobNum
        self.runTime = self.calcRunTime(minTime, maxTime)
        self.memSize = self.calcMemSize(minMemory, maxMemory)
        self.remainingTime = self.runTime


    def __str__(self):
        #Quick and dirty
        return (str(self.runTime) + "\t\t" + str(self.memSize))

#Method to determine if there are still jobs that have not finished.
#Small amount of testing has shown that it does work
def hasTime(jobList):
    hasTime = False
    for job in jobList:
        if(job.remainingTime > 0):
            hasTime = True
    return hasTime

def printTable(pageTable, tableSize):
    i = 0
    while(i < len(pageTable)):
        if(i % 16 == 15 and i != 0):
            print(pageTable[i])
        elif(i % 4 == 3 and i != 0 and i % 16 != 15):
            print(pageTable[i], end="\t")
            
        else:
            #print(i,end="")
            print(pageTable[i], end="")   
        i += 1
        

def main():
    #For testing purposes, the args supplemented to the program have been what are in the project
    #For Linux, running "python3 memorySimulator.py 48000 1000 3 2 15 5000 25000" should terminate
    argv = sys.argv
    totalMemory = int(argv[1])
    memoryPartition = int(argv[2])
    numSlots = totalMemory // memoryPartition
    numJobs = int(argv[3])
    randomSeed = 13
    random.seed(randomSeed)
    minTimeSlice = int(argv[4])
    maxTimeSlice = int(argv[5])
    minMemorySlice = int(argv[6])
    maxMemorySlice = int(argv[7])
    jobList = []
    #Could probably be a for loop but it works
   	

	#amount of memory that is left based on total memory divinded by the memoryPartition
    remainingMemory = int(totalMemory) / int(memoryPartition)

	#changed the while loop to a for loop, it's more efficient
    for i in range(int(numJobs)):

        jobList.append(job(i, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))
    
    #Super ugly print statement but it shows the starting state of the simulator
    print("Simulator Parameters:\nMemory Size: %d\nPage Size: %d\nRandom Seed: %d\nNumber of Jobs: %d\nRuntime (min-max) timesteps: %d-%d\nMemory (min-max): %d-%d" % (totalMemory, memoryPartition, randomSeed, numJobs, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))

    print("Job Queue:\nJob #\t Runtime\tMemory")
    for k in range(len(jobList)):
        print(str(k) + "\t" + str(jobList[k]))
    print("Simulator Starting:")
    pageTable = []
    for i in range(numSlots):
        pageTable.append(".")

    #Method to print the page table just to make life easier
    printTable(pageTable, len(pageTable))
    timeStep = 0
    print("")

    #Iterates through the jobs and checks to see if time remains
    runJob = jobList[timeStep]
    nextJobLoop = 0
    while(hasTime(jobList)):
        print("Time Step " + str(timeStep))
        runJob = jobList[(timeStep + nextJobLoop) % len(jobList)]

        #Iterates through the list to skip jobs that have no time left
        while(runJob.remainingTime <= 0):
            runJob = jobList[(timeStep + nextJobLoop) % len(jobList)]
        print("Job " + str(runJob.jobNum + 1) + " running")
        nextJobLoop = 0
        runJob.remainingTime -= 1
        if(runJob.remainingTime == 0):
            print("Job " + str(runJob.jobNum + 1) + " finished.")
            jobList.remove(runJob)
        printTable(pageTable, len(pageTable))
        timeStep += 1


main()
