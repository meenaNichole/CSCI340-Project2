import sys
import os
import random
import copy

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
        self.startTime = 0
        self.finishTime = 0
        self.neededSlots = 0
        self.startedJob = False


    def __str__(self):
        #Quick and dirty
        return (str(self.runTime) + "\t\t" + str(self.memSize))

#Method to determine if there are still jobs that have not finished.
#Small amount of testing has shown that it does work
def hasTime(jobList):
    hasTime = False
    for job in jobList:
        if(job.remainingTime >= 0):
            hasTime = True
    return hasTime

#Helper Methods
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

#Finds the first open slot in the page table to allow for quick finding of open slots
def firstOpenSlot(pageTable):
    for i in range(len(pageTable)):
        if(pageTable[i] == '.'):
            return i

#Deletes the job from the page table, once the job is finished
def deleteAll(pageTable, idToRem):
    for i in range(len(pageTable)):
        if(pageTable[i] == idToRem):
            pageTable[i] = "."
    return pageTable

#Finds the job in the job list for saving start/end time
#Needed for implementation of "removing jobs"
def findJob(jobList, idNum):
    for i in range(len(jobList)):
        if(jobList[i].jobNum == idNum):
            return i

#Not working as intended, not populating jobs that are not running
def addJobs(pageTable, jobList):
    availableSlots = 0
    jobIterator = 0
    for i in range(len(pageTable)):
        if(pageTable[i] == '.'):
            availableSlots += 1
            if(availableSlots > jobList[jobIterator].neededSlots and not jobList[jobIterator].startedJob):
                pageTable[i - availableSlots] = jobList[jobIterator].jobNum
                availableSlots -= 1
    return pageTable                
        

def main():
    #For testing purposes, the args supplemented to the program have been what are in the project
    #For Linux, running "python3 memorySimulator.py 48000 1000 3 2 15 5000 25000" should terminate
    argv = sys.argv
    totalMemory = int(argv[1])
    memoryPartition = int(argv[2])
    numSlots = totalMemory // memoryPartition
    availableSlots = numSlots
    numJobs = int(argv[3])
    randomSeed = 13
    random.seed(randomSeed)
    minTimeSlice = int(argv[4])
    maxTimeSlice = int(argv[5])
    minMemorySlice = int(argv[6])
    maxMemorySlice = int(argv[7])
    jobList = []
    finalJobList = []

	#amount of memory that is left based on total memory divinded by the memoryPartition
    remainingMemory = int(totalMemory) / int(memoryPartition)
	
	#changed the while loop to a for loop, more efficient
    for i in range(int(numJobs)):
        jobList.append(job(i + 1, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))
        jobList[i].neededSlots = jobList[i].memSize // memoryPartition
        finalJobList = copy.deepcopy(jobList)
    #Super ugly print statement but it shows the starting state of the simulator
    print("Simulator Parameters:\nMemory Size: %d\nPage Size: %d\nRandom Seed: %d\nNumber of Jobs: %d\nRuntime (min-max) timesteps: %d-%d\nMemory (min-max): %d-%d" % (totalMemory, memoryPartition, randomSeed, numJobs, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))

    print("Job Queue:\nJob #\t Runtime\tMemory")
    for k in range(len(jobList)):
        print(str(k + 1) + "\t" + str(jobList[k]))
    print("Simulator Starting:")
    pageTable = []
    for i in range(numSlots):
        pageTable.append(".")
    #Method to print the page table just to make life easier
    printTable(pageTable, len(pageTable))
    timeStep = 0
    print("")
    runningJobs = []
    for i in range(len(jobList)):
        if(jobList[i].neededSlots <= availableSlots):
            runningJobs.append(jobList[i])
            jobList[i].startedJob = True
            numPages = jobList[i].neededSlots
            availableSlots -= numPages
            firstAvailableSlot = firstOpenSlot(pageTable)
            k = 0
            while(numPages > 0):
                pageTable[firstAvailableSlot + k] = (i + 1)
                k += 1
                numPages -= 1
            k = 0
            

    #Iterates through the jobs and checks to see if time remains
    runJob = runningJobs[timeStep]
    while(hasTime(runningJobs)):
        print("Time Step " + str(timeStep))
        runJob = runningJobs[timeStep % len(runningJobs)]
        jobStats = finalJobList[findJob(finalJobList, runJob.jobNum)]
        print("Job " + str(runJob.jobNum) + " running")
        runJob.remainingTime -= 1
        if(runJob.remainingTime <= 0):
            print("Job " + str(runJob.jobNum) + " finished.")
            jobStats.finishTime = timeStep
            runningJobs.remove(runJob)
            pageTable = deleteAll(pageTable, runJob.jobNum)
            pageTable = addJobs(pageTable, jobList)
        printTable(pageTable, len(pageTable))
        timeStep += 1
    print("\nJob information:\nJob #\tStart Time\tEnd Time")
    for finishedJob in finalJobList:
        print(str(finishedJob.jobNum) + "\t" + str(finishedJob.startTime) + "\t\t" + str(finishedJob.finishTime))


main()
