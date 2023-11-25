from collections import defaultdict
import operator
import pandas as pd

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#              Read like a constant stream from text file
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Candidate:
    "Candidate contains only the candidate id and their current vote number"
    def __init__(self, id):
        self.id = id
        self.votes = 0

    def __str__(self):
        return f"Candidate {self.id} with {self.votes} votes"

class BallotCounter:
    "Use to count the result of a ballot as the vote are registered."
    def __init__(self):
        self.candidateList = []
        self.votersSet = set()

    def addVote(self, votersId,candidateId):
        """The function add the vote to the correct candidate and reorder the list.
            It check for fraudster that tried to vote multiple times and ignored 
            their vote if it is the case
		Parameters: 
			votersId (string): votersid. 
            candidateId (string): candidateId.
        """
        if votersId in self.votersSet:
            print(f"Oops: there seems to be a frauder. The voter {votersId} attempted to vote more than once." )
            return

        candIdx = -1
        for index, item in enumerate(self.candidateList):
            if item.id == candidateId:
                item.votes += 1
                candIdx = index
                break

        if candIdx == -1:
            # new candidate
            self.candidateList.append(Candidate(candidateId))
            return

        while candIdx-1 >= 0:
            if self.candidateList[candIdx].votes > self.candidateList[candIdx-1].votes:
                self.swapCandidatePos(candIdx,candIdx-1)
            else:
                break


    def swapCandidatePos(self,pos1,pos2):
        self.candidateList[pos1], self.candidateList[pos2] = self.candidateList[pos2], self.candidateList[pos1]


    def getWinners(self):
        return self.candidateList[:3]
    
    
def readBallot(filename):
    """ 
		The function read from a txt file and return the 3 candidates with the most votes. 

		Parameters: 
			filename (string): The txt file to read from. 
		
		Returns: 
			list[Candidate]: list of lenght 3 that objects of class Candidate
	"""

    lineNumber = 0
    bCounter = BallotCounter()

    with open(filename) as txt_file:
        for line in txt_file:
            lineNumber+=1
            if line == "" or line.isspace():
                continue 

            vote = line.split(",")
            if len(vote) != 2 :
                print(f"WARNING: line wrongly formatted data at line {lineNumber}. Data red: {line}")
                continue
            # if we wanted to display the new winners after each vote we would put this line
            # bCounter.getWinners()
            bCounter.addVote(vote[0].strip(),vote[1].strip())

    return bCounter.getWinners()


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

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                              Main part
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

if __name__ == "__main__":
    # BallotCountPanda("ballotData.txt")

    winners = readBallot("ballotData.txt")
    print(*winners, sep="\n")

