from collections import defaultdict

def BallotCount(filename):
    candidateDict = defaultdict(int)
    votersSet= set()

    with open(filename) as txt_file:
        for line in txt_file:
            vote = line.split()
            if len(vote) != 2 :
                # print error of text formating
                pass
            if  vote[0] in votersSet:
                # print fraud detection
                pass
            else:
                votersSet.add(vote[0])

            candidateDict[vote[1]] +=1

    
    print(candidateDict)
    print(votersSet)

if __name__ == "__main__":
    BallotCount("ballotData.txt")

