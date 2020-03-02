import sys
import random

class job:

    def calcRunTime(self):
        return random.randint(self.minTime, self.maxTime)
    
    def calcMemSize(self):
        return random.randint(self.minMemory, self.maxMemory)

    def __init__(self, minTime, maxTime, minMemory, maxMemory):
        self.minTime = minTime
        self.maxTime = maxTime
        self.minMemory = minMemory
        self.maxMemory = maxMemory
        self.runTime = self.calcRunTime()
        self.memSize = self.calcMemSize()
        self.remainingTime = self.runTime


    def __str__(self):
        #Quick and dirty
        return ("Run time is %d, Memory Size is %d, Remaining Time: %d" % (self.runTime, self.memSize, self.remainingTime))


        

def main():
    argv = sys.argv
#   for i in range(len(argv) - 1):
#       print(argv[i + 1])
    totalMemory = int(argv[1])
    memoryPartition = int(argv[2])
    numSlots = totalMemory // memoryPartition
    numJobs = int(argv[3])
    jobsIn = 0
    i = 4
    jobList = []
    while(jobsIn != numJobs):
        for j in range(numJobs):
            #Gets the jobs in order assuming parameters of all the time segments then the memory segments.
            jobList.append(job(int(argv[i]), int(argv[i + 1]), int(argv[i + 2 * numJobs]), int(argv[i + 2 * numJobs + 1])))
            jobsIn += 1
            i += 2
    for k in range(len(jobList)):
        print(jobList[k])
    
    

main()