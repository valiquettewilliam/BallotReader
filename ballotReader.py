from collections import defaultdict
import operator
import pandas as pd

def BallotCount(filename):
    """ 
		The function read from a txt file and return the 3 candidates with the most votes. 

		Parameters: 
			filename (string): The txt file to read from. 
		
		Returns: 
			list[tuple]: list of lenght 3 that contains tuple as (CandidateID, votes) 
	"""
    candidateDict = defaultdict(int)
    votersSet= set()
    lineNumber = 0

    with open(filename) as txt_file:
        for line in txt_file:
            lineNumber+=1
            # ignore empty lines
            if line == "" or line.isspace():
                continue 

            vote = line.split(",")
            if len(vote) != 2 :
                print(f"WARNING: line wrongly formatted data at line {lineNumber}. Data red: {line}")
                continue
            if  vote[0] in votersSet:
                print(f"Oops: there seems to be a frauder. The voter {vote[0]} attempted to vote more than once." )
                continue

            votersSet.add(vote[0])
            try:
                candidateDict[int(vote[1])] +=1
            except ValueError:
                print(f"WARNING: Found vote data which is not a number at line {lineNumber}. Data red: {line}")

    # sort by value in reverse order
    sortedList = sorted(candidateDict.items(), key=operator.itemgetter(1), reverse=True)

    return sortedList[:3]


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                       Pandas DataFrame section
#               If we were to read it not like a stream
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
class BallotReader:
    COLUMS_NAMES = ["voderId","candidateId"]

    def __init__(self, ballotFilename):
        self.filename = ballotFilename
        self.df = pd.DataFrame()

    def readFile(self):
        self.df = pd.read_csv( self.filename, names=self.COLUMS_NAMES,on_bad_lines = 'warn')


    def getFraudster(self):
        fraudster =  self.df[self.df.duplicated(subset="voderId")]
        return fraudster["voderId"].to_list()
        
    def removeFraudster(self):
        self.df = self.df.drop_duplicates(subset="voderId",keep=False)

    def getTop3(self):
        result = self.df.drop_duplicates(subset="voderId",keep=False)
        result = result.groupby("candidateId").agg(votes=('voderId', 'count'))
        result = result.sort_values(by=["votes"], ascending=False)
        # so the column's title appear aligned
        result = result.reset_index()
        return result.head(3)


def BallotCountPanda(filename):
    ballotR = BallotReader(filename)

    ballotR.readFile()

    fraudster = ballotR.getFraudster()
    if fraudster:
        print("Opps! We seems to have some fraudster. Here are their voterId:")
        print(' '.join(map(str, fraudster) ))
        print("All of their votes will be remove from the count.")
        ballotR.removeFraudster()
    
    winners = ballotR.getTop3()
    print("The top 3 candidates are:")
    print(winners.to_string(index=False))


if __name__ == "__main__":
    # BallotCountPanda("ballotData.txt")

    help(BallotCount)

    winners = BallotCount("ballotData.txt")
    print(f"""The winners are: 
          First place:  {winners[0][0]}  with {winners[0][1]} votes.
          Second place: {winners[1][0]}  with {winners[1][1]} votes.
          Third place:  {winners[2][0]}  with {winners[2][1]} votes.  """)

