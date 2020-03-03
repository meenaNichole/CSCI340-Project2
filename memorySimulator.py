import sys
import random

class job:

    def calcRunTime(self, minTime, maxTime):
        return random.randint(minTime, maxTime)
    
    def calcMemSize(self, minMemory, maxMemory):
        return random.randint(minMemory, maxMemory)

    def __init__(self, minTime, maxTime, minMemory, maxMemory):
        self.runTime = self.calcRunTime(minTime, maxTime)
        self.memSize = self.calcMemSize(minMemory, maxMemory)
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
    i = 0
    minTimeSlice = int(argv[4])
    maxTimeSlice = int(argv[5])
    minMemorySlice = int(argv[6])
    maxMemorySlice = int(argv[7])
    jobList = []
    while(i < numJobs):
        jobList.append(job(minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))
        i += 1

    print("Simulator Parameters:\nMemory Size: %d\nPage Size: %d\nRandom Seed: 2\nNumber of Jobs: %d\nRuntime (min-max) timesteps: %d-%d\nMemory (min-max): %d-%d" % (totalMemory, memoryPartition, numJobs, minTimeSlice, maxTimeSlice, minMemorySlice, maxMemorySlice))

    for k in range(len(jobList)):
        print(jobList[k])
    
    

main()