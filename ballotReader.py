from collections import defaultdict
import operator
import pandas as pd

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

    # sort by value in reverse order
    sortedList = sorted(candidateDict.items(), key=operator.itemgetter(1), reverse=True)
    print(sortedList)

    return [winners[1] for winners in sortedList[:3]]

def BallotCountPanda(filename):
    colnames = {
        "voderId": "category",
        "candidateId": "category",
    }   

    df = pd.read_csv( filename, names=colnames,on_bad_lines = 'warn')
    
    result = df.groupby("candidateId").agg(votes=('voderId', 'count'))
    
    result = result.sort_values(by=["votes"], ascending=False)
    # so the column's title appear aligned
    result = result.reset_index()

    print(result.to_string())








if __name__ == "__main__":
    BallotCountPanda("ballotData.txt")

    winners = BallotCount("ballotData.txt")
    print(f"""The winners are: 
          First place:{winners[0]}
          First place:{winners[1]}
          First place:{winners[2]}""")

