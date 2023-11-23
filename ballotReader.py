from collections import defaultdict

def BallotCount(filename):
    candidateDict = defaultdict(int)
    votersSet= set()

    with open(filename) as txt_file:
        for line in txt_file:
            # ignore empty lines
            if line == "" or line.isspace():
                continue 

            vote = line.split(",")
            if len(vote) != 2 :
                print("WARNING: line wrongly formatted data. Data red: " + line)
                continue
            if  vote[0] in votersSet:
                print(f"Oops: there seems to be a frauder. The voter {vote[0]} attempted to vote more than once." )
                continue

            votersSet.add(vote[0])
            # maybe check for a casting error here 
            candidateDict[int(vote[1])] +=1

    
    print(candidateDict)
    print(votersSet)

if __name__ == "__main__":
    BallotCount("ballotData.txt")

