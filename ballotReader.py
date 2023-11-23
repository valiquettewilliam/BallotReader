

def BallotCount(filename):
    with open(filename) as txt_file:
        for line in txt_file:
            print(line)



if __name__ == "__main__":
    BallotCount("ballotData.txt")

